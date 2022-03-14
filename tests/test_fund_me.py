import pytest
from scripts.helpful_scripts import set_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import accounts, network, exceptions


# En el comando de entrance_fee practicamente con el objeto contrato que creamos, vamos a entrar en una de las properties del contrato en solidity es como entrar dos niveles dentro de un contrato.

# Recordar que cuando usamos fund o queremos hacer una transaction, tenemos que poner los inputs dentro de las llaves.


def test_can_fund_and_withdraw():
    account = set_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    bad_actor = accounts.add()
    fund_me = deploy_fund_me()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
