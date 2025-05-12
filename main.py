# Imports
from abc import ABC, abstractmethod # for abstract classes
import json # for JSON file handling
from datetime import datetime # for date handling

# Custom Exception Classes
class OutOfStockError(Exception):
    pass # pass statement is used to indicate that the function does not do anything before we define or call it

class DuplicateIDError(Exception):
    pass

class InvalidData(Exception):
    pass

# Abstract Base Class
class Product(ABC):
    def __init__(self, product_id, name, price, quantity_in_stock):  # constructor
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock

    @abstractmethod # abstract method
    def restock(self, amount):
        pass

    @abstractmethod
    def sell(self, quantity):
        pass

    def get_total_value(self):
        return self._price * self._quantity_in_stock
    
    def __str__(self): # overriding the __str__ method to provide a string representation of the object
        return f"Product ID: {self._product_id}\nProduct Name: {self._name}\nProduct Price: {self._price} PKR\nQuantity Of Product: {self._quantity_in_stock}"

# Subclasses of Product
class Electronics(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, brand, warranty_years):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.brand = brand
        self.warranty_years = warranty_years

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise OutOfStockError("Sorry! This product does not have enough stock.")
        self._quantity_in_stock -= quantity

    def __str__(self):  # overriding the __str__ method to include brand and warranty
        return super().__str__() + f"\nBrand Of Product: {self.brand}\nWarranty of Product: {self.warranty_years} years"

class Grocery(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, expiry_date):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d") # converting string to datetime object

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise OutOfStockError("Sorry! This product does not have enough stock.")
        self._quantity_in_stock -= quantity

    def is_expired(self):
        return datetime.now() > self.expiry_date # checking if the product is expired

    def __str__(self): # overriding the __str__ method to include expiry date
        status = "Product is Expired" if self.is_expired() else "Product is not expired"
        return super().__str__() + f"\nExpiry Date: {self.expiry_date.date()} | {status}"

class Clothing(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, size, material):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.size = size
        self.material = material

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise OutOfStockError("Sorry! This product does not have enough stock.")
        self._quantity_in_stock -= quantity

    def __str__(self): # overriding the __str__ method to include size and material
        return super().__str__() + f"\nSize: {self.size}\nMaterial: {self.material}"

# Inventory Class
class Inventory:
    def __init__(self):
        self._products = {} # dictionary to store products with product_id as key

    def add_product(self, product):
        if product._product_id in self._products: # checking if product ID already exists
            raise DuplicateIDError("The product ID you entered already exists.")
        self._products[product._product_id] = product # adding product to the inventory

    def remove_product(self, product_id): # removing product from the inventory
        if product_id in self._products:
            del self._products[product_id]

    def search_by_name(self, name): # searching product by name
        return [p for p in self._products.values() if p._name.lower() == name.lower()]  # case insensitive search
    
    def search_by_type(self, product_type): # searching product by type
        return [p for p in self._products.values() if type(p).__name__.lower() == product_type.lower()]
    
    def list_all_products(self): # listing all products
        return list(self._products.values())
    
    def sell_product(self, product_id, quantity): # selling product
        if product_id not in self._products:
            raise KeyError("This product is not found.")
        self._products[product_id].sell(quantity) 

    def restock_product(self, product_id, quantity): # restocking product
        if product_id not in self._products:
            raise KeyError("This product is not found.")
        self._products[product_id].restock(quantity)

    def total_inventory_value(self): # calculating total inventory value
        return sum(p.get_total_value() for p in self._products.values())

    def remove_expired_products(self): # removing expired products
        expired_ids = [pid for pid, prod in self._products.items() # pid is product id and prod is product object
                       if isinstance(prod, Grocery) and prod.is_expired()]
        for pid in expired_ids:  # removing expired products
            del self._products[pid]

    def save_to_file(self, filename): # saving inventory to a file
        data = [] # list to store product data
        for p in self._products.values():
            d = { # dictionary to store product details
                "type": p.__class__.__name__,
                "id": p._product_id,
                "name": p._name,
                "price": p._price,
                "quantity": p._quantity_in_stock
            }
            if isinstance(p, Electronics): #isinstance checks to determine the type of product
                d.update({"Warranty Of Product": p.warranty_years, "Brand Of Product": p.brand}) # updating dictionary with product details
            elif isinstance(p, Grocery):
                d.update({"Expiry Date": p.expiry_date.strftime("%Y-%m-%d")})
            elif isinstance(p, Clothing):
                d.update({"Size OF Product": p.size, "Product Material": p.material})
            data.append(d)
        with open(filename, "w") as f: # writing data to file 
            json.dump(data, f) # converting a Python object into a JSON string

    def load_from_file(self, filename): # loading inventory from a file
        with open(filename, "r") as f: # reading data from file
            data = json.load(f) # converting JSON string into a Python object
            for d in data:
                t = d["type"] # getting the type of product
                if t == "Electronics":
                    p = Electronics(d["ID Of Product"], d["Name"], d["Price"], d["Quantity"], d["Brand"], d["Warranty Of Product"])
                elif t == "Grocery":
                    p = Grocery(d["ID Of Product"], d["Name"], d["Price"], d["Quantity"], d["Expiry Date"])
                elif t == "Clothing":
                    p = Clothing(d["ID Of Product"], d["Name"], d["Price"], d["Quantity"], d["Size"], d["Material"])
                else:
                    continue
                self._products[d["ID Of Product"]] = p

