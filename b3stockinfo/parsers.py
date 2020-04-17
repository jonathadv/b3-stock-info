import re


def number_parser(value):
    regex = r"R\$|%|\."
    value = re.sub(regex, "", value)
    if "," in value:
        value = value.replace(",", ".")
        return float(value)
    return int(value)


def name_parser(value):
    return value.split("-")[1].strip()


def ticker_parser(value):
    return value.split("-")[0].strip()
