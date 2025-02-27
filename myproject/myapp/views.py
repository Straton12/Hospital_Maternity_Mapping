from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Transform
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from .models import KenyaSubcounty, KenyaCounty, KenyaCountry, Hospitals, level4_buffer, level5_buffer
from .serializers import KenyaSubcountySerializer, KenyaCountySerializer, KenyaCountrySerializer, HospitalsSerializer, Level4BufferSerializer, Level5BufferSerializer
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
import logging
from collections import defaultdict


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def home(request):
    return render(request, "home.html")

def map_view(request):
    return render(request, "base.html")

class KenyaSubcountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KenyaSubcounty.objects.all()
    serializer_class = KenyaSubcountySerializer

class KenyaCountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KenyaCountry.objects.all()
    serializer_class = KenyaCountrySerializer

class KenyaCountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KenyaCounty.objects.all()
    serializer_class = KenyaCountySerializer
    




class HospitalsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hospitals.objects.all()
    serializer_class = HospitalsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(facility__icontains=search_query)
        return queryset

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def filtered(self, request):
        bbox = request.query_params.get('bbox')
        zoom = int(request.query_params.get('zoom', 3))

        if bbox:
            bbox = list(map(float, bbox.split(',')))
            polygon = Polygon.from_bbox(bbox)

            # Optimize by using __intersects instead of __within
            hospitals = Hospitals.objects.filter(geom__intersects=polygon)

            # Reduce number of hospitals for lower zoom levels
            if zoom < 10:
                hospitals = hospitals[:500]  # Load fewer points at low zoom

            # Transform to a projected CRS for better performance
            hospitals = hospitals.annotate(geom_transformed=Transform("geom", 4326))

            serializer = HospitalsSerializer(hospitals, many=True)
            return Response({'type': 'FeatureCollection', 'features': serializer.data})

        return Response({'type': 'FeatureCollection', 'features': []})
    

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def within_polygon(self, request):
        from django.contrib.gis.geos import GEOSGeometry
        
        geometry = request.data.get('geometry')
        if not geometry:
            return Response({'error': 'No geometry provided'}, status=400)

        try:
            geom = GEOSGeometry(str(geometry), srid=4326)
            hospitals = Hospitals.objects.filter(geom__intersects=geom)
            level_counts = hospitals.values('keph_level').annotate(count=Count('keph_level'))
            serializer = self.get_serializer(hospitals, many=True)
            response_data = {
                'type': 'FeatureCollection',
                'features': serializer.data,
                'stats': {f'Level {item["keph_level"]}': item["count"] for item in level_counts}
            }
            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    
    
class Level4BufferViewSet(viewsets.ModelViewSet):
    queryset = level4_buffer.objects.all()
    serializer_class = Level4BufferSerializer

class Level5BufferViewSet(viewsets.ModelViewSet):
    queryset = level5_buffer.objects.all()
    serializer_class = Level5BufferSerializer
    
def analytics_view(request):
    return render(request, 'analytics.html') 

@login_required
def analytics_view(request):
    # Fetch all counties and subcounties from the database
    counties = KenyaCountry.objects.values_list('adm0_en', flat=True).distinct()
    subcounties = KenyaSubcounty.objects.values_list('adm2_en', 'adm1_en').distinct()
    
    # Convert subcounties to a dictionary where the key is the county and the value is a list of subcounties
    subcounties_dict = {}
    for subcounty, county in subcounties:
        if county not in subcounties_dict:
            subcounties_dict[county] = []
        subcounties_dict[county].append(subcounty)
    
    return render(request, "analytics.html", {"counties": counties, "subcounties": subcounties_dict})
# View to fetch buffer distances
@login_required
def buffer(request):
    # Fetch buffer distances for Level 4 and Level 5
    level4_buffers = level4_buffer.objects.values_list('distance', flat=True).distinct().order_by('distance')
    level5_buffers = level5_buffer.objects.values_list('distance', flat=True).distinct().order_by('distance')
    
    return render(request, "analytics.html", {
        "level4_buffers": list(level4_buffers),
        "level5_buffers": list(level5_buffers),
    })
    

