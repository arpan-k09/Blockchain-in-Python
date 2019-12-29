import hashlib
import json

def hash_str_256(st):
    return hashlib.sha256(st).hexdigest()

def hash_block(block):
    #return '-'.join([str(block[key]) for key in block])
    '''JSON converts dictionary to string and for hash fun we need string(in binary form) dumps is
    method of json package and convert it into a binary formate by encode method '''
    return hash_str_256(json.dumps(block, sort_keys=True).encode())
