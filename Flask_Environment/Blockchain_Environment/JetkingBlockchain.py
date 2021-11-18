#Importing the modules, datetime, json, hashlib, Flask, jsonify

import datetime
import json
import hashlib
from flask import Flask, jsonify

#Create the class called Blockchain

class Blockchain:
   
   def __init__(self):
       self.chain = []
       self.create_blockchain(proof_of_work=1, previous_hash='0')

   def create_blockchain(self, proof_of_work, previous_hash):
       block = {
           'index': len(self.chain) + 1,
           'timestamp': str(datetime.datetime.now()),
           'proof_of_work': proof_of_work,
           'previous_hash': previous_hash
       }

       self.chain.append(block)
       return block

   def get_previous_block(self):
       last_block = self.chain[-1]
       return last_block

   def proof_of_work(self, previous_proof):

       # miners proof submitted
       new_proof = 1

       # status of proof of work
       check_proof = False

       while check_proof is False:

           # problem and algorithm based off the previous proof and new proof
           hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

           # check miners solution to problem, by using miners proof in cryptographic encryption

           # if miners proof results in 4 leading zero's in the hash operation, then:

           if hash_operation[:4] == '0000':
               check_proof = True

           else:
               # if miners solution is wrong, give miner another chance until he is getting correct proof
               new_proof += 1

       return new_proof

   # generate a hash of an entire block
   def hash(self, block):

       encoded_block = json.dumps(block, sort_keys=True).encode()
       return hashlib.sha256(encoded_block).hexdigest()

   # check if the blockchain is valid
   def is_chain_valid(self, chain):

       # get the first block in the chain and it serves as the previous block
       previous_block = chain[0]

       # an index of the blocks in the chain for iteration
       block_index = 1

       while block_index < len(chain):
	   #untill 10<10 while loop will iterates it starts from 1<10
           # get the current block
           block = chain[block_index]

           # check if the current block link to previous block has the same hash of the previous block
           if block["previous_hash"] != self.hash(previous_block):
               return False

           # get the previous proof from the previous block
           previous_proof = previous_block['proof_of_work']

           # get the current proof from the current block
           current_proof = block['proof_of_work']

           # run the proof data through the algorithm
           hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

           # check if hash operation is invalid
           if hash_operation[:4] != '0000':
               return False

           # set the previous block to the current block after running validation on current block
           previous_block = block
           block_index += 1
       return True


app = Flask(__name__)

blockchain = Blockchain()


@app.route('/mine_a_block', methods=['GET'])
def mine_a_block():
   # get the data we need to create a block

   previous_block = blockchain.get_previous_block()

   previous_proof = previous_block['proof_of_work']

   proof_of_work = blockchain.proof_of_work(previous_proof)

   previous_hash = blockchain.hash(previous_block)

   block = blockchain.create_blockchain(proof_of_work, previous_hash)

   response = {'message': 'Congratualtions,You have Successfully Mined a New Block!!!!!',
               'index': block['index'],
               'timestamp': block['timestamp'],
               'proof_of_work': block['proof_of_work'],
               'previous_hash': block['previous_hash']}

   return jsonify(response), 200

@app.route('/get__complete_chain', methods=['GET'])
def get_complete_chain():

   response = {'chain': blockchain.chain,
               'length': len(blockchain.chain)}

   return jsonify(response), 200

@app.route('/is_blockchain_valid', methods=['GET'])
def is_blockchain_valid():

    valid = blockchain.is_chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'Yes, The Blockchain is valid.'}

    else:
        response = {'message': 'No, The Blockchain is not valid.'}

    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
