
# name -> {"price": int, "stock": int}
products = {
    "shirt": {"price": 1500, "stock": 20},
    "jeans": {"price": 3000, "stock": 15},
    "shoes": {"price": 4000, "stock": 10},
    "tshirt": {"price": 1200, "stock": 25},
    "jacket": {"price": 5000, "stock": 8},
    "trouser": {"price": 2500, "stock": 12},
    "hoodie": {"price": 3500, "stock": 10},
    "cap": {"price": 800, "stock": 30},
    "belt": {"price": 1000, "stock": 18},
    "watch": {"price": 6000, "stock": 5},
    "bag": {"price": 3000, "stock": 9},
    "sunglasses": {"price": 2000, "stock": 14},
}

sales_log = []          # list of (item, qty, amount)
LINE = "=" * 40


# ---------- helpers ----------
def get_int(prompt, minimum=None, maximum=None):
    """Keep asking until the user enters a valid whole number in range."""
    while True:
        try:
            value = int(input(prompt))   #The program asks the user for input and converts it into an integer.
        except ValueError:               #If the user enters something that cannot be converted to an integer, such as ABC
            print("  Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"  Must be at least {minimum}.")
        elif maximum is not None and value > maximum:
            print(f"  Must be at most {maximum}.")
        else:
            return value

def get_name(prompt):
    return input(prompt).strip().lower()


def header(title):  #prints a centered title between two lines of = signs. It replaces the print lines you repeated in several places.
    print(f"\n{LINE}\n{title.center(40)}\n{LINE}")

def show_products(show_stock=True):
    header("AVAILABLE PRODUCTS")                                                    #align columns,stock of 10 shows as sold out.
    print(f"{'Item':<14}{'Price':>8}{'Stock':>8}")
    print("-" * 30)
    for name, info in sorted(products.items()):
        stock = info["stock"] if info["stock"] > 0 else "SOLD OUT"
        print(f"{name:<14}{info['price']:>8}{stock:>8}")

def show_buyer_products(show_stock=True):
    header("AVAILABLE PRODUCTS")
    print(f"{'Item':<14}{'Price':>8}")
    print("-" * 30)

    for name, info in sorted(products.items()):
        if info["stock"] > 0:
            print(f"{name:<14}{info['price']:>8}")


# ---------- seller ----------
def add_product():
    name = get_name("Product name: ")
    if not name:
        print("Name cannot be empty.")
        return
    price = get_int("Price: ", minimum=1)
    stock = get_int("Stock quantity: ", minimum=0)
    if name in products:
        products[name]["price"] = price
        products[name]["stock"] += stock
        print(f"'{name}' already existed: price updated, stock increased.")
    else:
        products[name] = {"price": price, "stock": stock}
        print(f"'{name}' added.")


def remove_product():
    name = get_name("Product to remove: ")
    if products.pop(name, None) is not None:
        print(f"'{name}' removed.")
    else:
        print("Product not found.")


def update_price():
    name = get_name("Product name: ")
    if name in products:
        products[name]["price"] = get_int("New price: ", minimum=1)
        print("Price updated.")
    else:
        print("Product not found.")


def restock():                                                                    #shirt stock = 20
    name = get_name("Product name: ")                                             #Quantity to add: 10
    if name in products:                                                          #shirt stock = 30
        products[name]["stock"] += get_int("Quantity to add: ", minimum=1)
        print("Stock updated.")
    else:
        print("Product not found.")


def sales_report(): # goes through sales-log and adss up the quantity and money
    header("SALES REPORT")                            #per item in a dictionary called totals.
    if not sales_log:                                      # then print each item and total the reveneue
        print("No sales yet.")
        return
    totals = {}
    for item, qty, amount in sales_log:
        q, a = totals.get(item, (0, 0))
        totals[item] = (q + qty, a + amount)
    for item, (q, a) in totals.items():
        print(f"{item:<14} x{q:<4} Rs {a}")
    print("-" * 30)
    print(f"Total revenue: Rs {sum(a for _, a in totals.values())}")


def seller_menu():
    actions = {
        "1": ("Add Product", add_product),
        "2": ("Remove Product", remove_product),
        "3": ("Update Price", update_price),
        "4": ("Restock", restock),
        "5": ("Show Products", show_products),
        "6": ("Sales Report", sales_report),
    }
    while True:
        header("SELLER MENU")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("7. Back")
        choice = input("Enter your choice: ").strip()
        if choice == "7":
            print("Returning to main menu...")
            return
        if choice in actions:
            actions[choice][1]()
        else:
            print("Invalid choice. Select 1-7.")


# ---------- buyer ----------                                                    # 1.creates empty cart
def buy():                                                                       # 2.it loops, asking for items
    cart = {}   # item -> quantity
    show_buyer_products()                                                # 3.done emd the loop cart shows whats in the cart
                                                              # 4.unknown item print item not found and
                                                                                    #contiune to loop.
    while True:                                                                  # 5. available
                                                                                 # 6. get in
        item = get_name("\nItem to buy ('done' to checkout, 'cart' to view): ")  # 7. cart. get
                                                                                 # 8. checkout
        if item == "done":
            break
        if item == "cart":
            for n, q in cart.items():
                print(f"  {n} x{q} = Rs {products[n]['price'] * q}")
            continue
        if item not in products:
            print("Item not found.")
            continue

        info = products[item]
        available = info["stock"] - cart.get(item, 0)
        if available <= 0:
            print("Sorry, no more stock for this item.")
            continue

        print(f"Price: Rs {info['price']}  |  Available: {available}")
        qty = get_int("Quantity (0 to cancel): ", minimum=0, maximum=available)
        if qty:
            cart[item] = cart.get(item, 0) + qty
            print(f"Added {qty} x {item}.")

    checkout(cart)


def checkout(cart):                         # if cart is empty it says no and return
    if not cart:                              # otherwise each item calculate,reduce stock, records sale,print receipt line

        print("\nYour cart is empty.")
        return

    header("RECEIPT")
    subtotal = 0
    for item, qty in cart.items():
        amount = products[item]["price"] * qty
        subtotal += amount
        products[item]["stock"] -= qty
        sales_log.append((item, qty, amount))
        print(f"{item:<14} x{qty:<3} Rs {amount}")

    discount = subtotal * 10 // 100 if subtotal >= 10000 else 0        # dicount line is subtotal
    print("-" * 30)
    print(f"Subtotal:  Rs {subtotal}")
    if discount:
        print(f"Discount (10% on orders of Rs 10000+): -Rs {discount}")
    print(f"TOTAL:     Rs {subtotal - discount}")
    print(LINE)
    print("Thank you for shopping with us!")


# ---------- main ----------
def main():
    header("WELCOME TO OUR STORE")
    while True:
        header("CHOOSE YOUR ROLE")
        print("1. Buyer\n2. Seller\n3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            buy()
        elif choice == "2":
            seller_menu()
        elif choice == "3":
            print("\nThank you for visiting our store. Have a great day!")
            break
        else:
            print("Invalid choice. Select 1, 2 or 3.")


if __name__ == "__main__":
    main()