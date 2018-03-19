import threading
import random as rnd



class Ledger(object):

    def __init__(self):
        self.ledger = {}
        self.counter = 0
        self.thread_lock = threading.Lock()

    def transfer(self, _from, _to, amount, type="common"):

        with self.thread_lock:
            self.counter += 1
            key = (_from, _to, self.counter, type)

        self.ledger[key] = amount

    def process_transfers(self, balances={}):

        net_transactions = {}

        for key in self.ledger.keys():
            clearance_key_A = (key[0], key[1])
            clearance_key_B = (key[1], key[0])

            amount = self.ledger[key]

            net_transactions[clearance_key_A] = net_transactions.get(clearance_key_A, 0) - amount
            net_transactions[clearance_key_B] = net_transactions.get(clearance_key_B, 0) + amount

            balances[clearance_key_A[0]] = balances.get(clearance_key_A[0], 0) - amount
            balances[clearance_key_A[1]] = balances.get(clearance_key_A[1], 0) + amount

        return net_transactions, balances

    def validate_net_transactions(self, net_transactions):

        result = 0
        for value in net_transactions.values():
            result += value

        if result != 0:
            raise ValueError("Result not zero - mismatched transactions: "+str(result))


ledger = Ledger()

banks = ["A", "B", "C", "D"]
max_amount = 2000
min_amount = 10

for i in range(0, 1000):
    id_A = rnd.randint(0, len(banks)-1)
    id_B = rnd.randint(0, len(banks)-1)

    if id_A == id_B:
        if id_B == len(banks) - 1:
            id_A = id_B - 1
        elif id_B == 0:
            id_A = 1

    amt = rnd.randrange(min_amount,max_amount)

    ledger.transfer(banks[id_A],banks[id_B],amt)

net_trans, balances = ledger.process_transfers()

ledger.validate_net_transactions(net_trans)

print(balances)









