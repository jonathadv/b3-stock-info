from typing import List, Callable
from requests import Response
from requests_html import HTMLSession
from .serializers import JsonSerializer
from .selectors import STOCK_SELECTORS, REIT_SELECTORS


class Stock(JsonSerializer):
    def __init__(self, **kwargs):
        super()
        self._ticker = None
        self._name = None
        self._currentValue = None
        self.__dict__.update(kwargs)

    def attributes(self, display_dunder: bool = False):
        attrs = []
        for k in self.__dict__.keys():
            if k.startswith("_") and not display_dunder:
                continue
            attrs.append(k)

        return attrs

    def __str__(self):
        return str(self.to_json())

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ticker='{self._ticker}', "
            f"name='{self._name}', "
            f"value={self._currentValue})"
        )


class StockFactoryError(Exception):
    pass


class StockFactory:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.session = HTMLSession()
        self.timeout = timeout

    def create(self, ticker: str, is_reit: bool = False) -> Stock:
        url = self.base_url % ticker

        try:
            payload: Response = self.session.get(url, timeout=self.timeout)
        except Exception as err:
            raise StockFactoryError(f"Unable connect.", err)

        if "/error" in payload.url:
            raise StockFactoryError(f"Unable to find Stock ticker `{ticker}` in B3")

        attrs = self.get_attributes(payload, is_reit)
        return Stock(**attrs)

    def get_attributes(self, payload: Response, is_reit: bool):
        selectors = REIT_SELECTORS if is_reit else STOCK_SELECTORS

        attrs = {}
        for field, args in selectors.items():
            value = self.get_value(payload, args["selector"], args["parsers"])
            attrs[field] = value
            if args.get("canonical"):
                attrs[args.get("canonical")] = value

        return attrs

    @staticmethod
    def get_value(payload: Response, selector: str, parsers: List[Callable] = None):
        if not parsers:
            parsers = []

        try:
            value = payload.html.find(selector)[0].text
            for parser in parsers:
                value = parser(value)

            return value

        except Exception as err:
            return None
