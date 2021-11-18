from django.conf.urls import url
from Reports import views

urlpatterns = [
    url(r'^index$'              , views.index               ,name='index'),
    url(r'^CustomerOrderStatus$', views.CustomerOrderStatus ,name='CustomerOrderStatus'),
    url(r'^SeasonsProblem$'     , views.SeasonsProblem      ,name='SeasonsProblem'),
    url(r'^DetectingChange$'    , views.DetectingChange     ,name='DetectingChange'),
]


