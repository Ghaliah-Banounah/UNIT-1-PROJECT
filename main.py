import pickle
from bakery.person import *
from bakery.order import *
from bakery.cart import Cart
import re
import time

#Using Rich library to style the output on terminal
from rich import print
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.text import Text
from rich.rule import Rule
from rich.progress import track

users: list[Person] = []

def loadUsers():
    '''This function gets a list of users from a pickle file'''
    global users
    try:
        with open("bakeryData/users.pkl", "rb") as file:
            #Read the list of users from a pickle file and store it in the variable
            users = list(pickle.load(file))
    except FileNotFoundError:
        print(Text("File doesn't exist.", style="red"))
    except Exception as e:
        print(Text(f"{e}", style="red"))

def saveUsers(user: Person):
    '''This function saves users to a pickle file'''
    loadUsers()
    users.append(user)
    with open("bakeryData/users.pkl", "wb") as file:
            pickle.dump(users, file)

def updateCustomer(customer: Customer) -> Customer:
    '''
    This function updates a customer's details then saves the updated info to the list of users in a pickle file
    '''
    loadUsers()
    for user in users:
        if user.getPhone() == customer.getPhone():

            choiceList: str = "Choose what to update:\n1. Name.\n2. Age\n3. Gender.\n4. Phone number.\n5. Password.\n6. Delivery address.\n7. Back to previous menu.\nYour choice"
            choice: str = Prompt.ask(Text(choiceList, style="#fff2f2"), choices=['1','2','3','4','5','6','7'], show_choices=False)
            
            #Update name
            if choice == '1':
                newName: str = Prompt.ask("[#ffd7f0]New name[/]")
                user.setName(newName)
                print(Text("Your name was updated successfully.", style="#9affbc"))

            #Update age 
            elif choice == '2':
                newAge: int =IntPrompt.ask("[#ffd7f0]New age[/]")
                user.setAge(newAge)
                print(Text("Age was updated successfully.", style="#9affbc"))

            #Update gender
            elif choice == '3':
                #Keep asking user to enter a valid gender
                newGender: str = Prompt.ask("[#ffd7f0]New gender[/]", choices=['male','Male','female','Female'], show_choices=False)
                user.setGender(newGender)
                print(Text("Gender was updated successfully.", style="#9affbc"))

            #Update phone number
            elif choice == '4':
                #Keep asking for correct phone number format
                while True:
                    newPhone: str = Prompt.ask("[#ffd7f0]New phone number[/]")
                    if not phoneValid(newPhone):
                        print(Text("Phone number should be 10 digits starting with (05).", style= "red"), end=" ")
                        Prompt.ask("[#fff2f2]Try again..[/]")
                    else:
                        user.setPhone(newPhone)
                        print(Text("Phone was updated successfully.", style="#9affbc"))
                        break
            
            #Update password
            elif choice == '5':
                #Keep asking for correct password format
                while True:
                    newPassword: str = Prompt.ask("[#ffd7f0]New password[/]")
                    if not passwordValid(newPassword):
                        print("[red bold]Password too weak[/], [#fff2f2]your password should satisfy the following:[/]")
                        print(Text("• Be at least 8 characters long.\n• Contain 1 upper case and 1 lower case letters.\n• Contain a special character e.g(@#_)\n", style = "#fff2f2"), end =" ")
                        Prompt.ask("[#fff2f2]Try again[/]")
                    else:
                        user.setPassword(newPassword)
                        print(Text("Your password was updated successfully.", style="#9affbc"))
                        break
            
            #Update delivery address
            elif choice == '6':
                newAddress: str = Prompt.ask("[#ffd7f0]New delivery address[/]")
                #Cast user to Customer class to be able to call the following method:
                customer = user
                customer.setDeliveryAddress(newAddress)
                print(Text("Your delivery address was updated successfully.", style="#9affbc"))
            
            #Return to previous menu
            elif choice == '7':
                break
            
            #Save the update user in the customer variable then return it later
            customer = user
            Prompt.ask(Text("Press Enter to continue..", style="white italic"))
    
    #Update the list of users with the new data
    with open("bakeryData/users.pkl", "wb") as file:
            #Store list of users in a pickle file
            pickle.dump(users, file)

    return customer

