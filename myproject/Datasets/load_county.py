import os
from django.contrib.gis.utils import LayerMapping
from myapp.models import Kenya_counties
from django.contrib.gis.gdal import DataSource



# Auto-generated `LayerMapping` dictionary for Kenya_counties model
kenya_counties_mapping = {
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'adm1_en': 'ADM1_EN',
    'date': 'date',
    'validon': 'validOn',
    'geom': 'POLYGON',
}


def import_data(verbose=True):
    file = os.getcwd() + "/Datasets/Counties.shp"
    data_source = DataSource(file)
    kenya_counties_layer = data_source[0].name
    
    kenya_counties_layermapping = LayerMapping(
        Kenya_counties, file, kenya_counties_mapping, layer = kenya_counties_layer
        )
    
    kenya_counties_layermapping.save(strict = True, verbose=verbose)