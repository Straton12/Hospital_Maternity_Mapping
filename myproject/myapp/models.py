from django.contrib.gis.db import models

class KenyaSubcounty(models.Model):
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    adm2_en = models.CharField(max_length=50)
    adm1_en = models.CharField(max_length=50)
    date = models.DateField()
    validon = models.DateField()
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        verbose_name_plural = "Kenya Subcounties"

class KenyaCountry(models.Model):
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    adm0_en = models.CharField(max_length=50)
    date = models.DateField()
    validon = models.DateField()
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        verbose_name_plural = "Kenya Country"

class KenyaCounty(models.Model):
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    adm1_en = models.CharField(max_length=50)
    date = models.DateField()
    validon = models.DateField()
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        verbose_name_plural = "Kenya Counties"
        
class Hospitals(models.Model):
    facility = models.CharField(max_length=254)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    accuracy = models.FloatField()
    kmfl_new = models.CharField(max_length=254)
    kmfl = models.CharField(max_length=254)
    nn_field = models.BigIntegerField()
    county = models.CharField(max_length=254)
    constituen = models.CharField(max_length=254, null=True, blank=True)
    sub_county = models.CharField(max_length=254, null=True, blank=True)
    ward = models.CharField(max_length=254, null=True, blank=True)
    keph_level = models.CharField(max_length=254)
    ownership = models.CharField(max_length=254)
    qq2 = models.CharField(max_length=254)
    q2 = models.CharField(max_length=254)
    qq3 = models.CharField(max_length=254)
    geom = models.PointField(srid=4326)
    
    class Meta:
        verbose_name_plural = "Hospitals"
        
class level4_buffer(models.Model):
    distance = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    
    class Meta:
        verbose_name_plural = "Level 4 Buffer"
        
class level5_buffer(models.Model):
    distance = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    
    class Meta:
        verbose_name_plural = "Level 5 Buffer"