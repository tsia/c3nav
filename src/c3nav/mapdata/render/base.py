import pickle

from django.db import transaction
from django.db.models import Q
from shapely.ops import unary_union

from c3nav.mapdata.models import Level


class LevelGeometries:
    def __init__(self):
        self.altitudeareas = []
        self.walls = None
        self.doors = None

    @staticmethod
    def rebuild():
        levels = Level.objects.prefetch_related('altitudeareas', 'buildings', 'doors', 'spaces',
                                                'spaces__holes', 'spaces__columns')
        for level in levels:
            geoms = LevelGeometries()
            buildings_geom = unary_union([b.geometry for b in level.buildings.all()])

            for space in level.spaces.all():
                if space.outside:
                    space.geometry = space.geometry.difference(buildings_geom)
                space.geometry = space.geometry.difference(unary_union([c.geometry for c in space.columns.all()]))
                space.holes_geom = unary_union([h.geometry for h in space.holes.all()])
                space.walkable_geom = space.geometry.difference(space.holes_geom)

            spaces_geom = unary_union([s.geometry for s in level.spaces.all()])
            geoms.doors = unary_union([d.geometry for d in level.doors.all()])
            walkable_geom = unary_union([s.walkable_geom for s in level.spaces.all()]).union(geoms.doors)

            for altitudearea in level.altitudeareas.all():
                geoms.altitudeareas.append((altitudearea.geometry.intersection(walkable_geom), altitudearea.altitude))

            geoms.walls = buildings_geom.difference(spaces_geom).difference(geoms.doors)
            level.geoms_cache = pickle.dumps(geoms)
            level.save()

        with transaction.atomic():
            for level in levels:
                level.save()


def get_render_level_data(level):
    levels = Level.objects.filter(Q(on_top_of=level.pk) | Q(base_altitude__lte=level.base_altitude))
    levels = levels.values_list('geoms_cache', 'default_height')
    return levels
