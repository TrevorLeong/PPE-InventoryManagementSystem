from hashlib import sha256
import os

# File names
INVENTORY_FILE = "ppe.txt"
DISTRIBUTION_FILE = "distribution.txt"
SUPPLIERS_FILE = "suppliers.txt"
HOSPITALS_FILE = "hospitals.txt"

# Predefined users with hashed passwords
users = {
    "user1": sha256("password1".encode()).hexdigest(),
    "user2": sha256("password2".encode()).hexdigest(),
    "user3": sha256("password3".encode()).hexdigest(),
    "user4": sha256("password4".encode()).hexdigest()
}

# Default supplier data (could be initialized or managed dynamically)
SUPPLIERS = {
    "S01": {"name": "SDN", "location": "Selangor"},
    "S02": {"name": "DND", "location": "Kuala Lumpur"},
    "S03": {"name": "ADN", "location": "Seremban"}
}


# LIM WEI SHENG
# TP069493
# Login Functionality
def login():
    """User login function with a maximum of 3 attempts."""
    for attempt in range(3):
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = sha256(password.encode()).hexdigest()
        if username in users and users[username] == hashed_password:
            print("Login successful!")
            return True
        else:
            print(f"Login failed! {2 - attempt} attempts remaining.")
    print("Too many failed attempts. Access terminated.")
    return False


# MUHAMMAD ‘AQIL ‘AIZAT BIN TAUFIK
# TP067860
# Initial Inventory Creation
def create_file_if_not_exists(file_name, header):
    """Utility function to create a file with a header if it doesn't exist."""
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write(header + "\n")


def initialize_inventory():
    """Initialize the inventory with items and suppliers."""
    if os.path.exists(INVENTORY_FILE):
        print("Inventory already created.")
    else:
        with open(INVENTORY_FILE, 'w') as file:
            file.write("ItemCode,SupplierCode,ItemName,Quantity\n")
            for item_code, item_name in {
                "HC": "Head Cover",
                "FS": "Face Shield",
                "MS": "Mask",
                "GL": "Gloves",
                "GW": "Gown",
                "SC": "Shoe Covers"
            }.items():
                supplier_code = input(f"Enter supplier code for {item_name} (e.g., S01): ")
                if supplier_code not in SUPPLIERS:
                    print(f"Invalid supplier code. Defaulting to S01 for {item_name}.")
                    supplier_code = "S01"
                file.write(f"{item_code},{supplier_code},{item_name},100\n")
        print("Inventory creation completed.")

        # Initialize suppliers file
        create_file_if_not_exists(SUPPLIERS_FILE, "SupplierCode,Name,Location")
        with open(SUPPLIERS_FILE, 'w') as file:
            for code, details in SUPPLIERS.items():
                file.write(f"{code},{details['name']},{details['location']}\n")
        print("Suppliers file created.")

        # Initialize hospitals file
        create_file_if_not_exists(HOSPITALS_FILE, "HospitalCode,HospitalName")
        for i in range(3):
            hospital_code = input(f"Enter hospital code for hospital {i + 1}: ")
            hospital_name = input(f"Enter hospital name for hospital {i + 1}: ")
            with open(HOSPITALS_FILE, 'a') as file:
                file.write(f"{hospital_code},{hospital_name}\n")
        print("Hospitals file created.")


# LEONG KA CHUN
# TP069486
# Item Inventory Update
def update_inventory(item_code, quantity, action):
    """Update inventory by adding or removing items."""
    if not os.path.exists(INVENTORY_FILE):
        print("Inventory file not found.")
        return

    with open(INVENTORY_FILE, 'r') as file:
        lines = file.readlines()

    updated = False
    with open(INVENTORY_FILE, 'w') as file:
        for line in lines:
            parts = line.strip().split(',')
            if parts[0] == item_code:
                current_quantity = int(parts[3])
                if action == "add":
                    current_quantity += quantity
                elif action == "remove" and current_quantity >= quantity:
                    current_quantity -= quantity
                else:
                    print(f"Insufficient stock for {item_code}. Current stock: {current_quantity}")
                    file.write(line)
                    continue
                parts[3] = str(current_quantity)
                updated = True
            file.write(','.join(parts) + '\n')

    if updated:
        print(f"Inventory updated for {item_code}.")
    else:
        print(f"Item {item_code} not found.")


# LIM WEI SHENG
# TP069493
# Item Inventory Tracking
def record_distribution(item_code, quantity, hospital_code):
    """Record the distribution of items to hospitals."""
    if os.path.exists(DISTRIBUTION_FILE):
        mode = 'a'
    else:
        mode = 'w'

    with open(DISTRIBUTION_FILE, mode) as file:
        file.write(f"{item_code},{quantity},{hospital_code}\n")
    print(f"Recorded distribution: {item_code}, {quantity} boxes to hospital {hospital_code}.")


