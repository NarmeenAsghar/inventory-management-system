## 📦 Inventory Management System

A simple command-line Inventory Management System built using **Object-Oriented Programming** in Python. It supports managing multiple product types (Electronics, Grocery, and Clothing), with features like adding, removing, searching, selling, restocking, and persisting data using JSON files.

### ✅ Features

* Add new products (Electronics, Grocery, Clothing)
* Sell and restock existing products
* Search by **name** or **type**
* View all products in a clean, readable format
* Save and load inventory to/from a JSON file
* Remove expired grocery items automatically

### 🛠 Technologies Used

* Python 3
* Object-Oriented Programming (OOP)
* JSON for file operations
* Custom Exception Handling

### 📦 Product Types and Their Attributes

| Type        | Common Fields             | Additional Fields          |
| ----------- | ------------------------- | -------------------------- |
| Electronics | ID, Name, Price, Quantity | Brand, Warranty (in years) |
| Grocery     | ID, Name, Price, Quantity | Expiry Date (YYYY-MM-DD)   |
| Clothing    | ID, Name, Price, Quantity | Size, Material             |

### 🚀 How to Run

1. **Make sure you have Python 3 installed.**
2. Save the code into a Python file (e.g., `main.py`)
3. Run the program:

   ```bash
   main.py
   ```

### 🧪 Sample Workflow

```bash
1. Add Product
   > Type: Electronics
   > ID: E101
   > Name: Laptop
   > Price: 60000
   > Quantity: 10
   > Brand: Dell
   > Warranty: 2

2. View All Products
   > Displays all product info with clean formatting

3. Save Inventory
   > Filename: my_inventory.json

4. Load Inventory
   > Filename: my_inventory.json
```

### 📁 File Save & Load

* Inventory can be saved to a `.json` file via Option 5.
* Same file can be loaded later via Option 6.
* Ensure filenames are provided **with `.json` extension**.

### ⚠️ Error Handling

* Duplicate Product ID → `DuplicateIDError`
* Invalid search type or product not found → Message displayed
* Expired groceries removed silently during listing or loading
