import ipfshttpclient

# Share TCP connections using a context manager
with ipfshttpclient.connect() as client:
    pass
    # print(client.name.resolve('12D3KooWEqnTdgqHnkkwarSrJjeMP2ZJiADWLYADaNvUb6SQNyPF'))
    # print(client.ls('/ipfs/QmSfSEXrkYzsLz4adKJzVe9zj8dT8V6X9rkXdXCenV35pQ'))
