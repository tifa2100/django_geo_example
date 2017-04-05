from django.shortcuts import render
from django.core.files.storage import FileSystemStorage







from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.contrib.gis.gdal import DataSource
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
# Import system modules
import itertools
import tempfile
import os
# Import custom modules
from managetasks.models import PointsCore
import json


from mapwidgets.widgets import GooglePointFieldWidget

def index(request):
    pointsCore = PointsCore.objects.order_by('auto_id')
    template = loader.get_template('managetasks/index.html')
    context = RequestContext(request, {
        'point_cores': pointsCore, 'content': render_to_string('managetasks/waypoints.html', {'point_cores': pointsCore})
    })
    return HttpResponse(template.render(context))


@csrf_exempt
################## doesnt work without the @csrf_exempt.  Have to figure out why this is the case#########
def save(request):
    c = {}
    c.update(csrf(request))
    for waypointString in request.POST.get('waypointsPayload', '').splitlines():
        waypointID, waypointX, waypointY = waypointString.split()
        waypoint = Waypoint.objects.get(id=int(waypointID))
        waypoint.geometry.set_x(float(waypointX))
        waypoint.geometry.set_y(float(waypointY))
        waypoint.save()
    return HttpResponse(json.dumps(dict(isOk=1)), c)


def search(request):
    # Build searchPoint
    try:
        searchPoint = Point(float(request.GET.get('lng')), float(request.GET.get('lat')))
    except:
        return HttpResponse(json.dumps(dict(isOk=0, message='Could not parse search point')))
    # Search database
    waypoints = PointsCore.objects.distance(searchPoint).order_by('distance')
    # Return
    return HttpResponse(json.dumps(dict(
        isOk=1,
        content=render_to_string('waypoints/waypoints.html', {
            'waypoints': waypoints
        }),
        waypointByID=dict((x.id, {
            'name': x.name,
            'lat': x.geometry.y,
            'lng': x.geometry.x,
        }) for x in waypoints),
    )))


def upload(request):
    if 'gpx' in request.FILES:
        # Get
        try:
            gpxFile = request.FILES['gpx']
        except IOError:
            print("gpx")


        handle, targetPath = tempfile.mkstemp()
        destination = os.fdopen(handle, 'wb')
        for chunk in gpxFile.chunks():
            destination.write(chunk)
        destination.close()

        # Parse
        dataSource = DataSource(targetPath)

        layer = dataSource[0]
        waypointNames = layer.get_fields('name')
        waypointGeometries = layer.get_geoms()

        # name change from Python 2 to 3
        try:
            zip_longest = itertools.zip_longest  # Python 3
        except AttributeError:
            zip_longest = itertools.izip_longest  # Python 2

        for waypointName, waypointGeometry in zip_longest(waypointNames, waypointGeometries):
            waypoint = Waypoint(name=waypointName, geometry=waypointGeometry.wkt)
            waypoint.save()

        # Clean up: took out the os.remove(targetPath)


    return HttpResponseRedirect(reverse('waypoints-index'))

























































# View For Upload Images
def upload_places(request):
    AWS_ACCESS_KEY = ''
    AWS_ACCESS_SECRET_KEY = ''
    if request.method == 'POST' and request.FILES['myfile']:
        for myfile in request.FILES.getlist('myfile'):
            key = myfile.name
            bucket = 'zoser-pois-photos'
            path = 'test_upload'
            if not upload_to_s3(AWS_ACCESS_KEY, AWS_ACCESS_SECRET_KEY, myfile, bucket, key, path):
                return render(request, 'managetasks/simple_upload.html', {
                    'uploaded_file_url': 'Nothing Uploaded'
                    })
    return render(request, 'managetasks/simple_upload.html')


def point_core(request):
    pass















def upload_places_storage(request):
    if request.method == 'POST' and request.FILES['myfile']:
        for myfile in request.FILES.getlist('myfile'):
            #myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
        return render(request, 'managetasks/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'managetasks/simple_upload.html')


def upload_places_new(request):
    AWS_ACCESS_KEY = ''
    AWS_ACCESS_SECRET_KEY = ''

    file = open('someFile.txt', 'r+')

    key = file.name
    bucket = 'zoser-pois-photos'

    if upload_to_s3(AWS_ACCESS_KEY, AWS_ACCESS_SECRET_KEY, file, bucket, key):
        print ('It worked!')
    else:
        print ('The upload failed...')


import os

import boto
from boto.s3.key import Key

def upload_to_s3(aws_access_key_id, aws_secret_access_key, file, bucket, key, sub_directory, callback=None, md5=None, reduced_redundancy=False, content_type=None):
    """
    Uploads the given file to the AWS S3
    bucket and key specified.

    callback is a function of the form:

    def callback(complete, total)

    The callback should accept two integer parameters,
    the first representing the number of bytes that
    have been successfully transmitted to S3 and the
    second representing the size of the to be transmitted
    object.

    Returns boolean indicating success/failure of upload.
    """
    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucket, validate=True)
    k = Key(bucket)
    if sub_directory != "":
        k.key = os.path.join(sub_directory, key)
    else:
        k.key = key
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)

    # Rewind for later use
    file.seek(0)

    if sent == size:
        return True
    return False















######################3
from .models import PointsCore
from django.shortcuts import render_to_response, get_object_or_404, redirect

def ShowZonen(request):
    zone=PointsCore.objects.all()
    return render_to_response('zonen.html', {"zone": zone})


def showZoneDetail(request, zone_id):
    zone=PointsCore.objects.get(id=zone_id)
    return render_to_response('zonendetail.html', {"zone": zone})
