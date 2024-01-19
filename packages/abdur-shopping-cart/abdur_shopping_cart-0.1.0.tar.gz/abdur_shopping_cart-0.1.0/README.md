# Simple Shopping Cart
This is a simple shopping cart that allows you to add items into the cart
and display the state of the cart.

## Installation

To install the library run the below command in your virtual environment

`pip install abdur-shopping-cart`

## Code style
This project makes use of black with default settings to format the code
and flake 8 as a linter.

## Usage

`
from abdur_shopping_cart.shopping_cart import ShoppingCart

cart = ShoppingCart()
print(cart.add_to_cart("cornflakes", 1))
print(cart.add_to_cart("cornflakes", 1))
print(cart.add_to_cart("weetabix", 1))
print(cart.calculate_state())
`

![Alt text](image.png)

## API

`add_to_cart(product_name, quantity)`
Takes in a product name as a string, quantity as an integer
Returns a success/failure

`calculate_state()`
Calculates the current state of the cart
Returns the product names, quantities, sub_total, tax and total

# Testing

The project uses pytest to run its tests

# Other
The .gitignore file was generated using gitignore.io
https://www.toptal.com/developers/gitignore/