import os
import sys
import unittest
import dotenv

from unittest import mock

PROGRAM_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(PROGRAM_PATH))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

dotenv.read_dotenv(os.path.join(BASE_DIR, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'like2price.settings')
import django
django.setup()


from ipfs_utility.core import like, dislike, create_item_folder, follow, IPFS


class IPFSTestCase(unittest.TestCase):

    def test_add(self):
        _hash = IPFS.add({
            "address": "123",
            "msg": {"123": 56},
            "sig": "123444rr",
            "version": "1"
        }, f'/2222/likes/test2')

        print(_hash)

        ipns = IPFS.get_ipns(_hash)
        print(ipns)


if __name__ == '__main__':
    unittest.main()
    # folder_ipns = create_item_folder('2222')
    # print('folder_ipns', folder_ipns)