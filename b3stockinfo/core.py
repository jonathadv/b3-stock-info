import json
from requests_html import HTMLSession
from .selectors import STOCK_SELECTORS, REIT_SELECTORS


class _ComplexEncoder(json.JSONEncoder):
    """ Complex Encoder """

    def default(self, obj):
        """ Default """

        if hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)


class Stock:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=False, indent=4, cls=_ComplexEncoder)


class StockFactoryError(Exception):
    pass


class StockFactory:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.session = HTMLSession()
        self.timeout = timeout

    def create(self, ticker, is_reit=False) -> Stock:
        url = self.base_url % ticker
        payload = self.session.get(url, timeout=self.timeout)

        if "/error" in payload.url:
            raise StockFactoryError(f"Unable to find Stock ticker `{ticker}` in B3")

        attrs = self.get_attributes(payload, is_reit)
        return Stock(**attrs)

    def get_attributes(self, payload, is_reit):
        selectors = REIT_SELECTORS if is_reit else STOCK_SELECTORS

        attrs = {}
        for field, args in selectors.items():
            attrs[field] = self.get_value(payload, args["selector"], args["parsers"])

        return attrs

    @staticmethod
    def get_value(payload, selector, parsers=None):
        if not parsers:
            parsers = []

        try:
            value = payload.html.find(selector)[0].text
            for parser in parsers:
                value = parser(value)

            return value

        except Exception as err:
            return None
