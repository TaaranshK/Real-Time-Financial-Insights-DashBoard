def check_alert(alert, current_price):
    """
    Check if alert condition is met.
    """

    if alert.condition == "above":
        return current_price > alert.target_price

    if alert.condition == "below":
        return current_price < alert.target_price

    return False
