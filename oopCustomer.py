class Customer:
    """Creates an object for new customers
       name: A string representing the customer's name
       balance: A float tracking the customers balance
"""

    #initialize the object with the following properties
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance

    def withdraw(self, amount):
        #check if amount withdrawn is greater than balance before proceeding
        if amount > self.balance:
            raise RuntimeError('Amount withdrawn is greater than balance.')
        elif amount == self.balance:
            raise RuntimeError('Warning: Amount withdrawn is equal to balance. Balance is now zero')
        self.balance -= amount
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance


bob = Customer('Bob', 10000.0)
jeff = Customer('Jeff', 5000)

print bob.deposit(1000)
print jeff.withdraw(5000)
