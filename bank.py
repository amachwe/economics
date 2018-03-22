from ledger import Ledger


class Bank(object):

    def __init__(self, id):

        self.id = id
        self.ledger = Ledger()
        self.net_deposits = {}
        self.net_transfers = {}

    def execute(self):

        self.net_transfers, self.net_deposits = self.ledger.process_transfers()

    def deposit(self, amount):
        self.ledger.deposit(self.id,amount)

    def withdrawal(self, amount):
        self.ledger.withdrawal(self.id, amount)

    def transfer(self,_to,amount):
        self.ledger.transfer(self.id,_to,amount)




bankA = Bank("A")
bankB = Bank("B")
bankA.deposit(1000)
bankB.deposit(2000)
bankA.transfer("B",10000)
bankA.withdrawal(1000)
bankB.withdrawal(2500)

bankA.execute()
bankB.execute()

print bankA.net_deposits
print bankA.net_transfers

print bankB.net_deposits