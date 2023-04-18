from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import ClearanceItem, TransactionLog, ClearingOffice
from django.utils import timezone
from datetime import datetime
from django.db.models import F

@receiver(post_save, sender=ClearanceItem)
def create_transaction_log(sender, instance, created, **kwargs):
    if created:
      TransactionLog.objects.create(cl_itemid=ClearanceItem.objects.get(cl_itemid=instance.cl_itemid),
         trans_desc="Add Clearance Item",
         trans_recorded=str(datetime.now().strftime('%Y-%m-%d')))
      ClearingOffice.objects.filter(office_id=instance.office).update(office_serial=F('office_serial') + 1)