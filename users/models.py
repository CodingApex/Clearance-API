from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    # password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    userid = models.CharField(null=True, max_length=9)
    office = models.ForeignKey('ClearingOffice', models.DO_NOTHING, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Raw Model
class RegistrarViews(models.Model):
    cl_itemid = models.CharField(primary_key=True, max_length=20)
    office_id = models.CharField(max_length=50, blank=True, null=True)
    studid = models.CharField(max_length=9, blank=True, null=True)
    studfullname = models.CharField(max_length=100, blank=True, null=True)
    collcode = models.CharField(max_length=4, blank=True, null=True)
    resolve = models.BooleanField(blank=True, null=True)

    # last_itemid = Item.objects.all().order_by('itemid').last()
    # if not last_itemid:
    #     return courseSubject + semester + schoolyear + '00'
    #     # ex. engg-2-2023-00
def get_default_id(self):
    last_cl_itemid = ClearanceItem.objects.all().order_by('cl_itemid').last()
    if not last_cl_itemid:
        return 'CL-' + str(datetime.now().strftime('%Y%m%d-')) + '0000'
    item_id = last_cl_itemid.cl_itemid
    item_int = item_id[13:17]
    new_item_int = int(item_int) + 1
    new_item_id = 'CL-' + str(datetime.now().strftime('%Y%m%d-')) + str(new_item_int).zfill(4)
    return new_item_id

class ClearanceItem(models.Model):
    cl_itemid = models.CharField(primary_key=True, max_length=20, default=get_default_id)
    studid = models.CharField(max_length=9, blank=True, null=True)
    office = models.ForeignKey('ClearingOffice', models.DO_NOTHING, blank=True, null=True)
    sem = models.CharField(max_length=1, blank=True, null=True)
    sy = models.CharField(max_length=9, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    resolve = models.BooleanField(default='False', blank=True, null=True)
    resolve_date = models.DateField(blank=True, null=True)
    resolve_by = models.CharField(max_length=8, blank=True, null=True)
    recorded_by = models.CharField(max_length=8, blank=True, null=True)
    record_date = models.DateField(auto_now_add = True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clearance_item'

# class ClearanceItem(models.Model):
#     cl_itemid = models.CharField(primary_key=True, max_length=20, default=get_default_id)
#     studid = models.CharField(max_length=9, blank=True, null=True)
#     officeid = models.CharField(max_length=3, blank=True, null=True)
#     # officeid = models.ForeignKey('Office', models.DO_NOTHING, db_column='officeid', blank=True, null=True)
#     sem = models.CharField(max_length=1, blank=True, null=True)
#     sy = models.CharField(max_length=9, blank=True, null=True)
#     remarks = models.TextField(blank=True, null=True)
#     resolution = models.TextField(blank=True, null=True)
#     resolve = models.BooleanField(blank=True, null=True)
#     resolve_date = models.DateField(blank=True, null=True)
#     resolve_by = models.CharField(max_length=8, blank=True, null=True)
#     recorded_by = models.CharField(max_length=8, blank=True, null=True)
#     record_date = models.DateField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'clearance_item'

class ClearingOffice(models.Model):
    office = models.OneToOneField('Office', models.DO_NOTHING, primary_key=True)
    staff = models.TextField(blank=True, null=True)
    office_serial = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clearing_office'

class Office(models.Model):
    office_id = models.CharField(primary_key=True, max_length=50)
    office_name = models.CharField(max_length=200)
    office_head = models.CharField(max_length=8, blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    office_parent = models.CharField(max_length=50, blank=True, null=True)
    deptlogo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'office'

class TransactionLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    cl_itemid = models.ForeignKey('ClearanceItem', models.DO_NOTHING, db_column='cl_itemid', blank=True, null=True)
    trans_desc = models.TextField(blank=True, null=True)
    trans_recorded = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction_log'