from django.core.management.base import BaseCommand
import requests
from web3.main import Web3
from djsniper.sniper.models import NFTProject, NFT, NFTAttribute, NFTTrait

# https://polygon-mumbai.infura.io/v3/455905f17d0844778fff85d926a530e5

#INFURA_PROJECT_ID = "455905f17d0844778fff85d926a530e5"
#INFURA_ENDPOINT = f"https://goerli.infura.io/v3/{INFURA_PROJECT_ID}"

INFURA_ENDPOINT = f"https://polygon-mumbai.g.alchemy.com/v2/qg82ocbBhqeF4CalJF9ZHHAFLn7SdK1U"


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fetch_nfts(1)

    def fetch_nfts(self, project_id):
        project = NFTProject.objects.get(id=project_id)

        w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))
        contract_instance = w3.eth.contract(
            address=project.contract_address, abi=project.contract_abi
        )

        # Hardcoding only 10 NFTs otherwise it takes long
        for i in range(0, 5):
            ipfs_uri = contract_instance.functions.tokenURI(i).call()
            data = requests.get(
                f"https://ipfs.io/ipfs/{ipfs_uri.split('ipfs://')[1]}"
            ).json()
            nft = NFT.objects.create(
                nft_id=i, project=project#, image=data["image"].split("ipfs://")[1]
            )
            attributes = data["attributes"]
            for attribute in attributes:
                nft_attribute, created = NFTAttribute.objects.get_or_create(
                    project=project,
                    name=attribute["trait_type"],
                    value=attribute["value"],
                )
                NFTTrait.objects.create(nft=nft) #, attribute=nft_attribute)
