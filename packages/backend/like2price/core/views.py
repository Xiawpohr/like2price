from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from like2price.core.models import (
    Artist,
    Item,
    Sign,
)
from like2price.core.serializers import (
    ArtistSerializer,
    ItemSerializer,
    CreateItemSerializer,
    CreateSignSerializer,
    PriceSerializer,
    NftToItemSerializer,
)

from like2price.pricing_models.train_model import predict


class ArtistViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    authentication_classes = ()
    permission_classes = ()


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        try:
            self.serializer_class = CreateItemSerializer
            response = super().create(request, *args, **kwargs)
            return response
        except Exception as e:
            print(e)
            return Response({
                'success': False,
                'msg': 'Create NFT failed.'
            }, status=status.HTTP_400_BAD_REQUEST)

    # [GET] /api/items/id?ntf_id={ntf_id}
    @action(detail=False, methods=['GET'])
    def id(self, request):
        params = self.request.query_params
        nft_id = params.get('nft_id')
        item = self.get_queryset().filter(nft_id=nft_id)
        if item.exists():
            item = item[0]
        else:
            return Response({
                'success': False,
                'msg': 'nft_id not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = NftToItemSerializer(item)
        return Response(serializer.data)


class SignViewSet(viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Sign.objects.all()
    serializer_class = CreateSignSerializer
    authentication_classes = ()
    permission_classes = ()


class PriceViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = PriceSerializer
    authentication_classes = ()
    permission_classes = ()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = dict()
        data["id"] = instance.id
        data["price"] = predict(
            instance.likes, instance.dislikes, instance.followers)
        serializers = self.get_serializer(data)
        return Response(serializers.data)