def print_inventory():
    """Display current inventory and low stock items."""
    if not os.path.exists(INVENTORY_FILE):
        print("Inventory file not found.")
        return

    print("Current Inventory:")
    inventory = []
    with open(INVENTORY_FILE, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            item_code, supplier_code, item_name, quantity = line.strip().split(',')
            inventory.append((item_code, supplier_code, item_name, int(quantity)))

    # Sort and display inventory
    inventory.sort()
    for item_code, supplier_code, item_name, quantity in inventory:
        print(f"{item_code} ({item_name}): {quantity} boxes from {supplier_code}")
        if quantity < 25:
            print(f"Warning: Low stock on {item_code} - only {quantity} boxes remaining!")


# PRABHRAAJ SINGH CHAHAL A/L HARJEET SINGH CHAHAL
# TP076051
# Searching Functionality
def search_distribution(item_code):
    """Search and print distribution records for an item."""
    if not os.path.exists(DISTRIBUTION_FILE):
        print("Distribution file not found.")
        return

    distribution_summary = {}
    with open(DISTRIBUTION_FILE, 'r') as file:
        for line in file:
            code, qty, hospital = line.strip().split(',')
            if code == item_code:
                distribution_summary[hospital] = distribution_summary.get(hospital, 0) + int(qty)

    if distribution_summary:
        print(f"Distribution list for {item_code}:")
        for hospital, total_qty in distribution_summary.items():
            print(f"Hospital {hospital}: {total_qty} boxes")
    else:
        print("No distributions found for this item.")


# ONG WENG HONG
# TP071236
# Report Functionality
def generate_supplier_report():
    """Generate a report listing all suppliers and their PPE items."""
    if not os.path.exists(SUPPLIERS_FILE):
        print("Suppliers file not found.")
        return

    print("Supplier Report:")
    with open(SUPPLIERS_FILE, 'r') as file:
        next(file)  # Skip header
        for line in file:
            supplier_code, name, location = line.strip().split(',')
            print(f"Supplier Code: {supplier_code}, Name: {name}, Location: {location}")
            print("Supplies:")
            with open(INVENTORY_FILE, 'r') as inv_file:
                for inv_line in inv_file:
                    item_code, sup_code, item_name, _ = inv_line.strip().split(',')
                    if sup_code == supplier_code:
                        print(f"  - {item_code} ({item_name})")


def generate_hospital_report():
    """Generate a report listing all hospitals and the quantities distributed."""
    if not os.path.exists(HOSPITALS_FILE):
        print("Hospitals file not found.")
        return

    print("Hospital Report:")
    hospitals = {}
    with open(DISTRIBUTION_FILE, 'r') as file:
        for line in file:
            item_code, quantity, hospital_code = line.strip().split(',')
            if hospital_code not in hospitals:
                hospitals[hospital_code] = {}
            if item_code not in hospitals[hospital_code]:
                hospitals[hospital_code][item_code] = 0
            hospitals[hospital_code][item_code] += int(quantity)

    with open(HOSPITALS_FILE, 'r') as file:
        next(file)  # Skip header
        for line in file:
            hospital_code, hospital_name = line.strip().split(',')
            print(f"Hospital: {hospital_name} (Code: {hospital_code})")
            if hospital_code in hospitals:
                for item_code, quantity in hospitals[hospital_code].items():
                    print(f"  - {item_code}: {quantity} boxes")


def generate_monthly_report(month):
    """Generate a transaction report for a specific month."""
    # Placeholder for the monthly report implementation
    print(f"Transactions report for {month} generated.")


def menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\nMenu:")
        print("1. Initialize Inventory")
        print("2. Update Inventory")
        print("3. Record Distribution")
        print("4. Track Inventory")
        print("5. Search Distribution")
        print("6. Generate Supplier Report")
        print("7. Generate Hospital Report")
        print("8. Generate Monthly Report")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            initialize_inventory()
        elif choice == '2':
            item_code = input("Enter item code: ")
            quantity = int(input("Enter quantity: "))
            action = input("Enter action (add/remove): ").strip().lower()
            if action in ["add", "remove"]:
                update_inventory(item_code, quantity, action)
            else:
                print("Invalid action. Use 'add' or 'remove'.")
        elif choice == '3':
            item_code = input("Enter item code: ")
            quantity = int(input("Enter quantity: "))
            hospital_code = input("Enter hospital code: ")
            update_inventory(item_code, quantity, "remove")
            record_distribution(item_code, quantity, hospital_code)
        elif choice == '4':
            print_inventory()
        elif choice == '5':
            item_code = input("Enter item code to search: ")
            search_distribution(item_code)
        elif choice == '6':
            generate_supplier_report()
        elif choice == '7':
            generate_hospital_report()
        elif choice == '8':
            month = input("Enter month (MM/YYYY): ")
            generate_monthly_report(month)
        elif choice == '9':
            print("Exiting program")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    if login():
        menu()
