from django.db import models


class customer_ord_lines(models.Model):
    order_number    = models.CharField(max_length=10)
    item_name       = models.CharField(max_length=50)
    status          = models.CharField(max_length=10)
    def getData(self):
        return dict(order_number= self.order_number,
                    item_name   = self.item_name,
                    status      = self.status)


class customer_orders(models.Model):
    ord_id          = models.CharField(max_length=20)
    ord_dt          = models.DateField()
    qt_ordd         = models.IntegerField()

class weather(models.Model):
    date            = models.DateField()
    was_rainy       = models.BooleanField()
    def getData(self):
        return dict(date=self.date, was_rainy=self.was_rainy)


