
from rest_framework import serializers
from django.http import Http404

from like2price.core.models import (
    Artist,
    Item,
    Sign,
)
from ipfs_utility.core import (
    create_item_folder,
    like,
    dislike,
    follow,
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
        item_instance = super().create(validated_data)
        ipns = create_item_folder(validated_data["nft_address"])
        try:
            item_instance.ipns = ipns
            item_instance.save()
        except Exception as e:
            print(e)
        return item_instance


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
        response = super().create(validated_data)
        sign_instance = response
        try:
            if sign_type == "likes":
                item.likes += 1
                sign_instance.ipns = like(sign_instance.id, publish=True)
            elif sign_type == "dislikes":
                item.dislikes += 1
                sign_instance.ipns = dislike(sign_instance.id, publish=True)
            elif sign_type == "followers":
                item.followers += 1
                sign_instance.ipns = follow(sign_instance.id, publish=True)
            sign_instance.save()
        except Exception as e:
            print(e)
        item.save()
        return sign_instance

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        ret['username'] = ret['username'].lower()
        return ret


class PriceSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    price = serializers.FloatField()
