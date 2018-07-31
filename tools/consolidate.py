from bitcash import PrivateKeyTestnet

import gcl_secrets

FEE_AMOUNT = 20000

initiator_key = PrivateKeyTestnet(gcl_secrets.INITIATOR_PRIVATE_KEY)

balance = int(initiator_key.get_balance('satoshi'))
print(initiator_key.get_unspents())
to_send_amt = balance - FEE_AMOUNT
print(balance)
print(to_send_amt)

send_to = [
    (initiator_key.address, to_send_amt, 'satoshi')
]
# initiator_key.send(send_to, fee=1, )