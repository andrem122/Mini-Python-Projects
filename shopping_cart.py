#Shopping Cart Project

options = """
Select an Option Below:
1. Add item to cart
2. Remove item from cart
3. View Cart
0. Exit
"""

#print options to user
print options

#user selects an option
selected_option = input('Enter an option: ')

#initialize variables
item = ''
quantity = 0
shopping_cart = {}

while selected_option != 0:
    
    if selected_option == 1:
        item = raw_input('Enter the item: ')

        #if item already exists update quantity
        if item in shopping_cart:
            update_quantity_text = """Item already exists. Update Quantity?
                1. Yes
                2. No"""
            
            update_quantity_option = input(update_quantity_text)
            
            if update_quantity_option == 1:
                quantity = raw_input('Enter the quantity: ')
                shopping_cart[item] = quantity

            selected_option = input('Enter an option: ')
            continue
            
        quantity = raw_input('Enter the quantity: ')
        shopping_cart[item] = quantity
        
    elif selected_option == 2:

        #check if shopping cart is empty
        if bool(shopping_cart) is False:
            print 'No items in shopping cart'
        else:
            item = raw_input('Enter the item you want removed: ')
            
            #check if item is in shopping cart
            if item not in shopping_cart:
                print 'No item found. Please try again'
            else:
                del(shopping_cart[item])
                print item + ' removed from the shopping cart'

    elif selected_option == 3:
        if bool(shopping_cart) is False:
            print 'No items in shopping cart'
        else:
            for item in shopping_cart.keys():
                print 'Item: ' + item + ', ' + 'Quantity: ' + shopping_cart[item]
    else:
        print 'Invalid input. Please try again.'
        

    selected_option = input('Enter an option: ')


print 'You have exited the shopping cart'