@login_required
def get_buffer_distances(request):
    county_name = request.GET.get('county', None)
    subcounty_name = request.GET.get('subcounty', None)

    if not county_name:
        return JsonResponse({'error': 'County not provided'}, status=400)

    try:
        # Get the geometry of the selected county
        county = KenyaCountry.objects.get(adm0_en=county_name)
        county_geom = county.geom

        # Filter buffers that intersect with the selected county
        level4_buffers = level4_buffer.objects.filter(geom__intersects=county_geom).values_list('distance', flat=True).distinct().order_by('distance')
        level5_buffers = level5_buffer.objects.filter(geom__intersects=county_geom).values_list('distance', flat=True).distinct().order_by('distance')

        if subcounty_name:
            # Get the geometry of the selected subcounty
            subcounty = KenyaSubcounty.objects.get(adm2_en=subcounty_name)
            subcounty_geom = subcounty.geom

            # Filter buffers that intersect with the selected subcounty
            level4_buffers = level4_buffer.objects.filter(geom__intersects=subcounty_geom).values_list('distance', flat=True).distinct().order_by('distance')
            level5_buffers = level5_buffer.objects.filter(geom__intersects=subcounty_geom).values_list('distance', flat=True).distinct().order_by('distance')

        return JsonResponse({
            'level4_buffers': list(level4_buffers),
            'level5_buffers': list(level5_buffers),
        })

    except KenyaCountry.DoesNotExist:
        return JsonResponse({'error': 'County not found'}, status=404)
    except KenyaSubcounty.DoesNotExist:
        return JsonResponse({'error': 'Subcounty not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



logger = logging.getLogger(__name__)

@login_required
def count_hospitals_in_buffer(request):
    buffer_type = request.GET.get('buffer_type', None)  # 'level4' or 'level5'
    buffer_distance = request.GET.get('buffer_distance', None)  # Distance in km
    county_name = request.GET.get('county', None)  # Optional: Filter by county
    subcounty_name = request.GET.get('subcounty', None)  # Optional: Filter by subcounty

    if not buffer_type or not buffer_distance:
        return JsonResponse({'error': 'Buffer type and distance are required'}, status=400)

    try:
        # Convert buffer distance to float
        buffer_distance = float(buffer_distance)

        # Get the buffer geometry based on the selected buffer type and distance
        if buffer_type == 'level4':
            buffer = level4_buffer.objects.filter(distance=buffer_distance).first()
        elif buffer_type == 'level5':
            buffer = level5_buffer.objects.filter(distance=buffer_distance).first()
        else:
            return JsonResponse({'error': 'Invalid buffer type'}, status=400)

        if not buffer:
            return JsonResponse({'error': 'Buffer not found'}, status=404)

        # Get the buffer geometry
        buffer_geom = buffer.geom

        # Filter hospitals within the buffer geometry
        hospitals = Hospitals.objects.filter(geom__within=buffer_geom)

        # Optional: Filter by county or subcounty
        if county_name:
            hospitals = hospitals.filter(county__iexact=county_name)
        if subcounty_name:
            hospitals = hospitals.filter(sub_county__iexact=subcounty_name)

        # Group hospitals by their keph_level
        hospitals_by_level = defaultdict(list)
        for hospital in hospitals:
            hospitals_by_level[hospital.keph_level].append({
                'facility': hospital.facility,
                'county': hospital.county,
                'sub_county': hospital.sub_county,
                'ward': hospital.ward,
                'ownership': hospital.ownership,
            })

        return JsonResponse({
            'hospital_count': hospitals.count(),
            'hospitals_by_level': hospitals_by_level,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
    
@login_required
def get_hospital_stats(request):
    county_name = request.GET.get('county')

    if not county_name:
        return JsonResponse({'error': 'County not provided'}, status=400)

    # Get hospital counts by KEPH Level
    hospitals = Hospitals.objects.filter(county=county_name)
    level_counts = hospitals.values('keph_level').annotate(count=Count('keph_level'))

    # Get hospital counts by Subcounty & Level
    subcounty_counts = hospitals.values('sub_county', 'keph_level').annotate(count=Count('keph_level'))
    
    # Get hospital counts by Ownership
    ownership_counts = hospitals.values('ownership').annotate(count=Count('ownership'))
    
    # Count hospitals by Ownership & Subcounty
    ownership_subcounty_counts = hospitals.values('sub_county', 'ownership').annotate(count=Count('ownership'))

    # Get QQ3 Distribution per County
    qq3_county_data = hospitals.values('qq3').annotate(count=Count('qq3'))

    # Get QQ3 Distribution per Subcounty
    qq3_subcounty_data = hospitals.values('sub_county', 'qq3').annotate(count=Count('qq3'))

    # Convert to dictionary
    stats = {
        f'Level {item["keph_level"].replace("Level ", "")}': item["count"] for item in level_counts
    }
    
    subcounty_data = {}
    for item in subcounty_counts:
        subcounty = item['sub_county'] or "Unknown"
        level = f'Level {item["keph_level"].replace("Level ", "")}'

        if subcounty not in subcounty_data:
            subcounty_data[subcounty] = {}

        subcounty_data[subcounty][level] = item["count"]

    ownership_data = {item["ownership"]: item["count"] for item in ownership_counts}

    ownership_subcounty_data = {}
    for item in ownership_subcounty_counts:
        subcounty = item['sub_county'] or "Unknown"
        ownership = item["ownership"]

        if subcounty not in ownership_subcounty_data:
            ownership_subcounty_data[subcounty] = {}

        ownership_subcounty_data[subcounty][ownership] = item["count"]

    # Convert QQ3 data to dictionaries
    qq3_county_dict = {item['qq3']: item['count'] for item in qq3_county_data}

    qq3_subcounty_dict = {}
    for item in qq3_subcounty_data:
        subcounty = item['sub_county'] or "Unknown"
        qq3 = item["qq3"]

        if subcounty not in qq3_subcounty_dict:
            qq3_subcounty_dict[subcounty] = {}

        qq3_subcounty_dict[subcounty][qq3] = item["count"]

    # Calculate total hospitals
    total_hospitals = sum(stats.values())
    
    stats['total'] = total_hospitals  
    stats['subcounty_data'] = subcounty_data  
    stats['ownership_data'] = ownership_data 
    stats['ownership_subcounty_data'] = ownership_subcounty_data  

    # Add QQ3 data to the response
    stats['qq3_county_data'] = qq3_county_dict
    stats['qq3_subcounty_data'] = qq3_subcounty_dict

    return JsonResponse(stats)


