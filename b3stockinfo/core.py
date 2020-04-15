import re
from requests_html import HTMLSession


class CssSelectors:
    # fmt: off
    name = "h1.lh-4"
    current_price = ".special > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)"
    min_52_week = "div.w-50:nth-child(2) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)"
    max_52_week = "div.w-50:nth-child(3) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)"
    min_month = "div.w-50:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)"
    max_month = "div.w-50:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)"
    dividend_yield = "div.w-50:nth-child(4) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    stock_type = ".top-info-md-3 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    daily_liquidity_avg = ".top-info-md-3 > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > strong:nth-child(2)"
    ibov_participation_pct = ".top-info-md-3 > div:nth-child(4) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(3) > strong:nth-child(1)"
    options_market = "strong.mr-1"

    p_vp = "div.width-auto:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_l = "div.width-auto:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_ebitda = "div.width-auto:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_ebit = "div.width-auto:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_ativo = "div.width-auto:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    # fmt: on


class Stock:
    def __init__(self, payload, **kwargs):
        self.payload = payload
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)


class StockFactoryError(Exception):
    pass


class StockFactory:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.session = HTMLSession()
        self.timeout = timeout

    def create(self, stock_code) -> Stock:
        url = self.base_url % stock_code
        payload = self.session.get(url, timeout=self.timeout)
        print(payload.raw)
        if "/error" in payload.url:
            raise StockFactoryError(f"Unable to find stock code `{stock_code}` in B3")

        attrs = self.get_attributes(payload)
        return Stock(payload, **attrs)

    def get_attributes(self, payload):
        name_code = self.parse_selector(payload, CssSelectors.name, [self.name_parser])
        # fmt: off
        attrs = {
            "code": name_code[0],
            "name": name_code[1],
            "current_price": self.parse_selector(payload, CssSelectors.current_price, [self.currency_parser]),
            "min_52_week": self.parse_selector(payload, CssSelectors.min_52_week, [self.currency_parser]),
            "max_52_week": self.parse_selector(payload, CssSelectors.max_52_week, [self.currency_parser]),
            "min_month": self.parse_selector(payload, CssSelectors.min_month, [self.currency_parser]),
            "max_month": self.parse_selector(payload, CssSelectors.max_month, [self.currency_parser]),
            "dividend_yield": self.parse_selector(payload, CssSelectors.max_month, [self.currency_parser]),
            "stock_type": self.parse_selector(payload, CssSelectors.stock_type),
            "daily_liquidity_avg": self.parse_selector(payload, CssSelectors.daily_liquidity_avg, [self.currency_parser]),
            "ibov_participation_pct": self.parse_selector(payload, CssSelectors.ibov_participation_pct, [self.currency_parser]),
            "options_market": self.parse_selector(payload, CssSelectors.options_market, [self.number_parser]),
            "p_vp": self.parse_selector(payload, CssSelectors.p_vp, [self.number_parser]),
            "p_l": self.parse_selector(payload, CssSelectors.p_l, [self.number_parser]),
            "p_ebitda": self.parse_selector(payload, CssSelectors.p_ebitda, [self.number_parser]),
            "p_ebit": self.parse_selector(payload, CssSelectors.p_ebit, [self.number_parser]),
            "p_ativo": self.parse_selector(payload, CssSelectors.p_ativo, [self.number_parser]),

        }
        # fmt: on
        return attrs

    @staticmethod
    def number_parser(value):
        value = value.replace(".", "")
        if "," in value:
            value = value.replace(",", ".")
            return float(value)
        return int(value)

    @staticmethod
    def currency_parser(value):
        value = value.replace(".", "")
        match = re.search("\d+,\d+", value)
        if match:
            return float(match[0].replace(",", "."))

    @staticmethod
    def name_parser(value):
        return [s.strip() for s in value.split("-")]

    @staticmethod
    def parse_selector(payload, selector, parsers=None):
        if not parsers:
            parsers = []

        value = payload.html.find(selector)[0].text
        for parser in parsers:
            value = parser(value)

        return value
