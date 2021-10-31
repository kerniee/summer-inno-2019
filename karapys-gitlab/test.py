import unittest
from main import sendTx, web3

class TestSending(unittest.TestCase):
    
    def test_one_tx(self):
        self.assertEqual(web3.eth.getBalance('0x0000000000000000000000000000000000000000'), 0)
        sendTx()
        self.assertEqual(web3.eth.getBalance('0x0000000000000000000000000000000000000000'), 100)

if __name__ == '__main__':
    unittest.main()
