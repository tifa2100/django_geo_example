from django.contrib.gis.db import models

class PointsCore(models.Model):
    store_code = models.IntegerField(db_column='StoreCode')
    district_id = models.IntegerField(db_column='District',default=0)
    auto_id = models.IntegerField(db_column='AutoID',default=0)
    block_num = models.IntegerField(db_column='Block',default=0)
    done = models.BooleanField(db_column='Done',default=0)
    governorate_id = models.IntegerField(db_column='Governerate',default=0)
    district_name = models.CharField(db_column='DisName',max_length=30,default='')
    added_time = models.DateTimeField(db_column='addedTime',auto_now_add=True)
    added_by = models.IntegerField(db_column='pointAdder',default=1)
    modified_time = models.DateTimeField(db_column='editTime',auto_now_add=True)
    modified_by = models.IntegerField(db_column='editPerson',default=1)
    guid = models.CharField(db_column='guid',max_length=15,default='')

    point_location = models.PointField(srid=4326,db_column='geom')

class PointsExtra(models.Model):
    pass
