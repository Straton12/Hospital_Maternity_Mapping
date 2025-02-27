import os
from django.contrib.gis.utils import LayerMapping
from myapp.models import Hospitals
from django.contrib.gis.gdal import DataSource



# Auto-generated `LayerMapping` dictionary for Kenya_subcounty model
hospitals_mapping = {
    'facility': 'facility',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'altitude': 'altitude',
    'accuracy': 'accuracy',
    'kmfl_new': 'kmfl_new',
    'kmfl': 'kmfl',
    'nn_field': 'nn_',
    'county': 'county',
    'constituen': 'constituen',
    'sub_county': 'sub_county',
    'ward': 'ward',
    'keph_level': 'keph_level',
    'ownership': 'Ownership',
    'qq2': 'QQ2',
    'q2': 'Q2',
    'qq3': 'QQ3',
    'geom': 'POINT25D',
}

def import_data(verbose=True):
    file = os.getcwd() + "/Datasets/Hospitals.shp"
    data_source = DataSource(file)
    kenya_hospitals_layer = data_source[0].name
    
    kenya_hospitals_layermapping = LayerMapping(
        Hospitals, file, hospitals_mapping, layer = kenya_hospitals_layer
        )
    
    kenya_hospitals_layermapping.save(strict = True, verbose=verbose)