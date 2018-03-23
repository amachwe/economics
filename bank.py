from ledger import Ledger


class Bank(object):

    def __init__(self, id):

        self.id = id
        self.ledger = Ledger()
        self.net_deposits = {}
        self.net_transfers = {}
        self.securities = 0

    def execute(self):

        self.net_transfers, self.net_deposits = self.ledger.process_transfers()

    def deposit(self, amount):
        self.ledger.deposit(self.id,amount)

    def withdrawal(self, amount):
        self.ledger.withdrawal(self.id, amount)

    def transfer(self,_to,amount):
        self.ledger.transfer(self.id,_to,amount)

    def buy_securities(self, issuer_id, qty, asset_price=1.0):
        self.securities += qty
        self.ledger.transfer(self.id,issuer_id, asset_price*qty)

    def add_interest(self, interest_rate):

        self.net_deposits += self.net_deposits * interest_rate


class Government(object):

    def __init__(self, id):
        self.securities = 0
        self.money = 0
        self.id = id

    def create_securities(self, amount):
        self.securities += amount

    def sell_securities(self, qty, asset_price=1.0):
        if self.securities > qty:
            self.securities -= qty
            self.money += qty * asset_price
            return qty
        return 0

    def buy_securities(self, qty, asset_price=1.0):
        if qty > 0:
            self.securities += qty
            self.money -= qty * asset_price
            return qty
        return 0


class CentralBank(Bank):

    def __init__(self, id):
        super(CentralBank, self)
        self.id = id
        self.base_rate = 0.3 # % rate per turn
        self.total_reserves = 0

    def buy_reserves(self, _to, amount, asset_price = 1.0):
        self.ledger.deposit(_to, amount*asset_price)
        self.total_reserves += amount*asset_price

    def transfer_reserves(self,_from,_to,amount):
        self.ledger.transfer(_from, _to, amount)

    def set_base_rate(self, base_rate):

        self.base_rate = base_rate

    def get_base_rate(self):

        return self.base_rate

    def loan_reserves(self, _to, duration, amount):

        actual_amount = amount / ((1 + (self.base_rate/100))**duration)
        self.total_reserves += actual_amount

        self.ledger.deposit(_to,actual_amount)









bankA = Bank("A")
bankB = Bank("B")
bankC = CentralBank("Central")
govt = Government("Govt")
govt.create_securities(10000)

bankA.deposit(1000)
bankB.deposit(2000)
qty = govt.sell_securities(100, asset_price=1.11)
bankB.buy_securities("Govt",qty, asset_price=1.11)

bankA.transfer("B",10000)
bankA.withdrawal(1000)
bankB.withdrawal(2500)

bankA.execute()
bankB.execute()

print bankA.net_deposits
print bankA.net_transfers
print bankB.securities
print govt.securities
print govt.money

print bankB.net_deposits