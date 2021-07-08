from random import randrange
from uuid import uuid4
from classes import Blockchain
from flask import Flask, render_template, request

# Instantiate our Node
app = Flask("Home")

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html", message="Hello Flask!")

@app.route('/mine', methods=['GET'])
def mine():
    # Run the proof of work algo to get the next proof
    last_block = blockchain.last_block
    proof = blockchain.calculate_proof_of_work(last_block['proof'])

    # There is a reward for finding the proof
    # Sender is 0 and a new coin is mined

    blockchain.new_transaction(
        sender="0",
        recipient=str(uuid4()).replace('-', ''),
        amount=1,
    )
    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.mine(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return render_template("mine.html", message=response), 200


@app.route('/new', methods=['GET', 'POST'])
def new_transaction():
    # imported_json = json.loads(request.data)
    imported_json = {
        'sender': str(uuid4()).replace('-', ''),
        'recipient': str(uuid4()).replace('-', ''),
        'amount': randrange(1000)
    }
    # Check all required fields
    required = ['sender', 'recipient', 'amount']
    for elem in required:
        if (imported_json[elem] == ""):
            return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(imported_json['sender'], imported_json['recipient'], imported_json['amount'])

    return render_template("new.html", message=imported_json), 200


@app.route('/nodes', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return render_template("nodes.html", nodes=response['chain']), 200


if __name__ == '__main__':
    app.run()
