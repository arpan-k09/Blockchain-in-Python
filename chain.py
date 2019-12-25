open_transactions= []
owner = "Ashish"
genesis_block = {
    'previous_hash': '',
    'index':0,
    'transactions':[]
}
blockchain = [genesis_block]
participants = {'Ashish'}
MINING_REWARD = 10

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant]for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender']==participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    #tx_sender = 0
    tx_recipient = 0

    # for block in blockchain:
    #     for tx in block['transactions']:
    #         if tx['sender'] == participant:
    #             tx_sender += tx['amount']

    amount_recieve = 0
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_recieve += tx[0]
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
    transaction = {
        'sender':sender,
        'recipient':recipient,
        'amount':amount
    }

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        #Participants var is for maintaining the list of uses in transactions
        return True
    return False

def mine_block():

    last_block = blockchain[-1]
    #At above we're adding genesis_block for the initial value for last_block unless we can get error.

    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender':"MINING",
        'recipient': owner,
        'amount': MINING_REWARD
    }
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
        'transactions':copied_transaction
    }
    blockchain.append(block)
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
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True

waiting_for_input = True

while waiting_for_input:
    print("\n\n\nPlease choose")
    print("1 : Add new transaction value")
    print("2 : Mine a new block")
    print("3 : Output the blockchain blocks")
    print("4 : Output for participants")
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

    elif user_choice == "3":
        print_blockchain_value()

    elif user_choice == "4":
        print(participants)

    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index':0,
                'transactions':[{'sender':'Arpan','recipient':'korat','amount':100.0}]
            }

    elif user_choice == "q":
        waiting_for_input = False

    else:
        print("Wrong input")
    if not verify_chain():
        print("Invalid Blockchain!!!!!!!!!!!")
        waiting_for_input = False

    print(get_balance('Ashish'))