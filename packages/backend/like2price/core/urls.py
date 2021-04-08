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

route.register(r'api/items', ItemViewSet)
route.register(r'api/artists', ArtistViewSet)
route.register(r'api/signs', SignViewSet)
route.register(r'api/price', PriceViewSet)
urlpatterns = [
    path(r'', include(route.urls)),
]
