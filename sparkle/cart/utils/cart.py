from shop.models import Product
import random

CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        # Initialize the cart with the current session
        self.session = request.session
        # Load the cart from the session or create a new one
        self.cart = self.add_cart_session()

    def __iter__(self):
        # Get the IDs of products in the cart
        product_ids = self.cart.keys()
        # Fetch the corresponding Product objects from the database
        products = Product.objects.filter(id__in=product_ids)
        # Make a copy of the cart to modify
        cart = self.cart.copy()
        # Attach product objects to the cart items
        for product in products:
            cart[str(product.id)]['product'] = product
        # Calculate the total price for each item in the cart
        for item in cart.values():
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item  # Yield each item for iteration

    def add_cart_session(self):
        # Retrieve the cart from the session
        cart = self.session.get(CART_SESSION_ID)
        # If the cart doesn't exist, create an empty cart
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        return cart  # Return the cart

    def add(self, product, quantity):
        # Get the product ID as a string
        product_id = str(product.id)

        # If the product is not already in the cart, add it
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        # Increase the quantity of the product in the cart
        self.cart.get(product_id)['quantity'] += quantity
        self.save()  # Save the updated cart to the session

    def remove(self, product):
        # Get the product ID as a string
        product_id = str(product.id)
        # If the product is in the cart, remove it
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()  # Save the updated cart to the session

    def save(self):
        # Mark the session as modified to ensure changes are saved
        self.session.modified = True

    def get_total_price(self):
        # Calculate and return the total price of all items in the cart
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Remove the cart from the session
        del self.session[CART_SESSION_ID]
        self.save()  # Save the changes to the session

    def get_total_price(self):
        # Calculate total product price in the cart
        total_product_price = sum(int(item['price']) * item['quantity'] for item in self.cart.values())
        # Return total product price plus shipping cost
        return total_product_price + self.get_shipping_price()

    def get_shipping_price(self):
        # Return a fixed shipping price
        return 15
