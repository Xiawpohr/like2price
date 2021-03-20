import json
import requests

from urllib.parse import quote

from like2price.core.models import Sign


IPFS_CLUSTER_HOST = 'http://localhost:5001/api/v0'

class IPFS():
    urls = {
        'add': f'{IPFS_CLUSTER_HOST}/add',
        'mkdir': f'{IPFS_CLUSTER_HOST}/files/mkdir',
        'stat': f'{IPFS_CLUSTER_HOST}/files/stat',
        'cp': f'{IPFS_CLUSTER_HOST}/files/cp',
        'publish': f'{IPFS_CLUSTER_HOST}/name/publish'
    }

    @classmethod
    def create_folder(cls, path):
        try:
            url = cls.urls.get('mkdir')
            if url:
                response = requests.post(url, params={
                    'arg': path
                })

            url = cls.urls.get('stat')
            response = requests.post(url, params={
                'arg': path
            })

            return response.json()['Hash']

        except json.decoder.JSONDecodeError:
            print(">>>err")
            return {}

    @classmethod
    def get_ipns(cls, hash_address):
        url = cls.urls.get('publish')
        try:
            response = requests.post(url, params={
                'arg': f'/ipfs/{hash_address}',
                'allow-offline': True
            })

            return response.json()['Name']

        except json.decoder.JSONDecodeError:
            print(">>>err")
            return {}

    @classmethod
    def add(cls, data, filepath):
        try:
            _, filename = filepath.split(filepath)

            add_url = cls.urls.get('add')
            response = requests.post(f'{add_url}/', files={
                f'{filename}': json.dumps(data)
            })

            file_hash = response.json()['Hash']
            ipfs_file_hash = quote(f'/ipfs/{file_hash}', safe='')

            filepath = quote(filepath, safe='')

            cp_url = cls.urls.get('cp')
            response = requests.post(f'{cp_url}?arg={ipfs_file_hash}&arg={filepath}')

            return file_hash

        except json.decoder.JSONDecodeError:
            return {}


def create_item_folder(nft_address, nft_id=None, item_id=None):
    nft_folder_hash = IPFS.create_folder(f'/{nft_address}')
    IPFS.create_folder(f'/{nft_address}/likes')
    IPFS.create_folder(f'/{nft_address}/unlikes')
    IPFS.create_folder(f'/{nft_address}/followers')

    ipns = IPFS.get_ipns(nft_folder_hash)
    return ipns


def get_sign(sign_id):
    try:
        sign = Sign.objects.get(id=sign_id)
        return sign
    except Sign.DoesNotExist:
        return None


def serialize_sign(sign):
    return {
        'address': sign.address,
        'msg': sign.msg,
        'sig': sign.sig,
        'version': sign.version
    }


def like(sign_id):
    sign = get_sign(sign_id)
    data = serialize_sign(sign)
    _hash = IPFS.add(data, f'/{sign.item.nft_address}/likes/{sign.address}')
    ipns = IPFS.get_ipns(_hash)
    return ipns


def dislike(sign_id):
    sign = get_sign(sign_id)
    data = serialize_sign(sign)
    _hash = IPFS.add(data, f'/{sign.item.nft_address}/dislikes/{sign.address}')
    ipns = IPFS.get_ipns(_hash)
    return ipns


def follow(sign_id):
    sign = get_sign(sign_id)
    data = serialize_sign(sign)
    _hash = IPFS.add(data, f'/{sign.item.nft_address}/followers/{sign.address}')
    ipns = IPFS.get_ipns(_hash)
    return ipns
