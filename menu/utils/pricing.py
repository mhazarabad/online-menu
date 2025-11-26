def calculate_final_price(price, discount):
    """
    Calculate final price after discount.
    """
    if price is None:
        return 0.0
    if discount and discount > 0:
        return round(float(price) * (1 - discount / 100), 2)
    return float(price)