# main function to run the program
def main():
    inventory = Inventory()
    print("================= Welcome to the Inventory Management System ================")

    while True:
        print("\n1. Add Product")
        print("2. Sell Product")
        print("3. Search Product")
        print("4. View All Products")
        print("5. Save Inventory")
        print("6. Load Inventory")
        print("7. Exit")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            ptype = input("Enter Type Of Products (Electronics/Grocery/Clothing): ").lower()
            pid = input("Product ID: ")
            name = input("Name: ")
            price = float(input("Price: "))
            qty = int(input("Quantity: "))

            try:
                if ptype == "electronics":
                    brand = input("Enter Brand Name: ")
                    warranty = int(input("Warranty Of Product (years): "))
                    prod = Electronics(pid, name, price, qty, brand, warranty)
                elif ptype == "grocery":
                    exp = input("Expiry Date (YYYY-MM-DD): ")
                    prod = Grocery(pid, name, price, qty, exp)
                elif ptype == "clothing":
                    size = input("Size: ")
                    material = input("Material: ")
                    prod = Clothing(pid, name, price, qty, size, material)
                else:
                    print("Invalid Type! Please enter Electronics, Grocery, or Clothing.")
                    continue

                inventory.add_product(prod)
                print("Product has been added.")
            except Exception as e:  # catching any exception that occurs during product addition
                print("Error:", e)

        elif choice == "2":
            pid = input("Product ID: ")
            qty = int(input("Quantity: "))
            try:
                inventory.sell_product(pid, qty)
                print("Product is soldout.")
            except Exception as e:  # catching any exception that occurs during product selling
                print("Error:", e)

        elif choice == "3":
            mode = input("Search by name/type: ").lower()
            if mode == "name":
                name = input("Enter name of product: ")
                for p in inventory.search_by_name(name):
                    print(p)
            elif mode == "type":
                typ = input("Enter type of product: ")
                for p in inventory.search_by_type(typ):
                    print(p)
            else:
                print("Invalid search mode! Please try again.")

        elif choice == "4":
            for p in inventory.list_all_products():
                print(p)
                print("-" * 50)

        elif choice == "5":
            f = input("Filename: ") # getting filename from user only in json format like "filename.json"
            inventory.save_to_file(f)
            print("Inventory details is saved.")

        elif choice == "6":
            f = input("Filename: ")
            inventory.load_from_file(f) # loading inventory from file, same file used in saving
            print("Inventory loaded.")

        elif choice == "7":
            print("Thankyou! For Using this program.")
            break

        else:
            print("Invalid choice! Please try again.")

# calling main function
if __name__ == "__main__":
    main()