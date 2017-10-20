import os

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseNotModified
from shapely.geometry import box

from c3nav.mapdata.models import Level, MapUpdate, Source
from c3nav.mapdata.render.svg import SVGRenderer


def tile(request, level, zoom, x, y, format):
    zoom = int(zoom)
    if not (0 <= zoom <= 10):
        raise Http404

    bounds = Source.max_bounds()

    x, y = int(x), int(y)
    size = 256/2**zoom
    minx = size * x
    miny = size * (-y-1)
    maxx = minx + size
    maxy = miny + size

    if not box(bounds[0][1], bounds[0][0], bounds[1][1], bounds[1][0]).intersects(box(minx, miny, maxx, maxy)):
        raise Http404

    renderer = SVGRenderer(level, miny, minx, maxy, maxx, scale=2**zoom, user=request.user)

    update_cache_key = MapUpdate.cache_key()
    access_cache_key = renderer.access_cache_key
    etag = update_cache_key+'_'+access_cache_key

    if_none_match = request.META.get('HTTP_IF_NONE_MATCH')
    if if_none_match == etag:
        return HttpResponseNotModified()

    f = None
    if settings.CACHE_TILES:
        dirname = os.path.sep.join((settings.TILES_ROOT, update_cache_key, level, str(zoom), str(x), str(y)))
        filename = os.path.sep.join((dirname, access_cache_key+'.'+format))

        try:
            f = open(filename, 'rb')
        except FileNotFoundError:
            pass

    content_type = 'image/svg+xml' if format == 'svg' else 'image/png'

    if not settings.CACHE_TILES or f is None:
        try:
            renderer.check_level()
        except Level.DoesNotExist:
            raise Http404

        svg = renderer.render()
        if format == 'svg':
            data = svg.get_xml()
            filemode = 'w'
        elif format == 'png':
            data = svg.get_png()
            filemode = 'wb'
        else:
            raise ValueError

        if settings.CACHE_TILES:
            # noinspection PyUnboundLocalVariable
            os.makedirs(dirname, exist_ok=True)
            # noinspection PyUnboundLocalVariable
            with open(filename, filemode) as f:
                f.write(data)
    else:
        data = f.read()

    response = HttpResponse(data, content_type)
    response['ETag'] = etag
    response['Cache-Control'] = 'no-cache'

    return response
