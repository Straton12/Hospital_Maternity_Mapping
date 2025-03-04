import os
import django
import sys

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

# Add the project path to `sys.path`
sys.path.append("/app")

# Initialize Django
django.setup()

from django.contrib.gis.utils import LayerMapping
from myapp.models import KenyaCountry
from django.contrib.gis.gdal import DataSource



# Auto-generated `LayerMapping` dictionary for Kenya_coutry model
kenya_coutry_mapping = {
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'adm0_en': 'ADM0_EN',
    'date': 'date',
    'validon': 'validOn',
    'geom': 'POLYGON',
}



def import_data(verbose=True):
    file = os.getcwd() + "/Datasets/Country.shp"
    data_source = DataSource(file)
    kenya_counties_layer = data_source[0].name
    
    kenya_counties_layermapping = LayerMapping(
        KenyaCountry, file, kenya_coutry_mapping, layer = kenya_counties_layer
        )
    
    kenya_counties_layermapping.save(strict = True, verbose=verbose)