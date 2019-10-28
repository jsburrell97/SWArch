from classes import *

cart = Cart()
user = User(cart)

login = False

while(login == False):

    username = input("\nEnter your username: ")
    password = input("Enter your password: ")
    print("\n")

    try:
        
        if(user.login(username, password)):

            login = True
            print("Successful Login!\n")

    except FileNotFoundError:

        print("Login Failed\n")

print("------------------------------------------------------------")

logout = False
while(logout == False):

    print("\n1) View Items")
    print("2) Checkout")
    print("3) View Cart")
    print("4) Logout")
    print("5) View Purchase Record")
    
    action = input("Choose an option: ")
    print()

    if(action == "1" or action == "2" or action == "3" or action == "4" or action == "5"):

        if(action == "1"):
            
            name = ""
            category = ""
            description = ""
            price = 0.0

            item_amount = 0
            end_of_file = False

            file = open("items.txt", "r")

            back_to_menu = False
            
            while(back_to_menu == False):
                
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
                    add_item = input("Would you like to add this item to your cart?(y/n): ")
                    
                    while(add_item != "y" and add_item != "n"):

                        add_item = input("Please enter (y/n): ")

                    if(add_item == "y"):
                            
                        item_amount = input("How many of this item would you like to add?: ")
                        print("\n")    

                        while(item_amount.isdigit() != True or int(item_amount) < 0):

                            item_amount = input("Please enter a positive integer: ")

                        while(int(item_amount) > int(new_quantity)):

                            item_amount = input("Item does not have that much in stock! Please enter a valid number of items: ")

                        if(int(new_quantity) > 0):
                        
                            count = 0

                            for x in range(0, int(item_amount)):

                                temp_item = Item()
                                
                                temp_item.name = name
                                temp_item.category = category
                                temp_item.description = description
                                temp_item.price = float(price)
                                
                                user.cart.total_price += float(price)
                                user.cart.list_of_items.append(temp_item)

                                new_quantity = quantity.split()
                                new_quantity_numbers = new_quantity[len(new_quantity) - 1]
                                new_quantity_numbers = str(int(new_quantity_numbers) - int(item_amount))
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
                    print("Select 'View Items' in the menu to see the items again!")
                    back_to_menu = True

        if(action == "2"):

            print("The total comes to $", user.cart.total_price, sep = "")
            OSC = input("Please enter your OSC Card Number: ")

            OSC_check = False
            
            while(OSC_check == False):

                if(OSC.isnumeric()):

                    OSC_check = True

            shipping = input("Please enter the shipping address: ")

            confirm = input("Confirm purchase? (y/n): ")

            while(confirm != "y" and confirm != "n"):

                confirm = input("Confirm purchase? (y/n): ")

            if(confirm == "y"):

                purchase_record = open(username + "_record.txt", "a")
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
                   

        if(action == "3"):

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
                    add_back = user.cart.list_of_items.pop(int(item_removed) - 1)
                    
                    add_back_to_inventory = open("items.txt", "r")
                    filedata = add_back_to_inventory.read()
                    add_back_to_inventory.close()

                    filedata = filedata.splitlines()

                    position = filedata.index(add_back.name)
                    quantity_text = filedata[position - 1].split()
                    new_quantity = quantity_text[len(quantity_text) - 1]
                    new_quantity = str(int(new_quantity) + 1)
                    quantity_text[len(quantity_text) - 1] = new_quantity
                    filedata[position - 1] = quantity_text

                    write_file = open("items.txt", "w")

                    for x in range(0, len(filedata) - 1):

                        if("Quantity" in filedata[x]):
                            
                            if(type(filedata[x]) == list):
                                
                                filedata[x].insert(1, " ")
                                filedata[x].insert(3, " ")
                            
                        temp_string = ''.join(filedata[x]) + "\n"                        
                        write_file.write(temp_string)

                    write_file.close()                   
                    
                    print(add_back.name, "removed!")

            else:

                print("Your cart is empty!")
            
        if(action == "4"):

            logout = True

        if(action == "5"):

            view_record = open(username + "_record.txt", "r")

            data = view_record.read()

            view_record.close()

            print(data)

    else:
        
        print("Please choose a valid option!")

print("Thank you!")
