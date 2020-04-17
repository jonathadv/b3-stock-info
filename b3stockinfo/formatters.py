from .units import CURRENCY


def fmt_currency(value):
    return f"{CURRENCY}{value}"


def fmt_percentage(value):
    return f"{value} %"
