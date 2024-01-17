class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ShoppingCart:
    def __init__(self):
        self.products = []
        self.discount_rules = [
            self.flat_10_discount,
            self.bulk_5_discount,
            self.bulk_10_discount,
            self.tiered_50_discount
        ]

    def add_product(self, product, quantity, gift_wrapped):
        total_amount = product.price * quantity
        self.products.append({
            'name': product.name,
            'quantity': quantity,
            'total_amount': total_amount,
            'gift_wrapped': gift_wrapped
        })

    def calculate_subtotal(self):
        return sum(product['total_amount'] for product in self.products)

    def apply_discount(self):
        total_quantity = sum(product['quantity'] for product in self.products)
        max_discount = 0
        discount_name = ""

        for rule in self.discount_rules:
            discount = rule(total_quantity)
            if discount > max_discount:
                max_discount = discount
                discount_name = rule.__name__

        return discount_name, max_discount

    def calculate_shipping_fee(self):
        total_quantity = sum(product['quantity'] for product in self.products)
        return (total_quantity // 10) * 5

    def calculate_gift_wrap_fee(self):
        return sum(product['quantity'] for product in self.products)

    def flat_10_discount(self, total_quantity):
        return 10 if self.calculate_subtotal() > 200 else 0

    def bulk_5_discount(self, total_quantity):
        return 0.05 * sum(product['total_amount'] for product in self.products
                          if product['quantity'] > 10)

    def bulk_10_discount(self, total_quantity):
        return 0.1 * self.calculate_subtotal() if total_quantity > 20 else 0

    def tiered_50_discount(self, total_quantity):
        if total_quantity > 30:
            above_15_quantity = sum(product['quantity'] - 15 for product in self.products
                                    if product['quantity'] > 15)
            return 0.5 * sum(product['total_amount'] for product in self.products
                             if product['quantity'] > 15) if above_15_quantity > 0 else 0
        return 0

    def generate_receipt(self):
        print("Product\t\tQuantity\tTotal Amount\tGift Wrapped")
        for product in self.products:
            print(f"{product['name']}\t\t{product['quantity']}\t\t${product['total_amount']}\t\t"
                  f"{'Yes' if product['gift_wrapped'] else 'No'}")

        subtotal = self.calculate_subtotal()
        discount_name, discount_amount = self.apply_discount()
        shipping_fee = self.calculate_shipping_fee()
        gift_wrap_fee = self.calculate_gift_wrap_fee()

        print("\nSubtotal:", subtotal)
        print(f"{discount_name} Discount: {discount_amount}")
        print("Shipping Fee:", shipping_fee)
        print("Gift Wrap Fee:", gift_wrap_fee)

        total = subtotal - discount_amount + shipping_fee + gift_wrap_fee
        print("\nTotal:", total)


# Product Catalog
product_a = Product("Product A", 20)
product_b = Product("Product B", 40)
product_c = Product("Product C", 50)

# User input
cart = ShoppingCart()
cart.add_product(product_a, 3, False)  # Product A, Quantity: 3, Not Gift Wrapped
cart.add_product(product_b, 12, True)  # Product B, Quantity: 12, Gift Wrapped
cart.add_product(product_c, 2, False)  # Product C, Quantity: 2, Not Gift Wrapped

# Generate receipt
cart.generate_receipt()
