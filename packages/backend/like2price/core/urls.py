from django.urls import path, include
from rest_framework import routers


from like2price.core.views import (
    ItemViewSet,
    ArtistViewSet,
    SignViewSet,
    PriceViewSet,
)

route = routers.SimpleRouter()
route.trailing_slash = ''

route.register(r'v1/items', ItemViewSet)
route.register(r'v1/artists', ArtistViewSet)
route.register(r'v1/signs', SignViewSet)
route.register(r'v1/price', PriceViewSet)
urlpatterns = [
    path(r'', include(route.urls)),
]