def updateCustomerCart(customer: Customer, cart: Cart) -> Customer:
    '''This function updates the details of the customer's cart on the file'''
    
    #Get the list of users from the file
    loadUsers()
    #Loop over the list of users and find the customer
    for user in users:
        if user.getPhone() == customer.getPhone():
            #Update customer cart
            customer = user
            customer.setCart(cart)
            #Update the list of users with the new data
            with open("bakeryData/users.pkl", "wb") as file:
                pickle.dump(users, file)
            return customer
            
def updateCustomerOrders(customer: Customer, orders: list[Order]) -> Customer:
    '''This function updates the order history of a customer'''
    #Get the list of users from the file
    loadUsers()
    #Loop over the list of users and find the customer
    for user in users:
        if user.getPhone() == customer.getPhone():
            #Update customer's order history
            customer = user
            customer.setOrderHistory(orders)
            #Update the list of users with the new data
            with open("bakeryData/users.pkl", "wb") as file:
                pickle.dump(users, file)
            return customer

def phoneValid(phone: str) -> bool:
    '''This function validates a phone number and return true if it's valid'''
    numberPattern = r'^05[0-9]{8}$'
    return re.match(numberPattern, phone)

def passwordValid(password: str) -> bool:
    '''This function validates a password and returns true if it's valid'''
    passwordPattern = r'[A-Za-z0-9@#_+$&-]{8,}'
    return re.fullmatch(passwordPattern, password)

def checkUserLogin(phone: str, password: str) -> Person:
    '''This function searches for a user with a phone number and password, if they exists it returns the user'''
    loadUsers()
    for user in users:
        if user.getPhone() == phone and user.getPassword() == password:
            return user
        elif user.getPhone() == phone and user.getPassword() != password: 
            print(Text(f"Incorrect password for phone number {phone}", style="red"))
          
def checkUserRegister(phone: str, password: str) -> bool:
    '''This function checks if a user with the passed phone number exists. It returns True if they do and False if not'''
    loadUsers()
    for user in users:
        if user.getPhone() == phone and user.getPassword() == password:
            print(Text(f"You already have an account {user.getName()}!", style="red"))
            return True
        elif user.getPhone() == phone and user.getPassword() != password: 
            print(Text("An account with that number already exists", style="red"))
            return True
        else:
            return False            
     
def employeeMenu(employee: Employee):
    '''This function displays a menu of available actions to the employee'''

    #Keep showing the list of choices until the user enters 5
    while True:
        print(Rule(Text(f"Welcome, {employee.getName()}.. What would you like to do?", style="bold italic #e2deff"), characters="-  ", style="bold #aca2f5"))
        #Display a list of options to the employee
        choicesList: str = "1. Add a product.\n2. Remove a product.\n3. Update a product.\n4. View the menu.\n5. Exit.\nYour choice"
        choice = Prompt.ask(Text(choicesList, style = "#e7e4ff"), choices=['1','2','3','4','5'], show_choices=False)
        
        #Add product to the menu of available products
        if choice == '1':
            print(Rule(Text("Add Product", style="bold #fdffc3"), characters="- ", style="bold #fdffb0"))
            prodName: str = Prompt.ask("[bold #fbfbe2]Product name[/]")
            qty: int = IntPrompt.ask("[bold #fbfbe2]Quantity: ")
            price: float = FloatPrompt.ask("[bold #fbfbe2]Price: ")

            employee.addProduct(prodName, qty, price)
            print(Text(f"{prodName} was added successfully.", style="#9affbc"))

        #Remove product from the menu of available products
        elif choice == '2':
            print(Rule(Text("Remove Product", style="bold #fdffc3"), characters="- ", style="bold #fdffb0"))
            prodName: str = Prompt.ask("[bold #feffde]Product name[/]")
            removeMsg: str = employee.removeProduct(prodName)
            print(removeMsg)
                
        #Update product on the menu of available products
        elif choice == '3':
            print(Rule(Text("Update Product", style="bold #fdffc3"), characters="- ", style="bold #fdffb0"))
            prodName: str = Prompt.ask("[bold #feffde]Product name[/]")
            choicesList = "1. Update product name.\n2. Update product quantity\n3. Update product price.\n4. Back to main menu.\nYour choice"
            updateChoice: str = Prompt.ask(Text(choicesList, style = "#fbfbe2"), choices=['1','2','3','4'], show_choices=False)
            updateMsg: str = employee.updateProduct(prodName, updateChoice)
            print(updateMsg)
        
        #Display menu of available products
        elif choice == '4':
            menu: Table = employee.listAllProducts()
            print(menu)
        
        #Exit program
        elif choice == '5':
            for i in track(range(10), description="[white italic]Exiting program..[/]"):
                time.sleep(0.05)  # Simulate work being done
            break

        Prompt.ask(Text("Press Enter to continue..", style="white italic"))

