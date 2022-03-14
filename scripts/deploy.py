from brownie import FundMe, config, network, MockV3Aggregator
from eth_utils import to_wei
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    set_account,
    deploy_mocks,
)


def deploy_fund_me():
    account = set_account()

    # Tenemos que separar los casos segun la red a la que nos conectamos
    # Si la red a la que nos conectamos es red real, usamos el price_feed que pusimos en el config

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        print(price_feed_address)

        # En cambio si la red a la que nos conectamos es una development network, usamos el MockV3Aggregator para simular el price_feed
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
