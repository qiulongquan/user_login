from django.urls import re_path
from . import views

app_name = 'login'


urlpatterns = [
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^login/(?P<pk>\d+)/profile/$', views.profile, name='profile'),
    re_path(r'^login/(?P<pk>\d+)/profile/update/$',
            views.profile_update,
            name='profile_update'),
    re_path(r'^login/(?P<pk>\d+)/pwd_change/$',
            views.pwd_change,
            name='pwd_change'),
    re_path(r"^logout/$", views.logout, name='logout'),
]
