import os
from django.contrib.gis.utils import LayerMapping
from myapp.models import level4_buffer
from django.contrib.gis.gdal import DataSource



# Auto-generated `LayerMapping` dictionary for level4_buffer model
level4_buffer_mapping = {
    'distance': 'distance',
    'geom': 'POLYGON',
}

def import_data(verbose=True):
    file = os.getcwd() + "/Datasets/level4_buffer.shp"
    data_source = DataSource(file)
    level4_buffer_layer = data_source[0].name
    
    level4_buffer_layermapping = LayerMapping(
        level4_buffer, file, level4_buffer_mapping, layer = level4_buffer_layer
        )
    
    level4_buffer_layermapping.save(strict = True, verbose=verbose)