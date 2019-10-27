class Item:

    def __init__(self):

        name = ""
        self.category = ""
        self.description = ""
        self.price = 0.0
        

class Cart:

    def __init__(self):
        
        self.total_price = 0.0
        self.list_of_items = []
    
    
class User:

    def __init__(self, cart):

        self.cart = cart

    def login(self, username, password):

        user_file = username + ".txt"
        file = open(user_file, "r")
        checkuser = file.readline().rstrip()
        checkpass = file.readline().rstrip()
        file.close();

        if(checkuser == username and checkpass == password):

            return True

    def view_cart(self):

        for x in range(0, len(self.cart.list_of_items)):

            print("----------Item ", x + 1, "----------", sep = "")

            for y in range(0, 4):

                if(y == 0):

                    print("Name:", self.cart.list_of_items[x].name)

                if(y == 1):

                    print("Category:", self.cart.list_of_items[x].category)

                if(y == 2):

                    print("Description:", self.cart.list_of_items[x].description)

                if(y == 3):

                    print("Price: $", self.cart.list_of_items[x].price, sep = "")
                    print()
                    
        print("Total: $", self.cart.total_price, sep = "")
