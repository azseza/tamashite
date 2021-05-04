import Token

gateway1 = Token.gateway('config/gateway-1.json')
gateway2 = Token.gateway('config/gateway-2.json')
bank1 = Token.bank('config/bank-1.json')
bank2 = Token.bank('config/bank-2.json')


# Create alice member and link it to the alice's bank account.
alice_alias = 'ALICE' + Token.generate_id(10)
alice = Token.create_member(gateway1, alice_alias, 'aliceDevice', '123')
alice_access = bank1.create_access('alice', 'checking1', alice.public_key())
alice_account = alice.link_account(bank1.bank_code(), alice_access, "Alice's checking")
alice_account.info()

# Create bob member and link it to the bob's bank account.
bob_alias = 'BOB' + Token.generate_id(10)
bob = Token.create_member(gateway2, bob_alias, 'bobDevice', '321')
bob_access = bank2.create_access('bob', 'checking2', bob.public_key())
bob_account = bob.link_account(bank2.bank_code(), bob_access, "Bob's checking")

# Alice creates a Token and endorses it. Bob charges the token.
token = alice.create_payee_token(bob_alias, {'currency': 'EUR', 'singlePayment':{'amount':10}})
alice.endorse_token(token, alice_account)
bob_account.charge_token(token, 1, 'EUR', 'Python request')
alice_account.info()
