import csv
import os
from datetime import datetime


class CargoTracking:
    def __init__(self, filename="shipments.csv"):
        self.filename = filename
        self.initialize_file()

    def initialize_file(self):
        """Create CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Shipment ID', 'Cargo Type', 'Driver Name', 'End Location', 
                    'Estimated Arrival', 'Status', 'Date Added'
                ])

    def collect_cargo_information(self):
        """Collect cargo and shipment information from user input."""
        print("\n" + "="*50)
        print("CARGO/SHIPMENT INFORMATION FORM")
        print("="*50 + "\n")

        shipment_id = input("Enter shipment ID: ").strip()
        
        # Check for duplicate shipment ID
        if self.shipment_exists(shipment_id):
            print(f"Error: Shipment ID {shipment_id} already exists!")
            return None

        cargo_type = input("Enter cargo type (e.g., Electronics, Produce, Chemicals, Furniture): ").strip()
        driver_name = input("Enter driver name (First Last): ").strip()
        end_location = input("Enter end location (destination): ").strip()

        # Get ETA
        while True:
            eta = input("Enter estimated time of arrival (YYYY-MM-DD HH:MM format): ").strip()
            if self.validate_datetime(eta):
                break
            print("Invalid format. Please use YYYY-MM-DD HH:MM (e.g., 2026-08-25 14:30)")

        status = "In Transit"

        # Create shipment entry
        shipment_data = [
            shipment_id, cargo_type, driver_name, end_location, eta, status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        return shipment_data

    def validate_datetime(self, date_string):
        """Validate date and time format."""
        try:
            datetime.strptime(date_string, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    def shipment_exists(self, shipment_id):
        """Check if shipment ID already exists."""
        if not os.path.exists(self.filename):
            return False
        
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == shipment_id:
                    return True
        return False

    def save_shipment(self, shipment_data):
        """Save shipment information to CSV file."""
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(shipment_data)
        print("\n✓ Shipment information saved successfully!")

    def display_all_shipments(self):
        """Display all recorded shipments."""
        if not os.path.exists(self.filename):
            print("No shipment records found.")
            return

        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            shipments = list(reader)

        if len(shipments) <= 1:
            print("No shipment records found.")
            return

        print("\n" + "="*100)
        print("ACTIVE SHIPMENTS")
        print("="*100)
        
        # Print header
        print(f"{'Shipment ID':<15} {'Cargo Type':<18} {'Driver':<18} {'End Location':<20} {'ETA':<19} {'Status':<12}")
        print("-"*100)
        
        # Print data rows
        for shipment in shipments[1:]:
            print(f"{shipment[0]:<15} {shipment[1]:<18} {shipment[2]:<18} {shipment[3]:<20} {shipment[4]:<19} {shipment[5]:<12}")
        
        print("="*100 + "\n")

    def update_shipment_status(self):
        """Update the status of a shipment."""
        if not os.path.exists(self.filename):
            print("No shipment records found.")
            return

        shipment_id = input("Enter shipment ID to update: ").strip()

        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            shipments = list(reader)

        found = False
        for i, shipment in enumerate(shipments):
            if shipment and shipment[0] == shipment_id:
                found = True
                print(f"\nCurrent status: {shipment[5]}")
                print("Status options: In Transit, Delivered, Delayed, Cancelled")
                new_status = input("Enter new status: ").strip()
                shipments[i][5] = new_status
                break

        if not found:
            print(f"Shipment ID {shipment_id} not found.")
            return

        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(shipments)
        
        print("✓ Shipment status updated successfully!")


class TruckDriverForm:
    def __init__(self, filename="truck_drivers.csv"):
        self.filename = filename
        self.initialize_file()

    def initialize_file(self):
        """Create CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Name', 'Surname', 'Age', 'Height (cm)', 
                    'Driver History (years)', 'Job Title', 'Employment Status', 'Date Added'
                ])

    def collect_information(self):
        """Collect truck driver information from user input."""
        print("\n" + "="*50)
        print("TRUCK DRIVER INFORMATION FORM")
        print("="*50 + "\n")

        # Personal Information
        name = input("Enter first name: ").strip()
        surname = input("Enter surname: ").strip()
        
        while True:
            try:
                age = int(input("Enter age: "))
                if age < 18 or age > 120:
                    print("Please enter a valid age (18-120)")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for age")

        while True:
            try:
                height = int(input("Enter height (in cm): "))
                if height < 100 or height > 250:
                    print("Please enter a valid height (100-250 cm)")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for height")

        # Driver History
        while True:
            try:
                driver_history = int(input("Enter years of driving experience: "))
                if driver_history < 0 or driver_history > 70:
                    print("Please enter a valid number of years (0-70)")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for driver history")

        # Employment Information
        job_title = input("Enter job title (e.g., Long-haul Driver, Local Delivery Driver): ").strip()
        
        employment_status = self.get_employment_status()

        # Create data entry
        driver_data = [
            name, surname, age, height, driver_history, job_title, 
            employment_status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        return driver_data

    def get_employment_status(self):
        """Get employment status from user selection."""
        statuses = ["Full-time", "Part-time", "Contract", "Freelance", "Other"]
        print("\nEmployment Status Options:")
        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status}")
        
        while True:
            try:
                choice = int(input("Select employment status (1-5): "))
                if 1 <= choice <= 5:
                    return statuses[choice - 1]
                print("Please select a valid option (1-5)")
            except ValueError:
                print("Please enter a valid number")

    def save_driver(self, driver_data):
        """Save driver information to CSV file."""
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(driver_data)
        print("\n✓ Driver information saved successfully!")

    def display_all_drivers(self):
        """Display all recorded drivers."""
        if not os.path.exists(self.filename):
            print("No driver records found.")
            return

        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            drivers = list(reader)

        if len(drivers) <= 1:
            print("No driver records found.")
            return

        print("\n" + "="*80)
        print("REGISTERED TRUCK DRIVERS")
        print("="*80)
        
        # Print header
        print(f"{'Name':<12} {'Surname':<12} {'Age':<5} {'Height':<8} {'Exp (yrs)':<10} {'Job Title':<20} {'Status':<12} {'Date Added':<19}")
        print("-"*80)
        
        # Print data rows
        for driver in drivers[1:]:
            print(f"{driver[0]:<12} {driver[1]:<12} {driver[2]:<5} {driver[3]:<8} {driver[4]:<10} {driver[5]:<20} {driver[6]:<12} {driver[7]:<19}")
        
        print("="*80 + "\n")

    def run(self):
        """Main program loop."""
        cargo_tracker = CargoTracking()
        
        while True:
            print("\n" + "="*50)
            print("MAIN MENU")
            print("="*50)
            print("1. Add new truck driver")
            print("2. View all registered drivers")
            print("3. Add new shipment/cargo")
            print("4. View all shipments")
            print("5. Update shipment status")
            print("6. Exit")
            print("="*50)
            
            choice = input("Select an option (1-6): ").strip()
            
            if choice == '1':
                driver_data = self.collect_information()
                self.save_driver(driver_data)
            elif choice == '2':
                self.display_all_drivers()
            elif choice == '3':
                shipment_data = cargo_tracker.collect_cargo_information()
                if shipment_data:
                    cargo_tracker.save_shipment(shipment_data)
            elif choice == '4':
                cargo_tracker.display_all_shipments()
            elif choice == '5':
                cargo_tracker.update_shipment_status()
            elif choice == '6':
                print("\nThank you for using the Truck Driver & Cargo Management System. Goodbye!")
                break
            else:
                print("Invalid option. Please select 1-6.")


if __name__ == "__main__":
    form = TruckDriverForm()
    form.run()
