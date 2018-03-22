import threading
import random as rnd


class TransactionType(object):

        DEPOSIT = "deposit"
        WITHDRAWAL = "withdrawal"
        BANK_TRANSFER = "bank_transfer"


class Ledger(object):

    def __init__(self):
        self.ledger = {}
        self.counter = 0
        self.thread_lock = threading.Lock()

    def deposit(self, _to, amount):

        with self.thread_lock:
            self.counter += 1

        key = ("", _to, self.counter, TransactionType.DEPOSIT)

        self.ledger[key] = amount

    def withdrawal(self, _to, amount):

        with self.thread_lock:
            self.counter += 1

        key = ("", _to, self.counter, TransactionType.WITHDRAWAL)

        self.ledger[key] = -amount

    def transfer(self, _from, _to, amount, asset_price=1.0):

        with self.thread_lock:
            self.counter += 1

        key = (_from, _to, self.counter, TransactionType.BANK_TRANSFER)

        self.ledger[key] = amount*asset_price

    def process_transfers(self):

        net_transactions = {}
        net_deposits = {}

        for key in self.ledger.keys():

            amount = self.ledger[key]
            tx_type = key[3]

            if tx_type == TransactionType.BANK_TRANSFER:
                clearance_key_A = (key[0], key[1])
                clearance_key_B = (key[1], key[0])

                net_transactions[clearance_key_A] = net_transactions.get(clearance_key_A, 0) - amount
                net_transactions[clearance_key_B] = net_transactions.get(clearance_key_B, 0) + amount

            elif tx_type == TransactionType.DEPOSIT or tx_type == TransactionType.WITHDRAWAL:
                net_deposits[key[1]] = net_deposits.get(key[1], 0) + amount

        return net_transactions, net_deposits

    @staticmethod
    def validate_net_transactions(net_transactions):

        result = 0
        for value in net_transactions.values():
            result += value

        if result != 0:
            raise ValueError("Result not zero - mismatched transactions: "+str(result))


if __name__ == 'main':
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

        amt = rnd.randrange(min_amount, max_amount)
        if rnd.random()>0.5:
            ledger.deposit(banks[id_B], amt)
        else:
            ledger.withdrawal(banks[id_B], amt)

    net_trans, balances, deposits = ledger.process_transfers()

    Ledger.validate_net_transactions(net_trans)

    print(balances)
    print(net_trans)
    print(deposits)









