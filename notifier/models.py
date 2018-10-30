from django.db import models
import uuid
from django.db.models.functions import TruncHour
from django.db.models import Avg, Count, Sum, Max
from datetime import datetime, timedelta

# Create your models here.


class OutletModel(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=4096)
    last_checked = models.DateTimeField(null=True, blank=True)

    def get_stock_count(self):
        return self.stockhistory_set.order_by('-timestamp').first()

    #TODO: optimise this -- so many queries being issued due to ORM.
    def get_stock_history(self):
        return ",".join([str(x.stock_count) for x in self.stockhistory_set.order_by('-timestamp')[:100]])

    def get_hourly_history(self):
        return self.stockhistory_set.filter(timestamp__gte=datetime.now()-timedelta(days=7)).annotate(hour=TruncHour('timestamp')).values('hour').annotate(a=Avg('stock_count')).order_by('hour')

    def last_added(self):
        try:
            return StockHistory.objects.raw("SELECT * FROM (SELECT *, lead(stock_count) OVER (ORDER BY timestamp DESC) sclag, stock_count - lead(stock_count) OVER (ORDER BY timestamp DESC) as diff FROM notifier_stockhistory WHERE model_id=%s) as sc WHERE diff > 0 ORDER BY timestamp ASC LIMIT 1;", [self.id])[0]
        except IndexError:
            return self.stockhistory_set.order_by('timestamp').first()

    #TODO: this shouldn't be on the model...
    def get_color(self):
        recent = self.stockhistory_set.order_by('timestamp')[:2]

        if len(recent) < 2 or recent[0].stock_count == recent[1].stock_count:
            return "#999999"

        if recent[0].stock_count > recent[1].stock_count:
            return "#00FF00"
        else:
            return "#FF0000"

    def __str__(self):
        return self.name


class StockHistory(models.Model):
    stock_count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    model = models.ForeignKey('OutletModel', on_delete="cascade")

    def __str__(self):
        return "{}: {} @ {}".format(self.model.name, self.stock_count, self.timestamp)


class NotificationRequest(models.Model):
    uuid = models.UUIDField(null=True, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    model = models.ForeignKey('OutletModel', on_delete="cascade")
    sent = models.DateTimeField(blank=True, null=True)
    visited = models.IntegerField(default=0)

    def __str__(self):
        return "{} for {}".format(self.model, self.email)
