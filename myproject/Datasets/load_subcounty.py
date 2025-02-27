import os
from django.contrib.gis.utils import LayerMapping
from myapp.models import Kenya_subcounty
from django.contrib.gis.gdal import DataSource



# Auto-generated `LayerMapping` dictionary for Kenya_subcounty model
kenya_subcounty_mapping = {
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'adm2_en': 'ADM2_EN',
    'adm1_en': 'ADM1_EN',
    'date': 'date',
    'validon': 'validOn',
    'geom': 'POLYGON',
}


def import_data(verbose=True):
    file = os.getcwd() + "/Datasets/Sub_county.shp"
    data_source = DataSource(file)
    kenya_subcounty_layer = data_source[0].name
    
    kenya_subcounty_layermapping = LayerMapping(
        Kenya_subcounty, file, kenya_subcounty_mapping, layer = kenya_subcounty_layer
        )
    
    kenya_subcounty_layermapping.save(strict = True, verbose=verbose)