def customerMenu(customer: Customer):
    '''This function displays a menu of available actions for the customer'''

    cart: Cart = customer.getCart()   
    #Keep showing the list of choices until the user enters 5
    while True:
        print(Rule(Text(f"Welcome, {customer.getName()}.. What would you like to do?", style="italic bold #e2deff"),characters="-  ", style="bold #aca2f5"))
        #Prompt customer for a choice and only accept one of the specified choices
        choicesList: str = "1. View bakery menu.\n2. View cart.\n3. Make New order.\n4. View my profile.\n5. Exit.\nYour choice"    
        choice = Prompt.ask(Text(choicesList, style="#e7e4ff"), choices=['1','2','3','4','5'], show_choices=False)
        #Display menu
        if choice == '1':
            menu: str = customer.listAllProducts()
            print(menu)

        #Show cart
        elif choice == '2':
            print(Rule(Text("Your Cart", style="bold #fbfbe2"), characters="- ", style="bold #fdffb0"))
            #Keep displaying cart options to the customer until they enter 5
            while True:
                cartInfo = cart.viewCart()
                #Display cart contents if they exist
                print(cartInfo)
                choicesList = "1. Add to cart.\n2. Remove from cart.\n3. Update product quantity.\n4. Clear cart.\n5. Proceed to checkout.\n6. Back to previous menu.\nYour choice"
                cartChoice: str = Prompt.ask(Text(choicesList, style="#fbfbe2"), choices=['1','2','3','4','5','6'], show_choices=False)
                
                #Add product to cart
                if cartChoice == '1':
                    print(Rule(Text("Add to Cart", style="bold #fbfbe2"), characters="- ", style="bold #fdffb0"))
                    while True:
                        print(customer.listAllProducts())
                        print(Text("Enter the name and quantity of the product you want.", style="bold #fdffc3"))
                        prodName: str = Prompt.ask("[#fbfbe2]Product name[/]")
                        #Only accepts integers from the customer
                        prodQty: int = IntPrompt.ask("[#fbfbe2]Quantity[/]")
                        #Add the new product to the cart
                        cart.addToCart(prodName, prodQty)
                        customer = updateCustomerCart(customer, cart)
                        print(Text(f"{prodName} was successfully added to your cart.", style="#9affbc"))
                        
                        #Keep asking customer if they want to add more items to their cart until they enter n
                        addMore: bool = Confirm.ask(Text("Add more products?", style="bold #feffde"))
                        if addMore:
                            continue
                        elif not addMore:
                            break

                #Remove product from cart            
                elif cartChoice == '2':
                    print(Rule(Text("Remove from Cart", style="bold #fbfbe2"), characters="- ", style="bold #fdffb0"))
                    prodName: str = Prompt.ask(Text("Enter the name of the product you want to remove", style="bold #fbfbe2"))
                    isRemoved: bool = cart.removeFromCart(prodName)
                    if isRemoved:
                        customer = updateCustomerCart(customer, cart)
                        print(Text(f"{prodName} has been successfully removed from cart.", style="#9affbc"))
                    else: 
                        print(Text(f"{prodName} is not in your cart.", style="red"))
                
                #Update cart contents
                elif cartChoice == '3':
                    print(Rule(Text("Update Cart", style="bold #fbfbe2"), characters="- ", style="bold #fdffb0"))
                    prodName: str = Prompt.ask(Text("Enter the name of the product you want to update", style="bold #fbfbe2"))
                    #Only accepts integers from the customer
                    newQty: int = IntPrompt.ask(Text("New quantity", style="bold #fbfbe2"))
                    isUpdated: bool = cart.updateCart(prodName, newQty)
                    if isUpdated:
                        customer = updateCustomerCart(customer, cart)
                        print(Text(f"{prodName}'s quantity has been successfully updated.", style="#9affbc"))
                    else:
                        print(Text(f"{prodName} is not in your cart.", style="red"))
                
                #Clear cart
                elif cartChoice == '4':
                    isCleared: bool = cart.clearCart()
                    if isCleared:
                        customer = updateCustomerCart(customer, cart)
                        print(Text("Your cart has been cleared.", style="#9affbc"))
                    else:
                        print(Text("Your cart is already empty.", style="red"))
                    break
                
                #Checkout 
                elif cartChoice == '5':
                    print(Rule(Text("Checkout", style="bold #feffde"), characters="- ", style="bold #fdffb0"))
                    paymentMethod: str = Prompt.ask(Text("Payment method:\n1. Credit Card.\n2. Cash.\nYour choice", style="#fbfbe2",), choices=['1','2'], show_choices=False)
                    payment: str = ""
                    #Set payment value based on customer choice of payment method
                    if paymentMethod == '1':
                        #Check that the cutomer enters valid values
                        while True:
                            ccNumber: int = IntPrompt.ask("[#fbfbe2]Enter your credit card's number[/]")
                            #Credit card should have 16 digits
                            if ccNumber > 9999999999999999 or ccNumber < 1000000000000000:
                                print("[red]Please enter a valid credit card number.[/]")
                                continue
                            cvv: int = IntPrompt.ask("[#fbfbe2]Enter the cvv[/]")
                            if cvv > 999 or cvv < 100:
                                print("[red]Please enter a valid cvv number.[/]")
                                continue
                            break 
                        payment = "Credit Card"
                            
                    elif paymentMethod == '2':
                        payment = "Cash"
                    
                    #Delivery option 
                    deliver: bool = Confirm.ask(Text(f"Do you want delivery?\nP.S: Delivery cost 10SR", style="#fdffc3"))
                    if deliver:
                        deliverTo: str = customer.getDeliveryAddress()
                        #Show the current delivery address and ask customer if they want to deliver to a different address
                        print(Text.assemble("[bold #fdffc3]Order will be deliverd to:[/]", f"[italic #fbfbe2],{deliverTo}[/]"))
                        changeAddress: bool = Confirm.ask(Text("Do you want to change the delivery address?", style="#fdffc3"))
                        #If the customer wants to change the address, prompt them for the new address
                        if changeAddress:
                            deliverTo = Prompt.ask(Text("Enter the new delivery address", style="#fdffc3"))
                        #Create the new order object
                        newOrder: Order = Order(cart.getOrderedProducts(), payment, deliver, deliverTo)
                    else:
                        newOrder: Order = Order(cart.getOrderedProducts(), payment)
                    #Get the list of customer's order history and add the new order to them 
                    orders: list[Order] = customer.getOrderHistory()
                    orders.append(newOrder)

                    #Update the list of users with the new data
                    customer = updateCustomerOrders(customer, orders)
                    print(Text("Order was successfully completed.", style="#9affbc"))
                    print(Rule(Text("Thank you for shopping at Stellar Bakery, come again soon!", style="bold #e7e4ff"), characters="- ", style="italic bold #aca2f5"))
                    
                    #Clearing cart
                    cart = Cart()
                    customer = updateCustomerCart(customer, cart)
                    break

                #Back to previous menu
                elif cartChoice == '6':
                    break

                Prompt.ask(Text("Press Enter to continue..", style="white italic"))
        
        #Create a new order       
        elif choice == '3':
            print(Rule(Text("Make New Order", style="bold #feffde"), characters="-", style="bold #fdffc3"))

            #To make a new order contents of the cart will be cleared
            cart.clearCart()
            #Display menu to the user
            print(customer.listAllProducts())
            print(Text("Enter the name and quantity of the product you want.", style="bold #fdffc3"))
            prodName: str = Prompt.ask("[#feffde]Product name[/]")
            #Only accepts integers from the user
            prodQty: int = IntPrompt.ask("[#feffde]Quantity[/]")
            cart.addToCart(prodName, prodQty)
            customer = updateCustomerCart(customer, cart)
            print(Text(f"{prodName} was successfully added to your cart.", style="#9affbc"))

        #View and Update profile 
        elif choice == '4':
            print(Rule(Text("My Profile", style="bold #aceaff"), characters="-", style="bold #5dd6ff"))
            print(customer.getInfo())

            updateProfile: str = Confirm.ask(Text("Would you like to update your profile?", style="#aceaff"))
            if updateProfile:
                print(Rule(Text("Update Profile", style="bold #aceaff"), characters="-", style="bold #5dd6ff"))
                customer = updateCustomer(customer)
            elif not updateProfile:
                pass
        
        #Exit program
        elif choice == '5':
            for i in track(range(10), description="[white italic]Exiting program..[/]"):
                time.sleep(0.05)  # Simulate work being done
            break
        
        Prompt.ask(Text("Press Enter to continue..", style="white italic"))

