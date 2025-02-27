from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import KenyaSubcounty, KenyaCountry, KenyaCounty, Hospitals, level4_buffer, level5_buffer

class KenyaSubcountySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = KenyaSubcounty
        fields = '__all__'
        geo_field = 'geom'

class KenyaCountrySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = KenyaCountry
        fields = '__all__'
        geo_field = 'geom'

class KenyaCountySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = KenyaCounty
        fields = '__all__'
        geo_field = 'geom'

class HospitalsSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hospitals
        fields = '__all__'  # Include all model fields
        geo_field = 'geom'  # Specify the field that holds geospatial data
        
class Level4BufferSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = level4_buffer
        fields = ['id', 'distance']
        geo_field = 'geom'

class Level5BufferSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = level5_buffer
        fields = ['id', 'distance']
        geo_field = 'geom'