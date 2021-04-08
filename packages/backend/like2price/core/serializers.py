import os
import requests
import json
from web3 import Web3, HTTPProvider
from web3.auto import w3
from hexbytes import HexBytes
from eth_account.messages import encode_defunct

from rest_framework import serializers
from django.http import Http404

from like2price.core.models import (
    Artist,
    Item,
    Sign,
)
from like2price.core.web3_config import config
from ipfs_utility.core import (
    create_item_folder,
    like,
    dislike,
    follow,
)

PROJECT_ID = os.environ['PROJECT_ID']
ROPSTEN_URL = "https://rinkeby.infura.io/v3/%s" % PROJECT_ID

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            '__all__'
        )


class ItemSignSerializer(serializers.Serializer):
    ipns = serializers.CharField()
    address = serializers.CharField()


class ItemSerializer(serializers.ModelSerializer):
    like_signs = serializers.SerializerMethodField()
    dislike_signs = serializers.SerializerMethodField()
    follower_signs = serializers.SerializerMethodField()
    token_uri = serializers.SerializerMethodField()
    owner = serializers.CharField(source='owner.wallet_address', default='')
    nft_name = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            '__all__'
        )
        read_only_fields = (
            'token_uri',
            'like_signs',
            'dislike_signs',
            'follower_signs',
            'owner',
        )

    def get_like_signs(self, obj):
        signs = Sign.objects.filter(item=obj, type='likes')
        if signs.exists():
            return ItemSignSerializer(signs, many=True).data
        return []

    def get_dislike_signs(self, obj):
        signs = Sign.objects.filter(item=obj, type='dislikes')
        if signs.exists():
            return ItemSignSerializer(signs, many=True).data
        return []

    def get_follower_signs(self, obj):
        signs = Sign.objects.filter(item=obj, type='followers')
        if signs.exists():
            return ItemSignSerializer(signs, many=True).data
        return []

    def get_token_uri(self, obj):
        try:
            web3 = Web3(HTTPProvider(ROPSTEN_URL))
            web3_config = {'address': obj.nft_address, 'abi': config['abi']}
            contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'])
            nft_id = obj.nft_id
            token_uri = contract_instance.functions.tokenURI(int(nft_id)).call()
        except Exception as e:
            print(e)
            token_uri = None
        return token_uri

    def get_nft_name(self, obj):
        try:
            web3 = Web3(HTTPProvider(ROPSTEN_URL))
            web3_config = {'address': obj.nft_address, 'abi': config['abi']}
            contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'])
            nft_id = obj.nft_id
            ipfs_url = contract_instance.functions.tokenMetadataURI(int(nft_id)).call()
            r = requests.get(ipfs_url).content
            nft_name = json.loads(r).get('name')
        except Exception as e:
            print(e)
            nft_name = '***'
        return nft_name

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
            wallet_address=validated_data.get('owner').get("wallet_address"))
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
        self.verify_sign(validated_data.get('address'),
                         validated_data.get('msg'),
                         validated_data.get('sig'))

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

    @classmethod
    def verify_sign(cls, address, msg, signature):
        assert isinstance(msg, dict), 'msg must be dict'
        msg_escaped = json.dumps(msg).replace(' ', '')
        message = encode_defunct(text=msg_escaped)
        signature_bytes = HexBytes(signature)
        recovered_addr = w3.eth.account.recover_message(
            message, signature=signature_bytes)
        if recovered_addr != address:
            raise serializers.ValidationError('Recovered address not match')


class PriceSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    price = serializers.FloatField()


class NftToItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()