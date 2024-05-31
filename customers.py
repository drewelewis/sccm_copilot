from dataclasses import dataclass
from typing import List

    
@dataclass
class Order:
    id: int
    product: str
    quantity: int

    def tojson(self):
        return {
            'id': self.id,
            'product': self.product,
            'quantity': self.quantity
        }

    
@dataclass
class Customer:
    id: int
    name: str
    orders: List[Order]

    def tojson(self):
        return {
            'id': self.id,
            'name': self.name,
            'orders': [order.tojson() for order in self.orders]
        }

@dataclass
class Customers:
    customers: List[Customer]

    def tojson(self):
        return {
            'customers': [customer.tojson() for customer in self.customers]
        }
    
# Create a list of orders
orders = [Order(1, 'Product1', 2), Order(2, 'Product2', 1), Order(3, 'Product3', 5)]

# Create a list of customers
customers = [Customer(1, 'Customer1', orders), Customer(2, 'Customer2', [])]

c=Customers(customers)
print(c.tojson())
print("-------------------------")
# Print the list of customers
for customer in customers:
    print(customer.tojson())