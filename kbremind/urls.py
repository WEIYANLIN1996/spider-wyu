from . import views
from django.conf.urls import url



urlpatterns = [
    url(r'^$', views.getkb_login),
    url(r'getkb', views.getkb_tj),
    url(r'remindkq', views.remindkq),
    url(r'remindgb', views.remindgb),

]