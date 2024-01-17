import sys
from web3 import Web3
from dotenv import load_dotenv
import ipfshttpclient
import json
import requests
import os


load_dotenv()
IPFS_HOST = os.getenv('IPFS_HOST')
BLOCK_CHAIN_IP = os.getenv('BLOCK_CHAIN_IP')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')
ACCOUNT_ADDRESS = Web3.to_checksum_address(str(ACCOUNT_ADDRESS))


###### INITIALIZE THE CONNECTIONS TO THE SERVICES AND CONTRACTS INVOLVED ######

web3 = Web3(Web3.HTTPProvider(f"http://{BLOCK_CHAIN_IP}:8545"))                    # BLOCKCHAIN
response = requests.get(f'http://{IPFS_HOST}:6001/ipfs_portal_contracts')
data = response.json()
ipfs_json = data['portal_contracts']


nft_abi = ipfs_json['nft_abi']             
nft_address = ipfs_json['nft_address']
marketplace_abi = ipfs_json['marketplace_abi']
marketplace_address = ipfs_json['marketplace_address']


nft = web3.eth.contract(address=nft_address, abi=nft_abi)                           # NFT contract
marketplace = web3.eth.contract(address=marketplace_address, 
                                    abi=marketplace_abi)                            # Marketplace contract





def getPurchases():
    # Retrieves the account's purchases and returns them in a list
    if (ACCOUNT_ADDRESS):

        client = ipfshttpclient.connect(f"/ip4/{IPFS_HOST}/tcp/5001")                       # IPFS

        results = marketplace.caller({'from': ACCOUNT_ADDRESS}).getMyNfts()
        purchases=[]

        for r in results:
            token_id = r[1]
            content_hash = nft.functions.tokenURI(token_id).call()
            metadata_hash = r[5]

            

            metadata = client.cat(metadata_hash)
            metadata = metadata.decode("UTF-8")
            metadata = json.loads(json.loads(metadata))

            purchases.append({'contentURI': content_hash, 'title':metadata['title']})

        client.close()

        return purchases


def getDevices():
    results = marketplace.caller({'from': ACCOUNT_ADDRESS}).getMyDevices()
    devices = []

    client = ipfshttpclient.connect(f"/ip4/{IPFS_HOST}/tcp/5001")  

    for r in results:
        token_id = r[1]
        content_hash = nft.functions.tokenURI(token_id).call()

        content = client.cat(content_hash)
        content = content.decode("UTF-8")
        content = json.loads(content)
        
        devices.append({'name': content['name'], 'endpoint':content['device_endpoint'][7:]})
    
    client.close()
    
    return devices



def list_items():

    purchases = getPurchases()


    print("\nOwned algorithms")
    print("---------------------------------")
    i=1
    if(purchases):
        for purchase in purchases:
            print(str(i) + ") " + purchase['title'])
            i+=1
    
    else:
        print("You have not bought any items from the marketplace yet.")



def list_devices():

    devices = getDevices()

    print("\nOwned devices")
    print("---------------------------------")
    i=1
    if(devices):
        for device in devices:
            print(str(i) + ") " + device['name'] + " | " + device['endpoint'])
            i+=1
    
    else:
        print("You have not bought any items from the marketplace yet.")




# def register_devices():
#     # Retrieves the names and URLs of all the devices participating in the user's joined DAOs
#     daoStorage_contract = web3.eth.contract(address=DAO_STORAGE_ADDRESS, abi=daoStorage_abi)
#     daos_joined = daoStorage_contract.functions.getStoredHashes().call()


#     if(daos_joined):
#         client = ipfshttpclient.connect(f"/ip4/{IPFS_HOST}/tcp/5001")                       # IPFS
        
#         for dao_hash in daos_joined:
#             dao_info = client.cat(dao_hash)
#             dao_info = dao_info.decode("UTF-8")
#             dao_info = json.loads(dao_info)

#             print("Devices participating in " + dao_info['dao_name'] + ":")
#             for device in dao_info['devices']:
#                 status = ''
#                 try:
#                     response = requests.get('{}/register'.format(device['endpoint']))
#                     status = "ONLINE"
#                 except requests.exceptions.RequestException:
#                     status = "OFFLINE"

#                 print(device['device_name'], device['endpoint'][7:],status)
                    
#         client.close()

#     else:
#         print("You have not joined any DAOs yet.")


def deploy(algo_title:str):

    purchases = getPurchases()
    devices = getDevices()
    found = False
    for purchase in purchases:
        if found:
            break

        if(purchase['title']==algo_title):
            found = True
            algo_hash = purchase['contentURI']

            client = ipfshttpclient.connect(f"/ip4/{IPFS_HOST}/tcp/5001")                       # IPFS

            for device in devices:
                response = requests.post("http://{}/deploy_algorithm".format(device['endpoint']), json = {'algorithm_hash': algo_hash, 'algorithm_name':algo_title})                 

            client.close()
            

    if not found:
        print("The file you requested was not found in your purchases.")



def deploy_file(file_name:str):
    devices = getDevices()
    file = open(file_name,"rb")

    for device in devices:
        response= requests.post("http://{}/deploy_file".format(device['endpoint']), files={'file': file})                 
        print(response.text)
    
    file.close()
