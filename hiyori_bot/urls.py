from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('twitter/',include("app.urls")),
    path('',views.IndexView.as_view())
]
