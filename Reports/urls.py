from django.conf.urls import url
from Reports import views

urlpatterns = [
    url(r'^index$'              , views.index             ,name='index'),
    url(r'^CustomerOrderStatus$'              , views.CustomerOrderStatus,name='CustomerOrderStatus'),
]


