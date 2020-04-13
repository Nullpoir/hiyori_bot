from django.conf.urls import url
from . import views
from django.urls import path,include,reverse_lazy

urlpatterns = [
    path('',views.TwitterEndPointView.as_view(),name="TwitterEndPoint"),
]
