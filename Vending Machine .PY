import os

class VendingMachine:
    def __init__(self):
        self.items = {
            'Snacks': [("Lays", 1.0, 10), ("Takis", 2.5, 8), ("Oman Chips", 1.5, 12),
             ("Kukure", 2.0, 15), ("Cheetos", 1.5, 9)],
            'Drinks': [("Dew", 1.0, 20), ("Pepsi", 1.5, 18), ("Sprite", 1.5, 16), ("Redbull", 3.0, 10),
             ("Coffee", 2.0, 10), ("Laban", 1.0, 12), ("Karak Chai", 1.5, 15)],
            'Sweets': [("Baklava", 3.0, 10), ("Luqaimat", 2.5, 8), ("Knafeh", 4.0, 12),
             ("Basbousa", 3.0, 10), ("Umm Ali", 3.5, 9)]
        }
        self.selected_items = []
        self.money_inserted = 0.0
        self.total_cost = 0.0
        self.amount_paid = 0.0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_money_input(self):
        self.clear_screen()
        print("\033[1;36m====================================\033[0m")
        print("\033[1;36m           VENDING MACHINE          \033[0m")
        print("\033[1;36m====================================\033[0m")
        print("\n\033[1;34m-- Available Categories --\033[0m")
        for i, category in enumerate(self.items.keys(), 1):
            print(f"{i}. {category}")
        print("\n-- Money Insertion --")
        while True:
            try:
                self.money_inserted = float(input("Enter your money (in AED): "))
                if self.money_inserted >= 0.0:
                    break
                else:
                    print("Please enter a valid positive amount.")
            except ValueError:
                print("Please enter a valid number.")

    def display_menu(self, category):
        self.clear_screen()
        print("\033[1;36m====================================\033[0m")
        print(f"\033[1;36m          {category.upper()} MENU           \033[0m")
        print("\033[1;36m====================================\033[0m")
        for i, (item, price, quantity) in enumerate(self.items[category], 1):
            print(f"\033[1;33m{i}. {item}\033[0m ({quantity} left) - \033[1;32m{price} AED\033[0m")

    def select_item(self, category, item_index):
        if 1 <= item_index <= len(self.items[category]):
            item = self.items[category][item_index - 1]
            try:
                quantity = int(input(f"How many '{item[0]}' do you want to purchase? (1-{item[2]}): "))
                if 1 <= quantity <= item[2]:
                    item_price = item[1] * quantity
                    if self.money_inserted >= item_price:
                        self.selected_items.append((item[0], item[1], quantity))
                        self.items[category][item_index - 1] = (item[0], item[1], item[2] - quantity)
                        print(f"{quantity} {item[0]}{'s' if quantity > 1 else ''} added to your cart.")
                        return True
                    else:
                        print("You don't have enough money for this item.")
                else:
                    print(f"Invalid quantity. Please enter a quantity between 1 and {item[2]}.")
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")
        else:
            print("Invalid selection. Please enter a valid item number.")

    def calculate_total(self):
        return sum(item[1] * item[2] for item in self.selected_items)

    def get_billing_details(self):
        self.clear_screen()
        print("\033[1;36m====================================\033[0m")
        print("\033[1;36m         BILLING DETAILS           \033[0m")
        print("\033[1;36m====================================\033[0m")
        self.total_cost = self.calculate_total()
        print(f"\033[1;32mTotal cost: {self.total_cost} AED\033[0m")
        for item, price, quantity in self.selected_items:
            total_item_cost = price * quantity
            print(f"\033[1;33m{item} x{quantity}: {total_item_cost} AED\033[0m")
        while True:
            try:
                amount_paid = float(input("\033[1;34mEnter the amount you want to pay (in AED): \033[0m"))
                if amount_paid >= self.total_cost:
                    self.amount_paid = amount_paid
                    break
                else:
                    print("\033[1;31mAmount paid should be equal to or greater than the total cost.\033[0m")
            except ValueError:
                print("\033[1;31mPlease enter a valid number.\033[0m")

    def get_change(self):
        change = self.amount_paid - self.total_cost
        if change > 0:
            print(f"Change: {change} AED")
        else:
            print("No change due.")

    def thank_you_message(self):
        self.clear_screen()
        print("\033[1;36m====================================\033[0m")
        print("\033[1;32m   Thank you for your purchase!    \033[0m")
        print("\033[1;32m   Please visit again.             \033[0m")
        print("\033[1;36m====================================\033[0m")

    def select_category(self):
        while True:
            self.clear_screen()
            print("\033[1;36m====================================\033[0m")
            print("\033[1;36m           VENDING MACHINE          \033[0m")
            print("\033[1;36m====================================\033[0m")
            print("\n\033[1;34m-- Available Categories --\033[0m")
            for i, category in enumerate(self.items.keys(), 1):
                print(f"{i}. {category}")
            print("\n\033[1;34m-- Options --\033[0m")
            print("4. Checkout")
            print("5. Exit")
            try:
                category_choice = int(input("Select a category (1-3), Checkout (4), or Exit (5): "))
                if 1 <= category_choice <= 3:
                    category = list(self.items.keys())[category_choice - 1]
                    self.display_menu(category)
                    while True:
                        item_choice = input("Select an item (enter item number) or press 'b' to go back: ")
                        if item_choice.lower() == 'b':
                            break
                        try:
                            item_index = int(item_choice)
                            if not self.select_item(category, item_index):
                                break
                        except ValueError:
                            print("Invalid input. Please enter a valid item number or 'b' to go back.")
                elif category_choice == 4:
                    self.get_billing_details()
                    self.get_change()
                    self.thank_you_message()
                    break
                elif category_choice == 5:
                    print("Exiting the vending machine.")
                    break
                else:
                    print("Please enter a valid number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

if __name__ == "__main__":
    vending_machine = VendingMachine()
    vending_machine.get_money_input()
    vending_machine.select_category()
