import sys
import re
import json
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtGui import QFont

# ------------------- Class definition -------------------


class POS(QMainWindow):
    """A simple POS app"""

    all_items_window = None
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Zone POS")
        self.initUI()

    def initUI(self):
        # WIDGETS:
        # Item
        self.item_label = QLabel("ITEM NAME:")
        self.item_label.setFont(QFont("Times new roman", 12))
        self.item_entry = QLineEdit()
        self.item_entry.setFont(QFont("Times new roman", 12))

        # quantity
        self.quantity_label = QLabel("QUANTITY:")
        self.quantity_label.setFont(QFont("Times new roman", 12))
        self.quantity_entry = QLineEdit()
        self.quantity_entry.setFont(QFont("Times new roman", 12))

        # price
        self.price_label = QLabel("PRICE:")
        self.price_label.setFont(QFont("Times new roman", 12))
        self.price_entry = QLineEdit()
        self.price_entry.setFont(QFont("Times new roman", 12))

        # cost
        self.cost_label = QLabel("COST:")
        self.cost_label.setFont(QFont("Times new roman", 12))
        self.cost_entry = QLineEdit()
        self.cost_entry.setFont(QFont("Times new roman", 12))

        # supplier
        self.supplier_label = QLabel("SUPPLIER:")
        self.supplier_label.setFont(QFont("Times new roman", 12))
        self.supplier_entry = QLineEdit()
        self.supplier_entry.setFont(QFont("Times new roman", 12))


        # BUTTONS:
        self.add_button = QPushButton("ADD ITEM")
        self.add_button.setFont(QFont("Times new roman", 12))
        self.search_button = QPushButton("SEARCH")
        self.search_button.setFont(QFont("Times new roman", 12))
        self.show_all_items = QPushButton("SHOW ALL ITEMS")
        self.show_all_items.setFont(QFont("Times new roman", 12))
        self.delete_button = QPushButton("DELETE ITEM")
        self.delete_button.setFont(QFont("Times new roman", 12))

        self.setFixedSize(500, 400)

        # Layout
        layout = QVBoxLayout()
        # item
        layout.addWidget(self.item_label)
        layout.addWidget(self.item_entry)
        # quantity
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_entry)
        # price
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_entry)
        # cost
        layout.addWidget(self.cost_label)
        layout.addWidget(self.cost_entry)
        # supplier
        layout.addWidget(self.supplier_label)
        layout.addWidget(self.supplier_entry)

        # buttons
        layout.addWidget(self.add_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.show_all_items)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # connecting functions with the buttons
        self.add_button.clicked.connect(self.add_data)
        self.search_button.clicked.connect(self.find_item)
        self.delete_button.clicked.connect(self.delete_data)
        self.show_all_items.clicked.connect(self.show_all_items_func)

    def add_data(self):
        item = self.item_entry.text().lower()
        if self.quantity_entry.text():
            quantity = int(self.quantity_entry.text())
        price = self.price_entry.text()
        cost = self.cost_entry.text()  
        supplier = self.supplier_entry.text()

        if not item:
            QMessageBox.critical(
                self, "Oops", "Item entry can't be empty.")
            self.item_entry.clear()
            self.price_entry.clear()
            self.quantity_entry.clear()
            return  

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        # If the item already exists
        if item in data:
            QMessageBox.critical(
                self,
                "Error",
                "Item already exists."
            )

            self.item_entry.clear()
            self.price_entry.clear()
            self.quantity_entry.clear()

            return  

        # Add new item to the data
        data[item] = {
            "quantity": quantity,
            "price": price,
            "cost": cost,  
            "supplier": supplier,  
        }

        # Write the updated data to the json
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        QMessageBox.information(
            self, "Success", f"You've successfully added {item}!")

        # Refresh the table 
        if POS.all_items_window:
            table = POS.all_items_window.findChild(QTableWidget)
            if table:
                self.populate_table(table, data)

        self.item_entry.clear()
        self.price_entry.clear()
        self.quantity_entry.clear()
        self.cost_entry.clear()  
        self.supplier_entry.clear()  


    def delete_data(self):
        item = self.item_entry.text().lower()

        if re.search('^\s+$', item) or (not item):
            QMessageBox.information(
                self,
                "Oops",
                "You've left the item field empty"
            )
            return

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Error",
                "Data file not found."
            )
            self.item_entry.clear()
            return

        if item in data:
            del data[item]
            QMessageBox.information(
                self,
                "Success",
                f"You've successfully deleted {item}!"
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"{item} not found in the saved items!"
            )

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        
        if POS.all_items_window:
            table = POS.all_items_window.findChild(QTableWidget)
            if table:
                self.populate_table(table, data)

        self.item_entry.clear()
        self.price_entry.clear()

    def find_item(self):
        item = self.item_entry.text()

        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Error",
                "No data file found"
            )
        else:
            if item in data:
                quantity = data[item]['quantity']
                price = data[item]['price']
                QMessageBox.information(
                    self,
                    item,
                    f"Quantity: {quantity}\nPrice: {price}"
                )
            elif re.search("^\s+$", item):
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Please enter a valid item name."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"No details for {item} exist."
                )

    def show_all_items_func(self):
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "Error",
                "No data file found"
            )
        else:
            if data:
                # Check if the window is already created
                if not POS.all_items_window:
                    # Create a new window for displaying all items
                    POS.all_items_window = QWidget()
                    POS.all_items_window.setWindowTitle("All Items")

                    # Create a table 
                    table = QTableWidget()
                    table.setColumnCount(5)  # Item, Quantity, Price, Cost, supplier
                    table.setHorizontalHeaderLabels(["Item", "Quantity", "Price", "Cost", "Supplier"])

                    self.populate_table(table, data)

                    # layout for the new window
                    layout = QVBoxLayout()
                    layout.addWidget(table)

                    POS.all_items_window.setLayout(layout)

                # Set size for the window
                POS.all_items_window.setFixedSize(550, 600)

                POS.all_items_window.show()
            else:
                QMessageBox.information(
                    self,
                    "No Data",
                    "No data available."
                )

    def populate_table(self, table, data):
        table.setRowCount(0)  # Clear existing rows
        for row, (item, details) in enumerate(data.items()):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(item))
            table.setItem(row, 1, QTableWidgetItem(str(details.get('quantity', ''))))
            table.setItem(row, 2, QTableWidgetItem(str(details.get('price', ''))))
            table.setItem(row, 3, QTableWidgetItem(str(details.get('cost', ''))))
            table.setItem(row, 4, QTableWidgetItem(str(details.get('supplier', ''))))

    def add_data(self):
        item = self.item_entry.text().lower()
        if self.quantity_entry.text():
            quantity = int(self.quantity_entry.text())
        price = self.price_entry.text()
        cost = self.cost_entry.text()
        supplier = self.supplier_entry.text()

        if not item:
            QMessageBox.critical(
                self, "Oops", "Item entry can't be empty.")
            self.item_entry.clear()
            self.price_entry.clear()
            self.quantity_entry.clear()
            return 

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        # Check if the item already exists
        if item in data:
            QMessageBox.critical(
                self,
                "Error",
                "Item already exists."
            )

            self.item_entry.clear()
            self.price_entry.clear()
            self.quantity_entry.clear()
            self.cost_entry.clear()
            self.supplier_entry.clear()

            return 

        # Add the new item to the data
        data[item] = {
            "quantity": quantity,
            "price": price,
            "cost": cost,
            "supplier": supplier,
        }

        # Write the updated data to the json file
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        QMessageBox.information(
            self, "Success", f"You've successfully added {item}!")

        # Refresh the table
        if POS.all_items_window:
            table = POS.all_items_window.findChild(QTableWidget)
            if table:
                self.populate_table(table, data)

        self.item_entry.clear()
        self.price_entry.clear()
        self.quantity_entry.clear()
        self.cost_entry.clear()
        self.supplier_entry.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POS()
    window.show()
    sys.exit(app.exec())