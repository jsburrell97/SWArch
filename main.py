from classes import *

cart = Cart() #creating user and cart object
user = User(cart)

login = False

while(login == False): #cycles until user logs out

    username = input("\nEnter your username: ")
    password = input("Enter your password: ")
    print("\n")

    if(user.login(username, password)): #checks credentials against whats stored in the user's file

        login = True
        print("Successful Login!\n")

    else:

        print("Login Failed!\n")

print("------------------------------------------------------------")

logout = False
while(logout == False): #checks if you have logged out

    print("\n1) View Items") #prints menu to screen
    print("2) Checkout")
    print("3) View Cart")
    print("4) Logout")
    print("5) View Purchase Record")
    
    action = input("Choose an option: ")
    print()

    if(action == "1" or action == "2" or action == "3" or action == "4" or action == "5"):

        if(action == "1"): #shows items
            
            name = ""
            category = ""
            description = ""
            price = 0.0

            item_amount = 0
            end_of_file = False

            file = open("items.txt", "r")

            back_to_menu = False
            
            while(back_to_menu == False): #displays item data
                
                quantity = file.readline().rstrip()
                name = file.readline().rstrip()
                category = file.readline().rstrip()
                description = file.readline().rstrip()
                price = file.readline().rstrip()

                new_quantity = quantity.split()

                if(len(new_quantity) > 0):

                    print("Name:", name)
                    print("Category:", category)
                    print("Description:", description)
                    print("Price: $", price, sep = "")
                        
                    new_quantity = new_quantity[len(new_quantity) - 1] 

                    print("Quantity:", int(new_quantity), "\n")

                    print("(Next item will be displayed when you finish interacting with this one)\n")
                    add_item = input("Would you like to add this item to your cart?(y/n): ") #choose to add item
                    
                    while(add_item != "y" and add_item != "n"): #input verification

                        add_item = input("Please enter (y/n): ")

                    if(add_item == "y"):
                            
                        item_amount = input("How many of this item would you like to add?: ") #enters the number of items to add to the cart
                        print("\n")    

                        while(item_amount.isdigit() != True or int(item_amount) < 0):

                            item_amount = input("Please enter a positive integer: ")

                        while(int(item_amount) > int(new_quantity)):

                            item_amount = input("Item does not have that much in stock! Please enter a valid number of items: ")

                        if(int(new_quantity) > 0):
                        
                            count = 0

                            for x in range(0, int(item_amount)): #adds items to cart

                                temp_item = Item()
                                
                                temp_item.name = name
                                temp_item.category = category
                                temp_item.description = description
                                temp_item.price = float(price)
                                
                                user.cart.total_price += float(price)
                                user.cart.list_of_items.append(temp_item)

                                new_quantity = quantity.split()
                                new_quantity_numbers = new_quantity[len(new_quantity) - 1]
                                new_quantity_numbers = str(int(new_quantity_numbers) - 1)
                                new_quantity[len(new_quantity) - 1] = new_quantity_numbers
                                new_quantity = ' '.join(new_quantity)
                                
                                read_file = open("items.txt", "r")
                                filedata = read_file.read()
                                read_file.close()

                                filedata = filedata.replace(quantity, new_quantity)

                                write_file = open("items.txt", "w")
                                write_file.write(filedata)
                                write_file.close()

                                count += 1

                            print("Added", count, temp_item.name, "to your cart!")

                else:

                    file.close()
                    print("No more items to display!")
                    back_to_menu = True

        if(action == "2"): #checks out cart

            print("The total comes to $", user.cart.total_price, sep = "")
            OSC = input("Please enter your OSC Card Number: ") #input OSC number

            OSC_check = False
            
            while(OSC_check == False):

                if(OSC.isnumeric()):

                    OSC_check = True

            shipping = input("Please enter the shipping address: ") #input shipping address

            confirm = input("Confirm purchase? (y/n): ") #confirm checkout

            while(confirm != "y" and confirm != "n"):

                confirm = input("Confirm purchase? (y/n): ")

            if(confirm == "y"):

                purchase_record = open(username + "_record.txt", "a") #writes purchase data to user's purchase file
                purchase_record.write("--------------------------PURCHASES---------------------------\n")
                
                for x in range(0, len(user.cart.list_of_items)):

                    purchase_record.write("Name: " + user.cart.list_of_items[x].name + "\n")
                    purchase_record.write("Category: " + user.cart.list_of_items[x].category + "\n")
                    purchase_record.write("Description: " + user.cart.list_of_items[x].description + "\n")
                    purchase_record.write("Price: $" + str(user.cart.list_of_items[x].price) + "\n\n")
                    
                purchase_record.write("Total: $" + str(user.cart.total_price) + "\n")
                purchase_record.write("OSC:" + OSC + "\n")
                purchase_record.write("Shipping Address: " + shipping + "\n\n")
                
                purchase_record.close()
                
                user.cart.total_price = 0.0
                user.cart.list_of_items.clear()
                   

        if(action == "3"): #prints cart to the screen

            user.view_cart()

            if(len(user.cart.list_of_items) > 0):
                
                remove_item = input("Would you like to remove an item from your cart(y/n):")

                while(remove_item != "y" and remove_item != "n"):

                    remove_item = input("please enter y/n: ")

                if(remove_item == "y"):
                    
                    item_removed = input("Enter the position in the cart of the item you want to remove (Ex. 1 = first item): ")

                    while(int(item_removed) < 0 and int(item_removed) > len(user.cart.list_of_items)):

                        cart_capacity = len(user.cart.list_of_items)
                        item_removed = input("Please enter a valid number(1 - ", cart_capacity, "): ", sep = "")      

                    user.cart.total_price -= user.cart.list_of_items[int(item_removed) - 1].price
                    user.cart.list_of_items.pop(int(item_removed) - 1)
                    print("Item removed!")

            else:

                print("Your cart is empty!")
            
        if(action == "4"): #logs out

            logout = True

        if(action == "5"): #views user's purchase record

            view_record = open(username + "_record.txt", "r")

            data = view_record.read()

            view_record.close()

            print(data)

    else:
        
        print("Please choose a valid option!")

print("Thank you!")
