
from rest_framework import serializers
from django.http import Http404

from like2price.core.models import (
    Artist,
    Item,
    Sign,
)


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            '__all__'
        )


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            '__all__'
        )


class CreateItemSerializer(serializers.ModelSerializer):
    nft_id = serializers.CharField()
    nft_address = serializers.CharField()
    wallet_address = serializers.CharField(
        source='owner.wallet_address', write_only=True)

    class Meta:
        model = Item
        fields = (
            '__all__'
        )
        read_only_fields = (
            "owner",
            "ipns",
        )

    def create(self, validated_data):
        if not validated_data.get('owner'):
            raise Http404('wallet_address not exists.')

        artist, _ = Artist.objects.get_or_create(
            wallet_address=validated_data.get('owner'))
        validated_data["owner"] = artist
        # TODO: get ipns
        # validated_data["ipns"] = "xxx"
        return super().create(validated_data)


class CreateSignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sign
        fields = (
            '__all__'
        )
        read_only_fields = (
            "ipns",
        )

    def create(self, validated_data):
        sign_type = validated_data.get('type')
        item = validated_data.get("item")
        if sign_type == "likes":
            item.likes += 1
        elif sign_type == "dislikes":
            item.dislikes += 1
        elif sign_type == "followers":
            item.followers += 1
        item.save()
        # TODO: add ipns's type to IPFS
        return super().create(validated_data)


class PriceSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    price = serializers.FloatField()
