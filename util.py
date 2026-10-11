def money(value_in_cents: int, disable_color: bool = False):
    as_money = f"${value_in_cents/1000:.2f}"
    if not disable_color:
        color = "green" if value_in_cents > 0 else "red"
        return f":{color}[{as_money}]"
    return as_money