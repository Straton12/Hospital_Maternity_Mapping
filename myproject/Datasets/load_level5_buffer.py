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
from myapp.models import level5_buffer
from django.contrib.gis.gdal import DataSource



# Auto-generated `LayerMapping` dictionary for level4_buffer model
level5_buffer_mapping = {
    'distance': 'distance',
    'geom': 'POLYGON',
}

def import_data(verbose=True):
    file = os.getcwd() + "/Datasets/level5_buffer.shp"
    data_source = DataSource(file)
    level5_buffer_layer = data_source[0].name
    
    level5_buffer_layermapping = LayerMapping(
        level5_buffer, file, level5_buffer_mapping, layer = level5_buffer_layer
        )
    
    level5_buffer_layermapping.save(strict = True, verbose=verbose)