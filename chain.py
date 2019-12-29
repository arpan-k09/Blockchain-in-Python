#import functools for reduce function in get_balance function
import hashlib
import json
import collections
import pickle


import hash_val as hb

open_transactions= []
owner = "Ashish"
genesis_block = {
    'previous_hash': '',
    'index':0,
    'transactions':[],
    'proof' : 100
}
blockchain = [genesis_block]
participants = {'Ashish'}
MINING_REWARD = 10
#
# def hash_block(block):
#     #return '-'.join([str(block[key]) for key in block])
#     '''JSON converts dictionary to string and for hash fun we need string(in binary form) dumps is
#     method of json package and convert it into a binary formate by encode method '''
#     return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

def load_data():
    with open('data.txt',mode='r') as fd:
        #file_cont = pickle.loads(fd.read())
        file_cont = fd.readlines()
        global blockchain
        global open_transactions

        # blockchain = file_cont['chain']
        # open_transactions = file_cont['open_tran']

        blockchain = json.loads(file_cont[0][:-1])
        updated_blockchain = []
        for block in blockchain:
            updated_block = {
                'previous_hash': block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [collections.OrderedDict([('sender',tx['sender']),
                                                          ('recipient',tx['recipient']),
                                                          ('amount',tx['amount'])]) for tx in block['transactions']]
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain

        updated_transactions = []
        open_transactions = json.loads(file_cont[1])
        for tx in open_transactions:
            updated_transaction = collections.OrderedDict([('sender',tx['sender']),
                                                          ('recipient',tx['recipient']),
                                                          ('amount',tx['amount'])])
            updated_transactions.append(updated_transaction)

        open_transactions = updated_transactions


load_data()


def store_data():
    with open('data.txt',mode='w') as fd:
        # fd.write(str(blockchain))
        fd.write(json.dumps(blockchain))
        fd.write('\n')
        fd.write(json.dumps(open_transactions))
        # store_data = {
        #     'chain':blockchain,
        #     'open_tran':open_transactions
        # }
        # fd.write(pickle.dumps(store_data))


def valid_proof(transaction , last_hash, proof):
    guess = (str(transaction) + str(last_hash) + str(proof)).encode()
    gusse_hash = hb.hash_str_256(guess)
    print(gusse_hash)
    return gusse_hash[0:2] == '0f'

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hb.hash_block(last_block)
    proof = 0
    print("Open : - ",open_transactions)
    while not valid_proof(open_transactions,last_hash,proof):
        proof += 1
    return proof

def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant]for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender']==participant]
    tx_sender.append(open_tx_sender)
    #amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + tx_amt[0] if len(tx_amt) > 0 else tx_sum + 0, tx_sender,0)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += sum(tx)
    #tx_sender = 0
    tx_recipient = 0

    # for block in blockchain:
    #     for tx in block['transactions']:
    #         if tx['sender'] == participant:
    #             tx_sender += tx['amount']

    # amount_recieve = functools.reduce(lambda tx_sum, tx_amt: tx_sum + tx_amt[0] if len(tx_amt) > 0 else tx_sum + 0, tx_recipient,0)
    amount_recieve = 0
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_recieve += sum(tx)
    # for block in blockchain:
    #     for tx in block['transactions']:
    #         if tx['recipient'] == participant:
    #             tx_recipient += tx['amount']

    return amount_recieve - amount_sent

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

def add_value(recipient,sender = owner,amount = 1.0):

    """Appends the new transaction value in the given blockchain......"""
    # if last_value == None:
    #     last_value = [1]
    # blockchain.append([last_value,transaction_value])
    # transaction = {
    #     'sender':sender,
    #     'recipient':recipient,
    #     'amount':amount
    # }
    transaction = collections.OrderedDict([('sender',sender),('recipient',recipient),('amount',amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        store_data()
        #Participants var is for maintaining the list of uses in transactions
        return True
    return False

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])

def mine_block():

    last_block = blockchain[-1]
    #At above we're adding genesis_block for the initial value for last_block unless we can get error.

    hashed_block = hb.hash_block(last_block)

    #print(hashed_block)

    proof = proof_of_work()

    # reward_transaction = {
    #     'sender':"MINING",
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = collections.OrderedDict([('sender', "MINING"), ('recipient', owner), ('amount', MINING_REWARD)])

    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    #open_transactions.append(reward_transaction)
    #print(hashed_block)
    # for key in last_block:
    #     value = last_block[key]
    #     hash_block += str(value)
    # print(hash_block)
    block = {
        'previous_hash': hashed_block,
        'index':len(blockchain),
        'transactions':copied_transaction,
        'proof' : proof
    }
    blockchain.append(block)
    #store_data()
    return True

def input_value():

    """Getting input for the new transaction..........."""
    #BECUASE AT ABOVE WE WERE SET SENDER NAME AS ASHISH BY DEFAULT
    #tx_sender = input("Enter sender name : - ")
    tx_recipient = input("Enter recipient name : - ")
    tx_amount = float(input("Enter the transaction value : - "))
    return tx_recipient,tx_amount


def get_user_choice():
    return input("Enter you choice : -")

def print_blockchain_value():
    # print(blockchain)
    for block in blockchain:
        print(block)

    #print(blockchain)
    # else:
    #     print("-"*50)

def get_last_value():

    """Returns the last value from the given blockchain list.........."""
    if len(blockchain)<1:
        return None
    return blockchain[-1]

def verify_chain():
    for (index,block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hb.hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block['transactions'][:-1],block['previous_hash'],block['proof']):
            print('Proof of work is invalid !!!!!!!!!!!!')
            return False
    return True

waiting_for_input = True

while waiting_for_input:
    print("\n\n\nPlease choose")
    print("1 : Add new transaction value")
    print("2 : Mine a new block")
    print("3 : Output the blockchain blocks")
    print("4 : Output for participants")
    print("5 : Transaction Validity")
    print("h : hack")
    #print("v : Verify the blockchain")
    print("q : For exit")
    user_choice = get_user_choice()

    #verify_chain()
    if user_choice == "1":
        #tx_data = input_value()
        recipient,amount = input_value()
        if add_value(recipient,amount=amount):
            print("Added transaction")
        else:
            print("Transaction Failed")
        print(open_transactions)

    #elif user_choice == "v":
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            store_data()
    elif user_choice == "3":
        print_blockchain_value()

    elif user_choice == "4":
        print(participants)

    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transaction")
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index':0,
                'transactions':[{'sender':'Arpan','recipient':'korat','amount':100.0,'proof':1}]
            }

    elif user_choice == "q":
        waiting_for_input = False

    else:
        print("Wrong input")
    if not verify_chain():
        print("Invalid Blockchain!!!!!!!!!!!")
        waiting_for_input = False

    print("Balance of {}: {:10.2f}".format('Ashish',get_balance('Ashish')))

else:
    print("User left !!!!!!!!")