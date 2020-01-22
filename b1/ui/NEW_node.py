from flask import Flask, jsonify, request, send_from_directory
'''jasonify takes data and automatically converts into the json data.........'''
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain


app = Flask(__name__)
wallet = Wallet()
'''We're passing None value of public key to the blockchain constructor...'''
blockchain = Blockchain(wallet.public_key)
CORS(app)


'''It's for response from server so we're sending back a res through a GET method..
and route is a end point and app is our application name above we can change it to anything we
want'''
@app.route('/', methods=['GET'])
def get_ui():
    #return 'This works!!!!'
    '''For the redirecting towards the html file uses send_from_directory function '''
    return send_from_directory('ui', 'NEW_node.html')

# '''Starting phase is this............'''
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)




@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    # wallet.save_keys()
    # response = {
    #     'public_key': wallet.public_key,
    #     'private_key': wallet.private_key,
    #     'funds': blockchain.get_balance()
    # }
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        #blockchain = Blockchain(wallet.public_key)
        return jsonify(response), 201
    else:
        response = {
            'message': 'Saving the keys failed.'
        }
        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Loading the keys failed.'
        }
        return jsonify(response), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Fetched balance successfully.',
            'funds': balance
        }
        return jsonify(response), 200
    else:
        response = {
            'messsage': 'Loading balance failed.',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'No wallet set up.'
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing.'
        }
        return jsonify(response), 400

    recipient = values['recipient']
    amount = values['amount']

    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)

    if success:
        response = {
            'message': 'Successfully added transaction.',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500


@app.route('/mineblock', methods=['POST'])
def block_mine():
    '''using mine_block method which is inside a blockchain file.......'''
    block = blockchain.mine_block()
    # dict_block = block.__dict__.copy()
    # dict_block['transactions'] = [
    #     tx.__dict__ for tx in dict_block['transactions']]


    # if blockchain.mine_block():
    #     return ...
    # else:
    #     response = {
    #         'message': 'Adding a block failed.',
    #         'wallet_set_up': wallet.public_key != None
    #     }
    #     return jsonify(response), 500


    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Block added successfully.',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed.',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/transactions', methods=['GET'])
def get_open_transaction():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]

    # response = {
    #     'message' : 'Fetched transaction successfully..',
    #     'transactions' : dict_transactions
    # }
    return jsonify(dict_transactions), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    '''we need to convert the objects to json serializable so we're using list comp.....'''
    di_chain = [block.__dict__.copy() for block in chain_snapshot]
    for d_b in di_chain:
        d_b['transactions'] = [tx.__dict__ for tx in d_b['transactions']]

    #     '''second in return statment is a status code and 200 is for OK'''
    #     return jsonify(chain_snapshot), 200
    return jsonify(di_chain), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
