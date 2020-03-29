from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views
from pricecheck.views import AlertDeleteView,activate

activate()

urlpatterns = [
    path('', views.home, name='Price-Home'),
    path('about/', views.about, name='Price-About'),
    path('users/', views.users, name='Price-users'),
    url(r'^(?P<pk>\d+)/delete', AlertDeleteView.as_view(), name='delete'),
    url(r'^register/$', views.register,name='register'),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'^login/$',views.user_login,name='login'),
]