from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random

'''binascii converts binary to ascii value'''
import binascii


class Wallet:
    """Creates, loads and holds private and public keys. Manages transaction signing and verification."""

    def __init__(self):
        # private_key, public_key = self.generate_keys()
        # self.private_key = private_key
        # self.public_key = public_key
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        """Create a new pair of private and public keys."""
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        # with open('wallet.txt', mode='w') as f:
        #     f.write(self.public_key)
        #     f.write('\n')
        #     f.write(self.private_key)

    def save_keys(self):
        """Saves the keys to a file (wallet.txt)."""
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                return True
            except (IOError, IndexError):
                print('Saving wallet failed...')
                return False

    def load_keys(self):
        """Loads the keys from the wallet.txt file into memory."""
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                '''At above we can see new line is add esacap char so we don't need it so we're using [:-1] range selector '''
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
            return True
        except (IOError, IndexError):
            print('Loading wallet failed...')
            return False


    def generate_keys(self):
        """Generate a new pair of private and public key."""
        '''First arg of the RSA.generate is a bit length and second is random function!!!'''
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        '''Public key is generated from the Private key so both are related to each other!!!!'''
        public_key = private_key.publickey()
        '''hexlify is for hexadecimal repre.... of binary data ... and DER is binary encoding'''
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii')
                , binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_transaction(self, sender, recipient, amount):
        """Sign a transaction and return the signature.

        Arguments:
            :sender: The sender of the transaction.
            :recipient: The recipient of the transaction.
            :amount: The amount of the transaction.
        """
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        """Verify the signature of a transaction.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        # if transaction.sender == 'MINING':
        #     return True

        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))