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
from myapp.models import KenyaCounty
from django.contrib.gis.gdal import DataSource

kenya_counties_mapping = {
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'adm1_en': 'ADM1_EN',
    'date': 'date',
    'validon': 'validOn',
    'geom': 'POLYGON',
}

def import_data(verbose=True):
    print("Starting import process...")

    file = os.getcwd() + "/Datasets/Counties.shp"

    if not os.path.exists(file):
        print(f"File not found: {file}")
        return

    print(f"Loading data from: {file}")

    data_source = DataSource(file)
    kenya_counties_layer = data_source[0].name
    print(f"Detected layer: {kenya_counties_layer}")

    kenya_counties_layermapping = LayerMapping(
        KenyaCounty, file, kenya_counties_mapping, layer=kenya_counties_layer
    )

    kenya_counties_layermapping.save(strict=True, verbose=verbose)
    print("Data import complete.")

# Run the import function
import_data()
