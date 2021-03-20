from rest_framework import routers
from django.conf.urls import include
from django.urls import path

route = routers.SimpleRouter()
route.trailing_slash = ''

urlpatterns = [
    path(r'', include('like2price.core.urls')),
    path('', include(route.urls)),
]