#Main program
def main():
    '''
    Function that contains all main operations
    '''
    choice: str = ""
    while choice != '1':
        print(Rule(Text("Welcome to Stellar Bakery", style="bold italic #f0cfff"), characters="- ", style="bold #e09eff"))
        choice = Prompt.ask("[#f5e6fc]1. Login.\n2. Register.\nYour choice[/]", choices=['1','2'], show_choices=False)
        
        #Login
        if choice == '1':
            while True:
                print(Rule(Text("Login", style="bold #bdeeff"), characters="- ", style="bold #5dd6ff"))
                phone: str = Prompt.ask("[#daf5ff]Enter your phone number[/]")
                #Check if phone number is valid
                if not phoneValid(phone):
                    print(Text("Phone number should be 10 digits starting with (05).", style= "red"), end=" ")
                    Prompt.ask("[#fff2f2]Try again..[/]")
                    continue
                password: str = Prompt.ask("[#daf5ff]Enter your password[/]")

                #Check if the user exists in the system, returns None if the user doesn't
                user: Person = checkUserLogin(phone, password)
                if user != None:
                    some: Customer = user
                    #Display the appropriate main menu for each of the employee and the customer
                    if user.getRole() == "employee":
                        employeeMenu(user)
                        break
                    elif user.getRole() == "customer":
                        customerMenu(user)
                        break
                else:
                    print(Text("There is no account with that phone number.", style= "red"))
                    Prompt.ask(Text("Press Enter to continue..", style="white italic"))
                    #Change choice value to break out of the loop
                    choice = '0'
                    break
        
        #Register
        elif choice == '2':
            while True:
                print(Rule(Text("Register", style="bold #bdeeff"), characters="- ", style="bold #5dd6ff"))
                name: str = Prompt.ask("[#daf5ff]Enter your name[/]")
                #Only accepts integers from the user
                age: int = IntPrompt.ask("[#daf5ff]Enter your age[/]")
                #Keep asking user to enter a valid gender
                gender: str = Prompt.ask("[#daf5ff]Enter your gender[/]", choices=['male','Male','female','Female'], show_choices=False)
                phone: str = Prompt.ask("[#daf5ff]Enter your phone number[/]")
                #Validate phone format
                if not phoneValid(phone):
                    print(Text("Phone number should be 10 digits starting with (05).", style= "red"), end=" ")
                    Prompt.ask("[#fff2f2]Try again..[/]")
                    continue
                password: str = Prompt.ask("[#daf5ff]Enter your password[/]")
                #Validate password format
                if not passwordValid(password):
                    print("[red bold]Password too weak[/], [#f5cda4]your password should satisfy the following:[/]")
                    print(Text("• Be at least 8 characters long.\n• Contain 1 upper case and 1 lower case letters.\n• Contain a special character e.g(@#_)\n", style = "#fff2f2"), end =" ")
                    Prompt.ask("[#fff2f2]Try again..[/]")
                    continue
                deliveryAddress: str = Prompt.ask("[#daf5ff]Enter your delivery address[/]")
                    
                #Check if the user exists in the system, returns False if they don't
                exist: bool = checkUserRegister(phone, password)
                if not exist:
                    customer: Customer = Customer(name, age, gender, phone, password, deliveryAddress)
                    #Store the created customer account in a pickle file with the rest of the users
                    saveUsers(customer)
                    print(Text("You have successfully registered, continue to login.", style="#9affbc"))
                break
            Prompt.ask(Text("Press Enter to continue..", style="white italic"))
        

#Executing main program
main()