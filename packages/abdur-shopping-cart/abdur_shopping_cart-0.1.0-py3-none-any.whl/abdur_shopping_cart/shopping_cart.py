import requests
import logging
import json


class ShoppingCart:
    _cart: dict

    def __init__(self) -> None:
        self._cart = {}
        self.base_url = "https://equalexperts.github.io/backend-take-home-test-data/"

    def add_to_cart(self, product_name: str, quantity: int) -> dict:
        """
        add_to_cart method will add the product_name, quantity and price of an item
        Given:
            A product name and a quantity
        Return:
            a successful message or failure message
        """
        try:
            if not product_name:
                raise Exception("Please enter a valid product name")

            response = requests.get(self.base_url + product_name + ".json")
            response = json.loads(response.text)
            product_price = response.get("price")

            # Handle scenario where an existing item is added to the cart
            if self._cart.get(product_name) is not None:
                quantity = quantity + self._cart.get(product_name).get("quantity")
                product_price = round(quantity * product_price, 2)

            self._cart[product_name] = {"quantity": quantity, "price": product_price}

            return {"status_code": 200, "message": "Successfully added item to cart"}

        except Exception as e:
            logging.error(f"error is {e}")
            return {"status_code": 500, "message": "Unable to add item to cart"}

    def calculate_state(self) -> str:
        """
        Return the current state of the cart.
        """
        cart_state: str = ""
        sub: float = 0
        tax: float = 0
        total: float = 0

        for key, value in self._cart.items():
            quantity = value.get("quantity")
            price = value.get("price")
            name = key

            cart_state = cart_state + f"Cart contains {quantity} x {name} \n"
            sub += price

        # Add sub total, tax and total
        tax = round(sub * (12.5 / 100), 2)
        total = round(sub + tax, 2)

        cart_state = cart_state + f"Subtotal = {sub:.2f} \n"
        cart_state = cart_state + f"Tax = {tax:.2f} \n"
        cart_state = cart_state + f"Total = {total:.2f}"

        return cart_state
