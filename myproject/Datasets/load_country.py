import os
from django.contrib.gis.utils import LayerMapping
from myapp.models import Kenya_coutry
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
        Kenya_coutry, file, kenya_coutry_mapping, layer = kenya_counties_layer
        )
    
    kenya_counties_layermapping.save(strict = True, verbose=verbose)