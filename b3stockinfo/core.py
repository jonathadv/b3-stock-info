import re
import json
from requests_html import HTMLSession


class _ComplexEncoder(json.JSONEncoder):
    """ Complex Encoder """
    def default(self, obj):
        """ Default """

        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)


class CssSelectors:
    # fmt: off
    name = "h1.lh-4"
    current_price = ".special > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)"
    min_52_week = "div.w-50:nth-child(2) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)"
    max_52_week = "div.w-50:nth-child(3) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)"
    min_month = "div.w-50:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)"
    max_month = "div.w-50:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)"
    dividend_yield = "div.w-50:nth-child(4) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    # fmt: on


class StockCssSelectors(CssSelectors):
    # fmt: off
    stock_type = ".top-info-md-3 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    daily_liquidity_avg = ".top-info-md-3 > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > strong:nth-child(2)"
    ibov_participation_pct = ".top-info-md-3 > div:nth-child(4) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(3) > strong:nth-child(1)"
    options_market = "strong.mr-1"
    p_vp = "div.width-auto:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_l = "div.width-auto:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_ebitda = "div.width-auto:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_ebit = "div.width-auto:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_ativo = "div.width-auto:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    ev_ebitda = "div.width-auto:nth-child(2) > div:nth-child(6) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    ev_ebit = "div.width-auto:nth-child(2) > div:nth-child(7) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    psr = "div.width-auto:nth-child(2) > div:nth-child(8) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_cap_giro = "div.width-auto:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    p_ativo_circ_liq = "div.width-auto:nth-child(2) > div:nth-child(10) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    gross_margin = "div.width-auto:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    ebitda_margin = "div.width-auto:nth-child(2) > div:nth-child(12) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    ebit_margin = "div.info:nth-child(13) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    net_margin = "div.info:nth-child(14) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    giro_ativo = "div.info:nth-child(15) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    roe = "div.info:nth-child(16) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    roa = "div.info:nth-child(17) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    roic = "div.info:nth-child(18) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    lpa = "div.info:nth-child(19) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    vpa = "div.info:nth-child(20) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)"
    # fmt: on


class ReitCssSelectors(CssSelectors):
    # fmt: off
    daily_liquidity_avg = ".p-0 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > strong:nth-child(2)"
    patrimony_val_per_share = ".top-info-md-3 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)"
    # fmt: on


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
            raise StockFactoryError(f"Unable to find stock ticker `{ticker}` in B3")

        attrs = self.get_attributes(payload, is_reit)
        return Stock(**attrs)

    def get_attributes(self, payload, is_reit):
        name_ticker = self.find_selector(payload, CssSelectors.name, [self.name_parser])
        # fmt: off
        attrs = {
            "ticker": name_ticker[0],
            "name": name_ticker[1],
            "current_price": self.find_selector(payload, CssSelectors.current_price, [self.currency_parser]),
            "min_52_week": self.find_selector(payload, CssSelectors.min_52_week, [self.currency_parser]),
            "max_52_week": self.find_selector(payload, CssSelectors.max_52_week, [self.currency_parser]),
            "min_month": self.find_selector(payload, CssSelectors.min_month, [self.currency_parser]),
            "max_month": self.find_selector(payload, CssSelectors.max_month, [self.currency_parser]),
            "dividend_yield": self.find_selector(payload, CssSelectors.dividend_yield, [self.number_parser]),
        }

        # fmt: on

        if is_reit:
            attrs.update(self.get_reit_attributes(payload))
        else:
            attrs.update(self.get_stock_attributes(payload))

        return attrs

    def get_stock_attributes(self, payload):
        # fmt: of
        stock_attrs = {
            "type": self.find_selector(payload, StockCssSelectors.stock_type),
            "ibov_participation_pct": self.find_selector(payload, StockCssSelectors.ibov_participation_pct, [self.currency_parser]),
            "options_market": self.find_selector(payload, StockCssSelectors.options_market, [self.number_parser]),
            "p_vp": self.find_selector(payload, StockCssSelectors.p_vp, [self.number_parser]),
            "p_l": self.find_selector(payload, StockCssSelectors.p_l, [self.number_parser]),
            "p_ebitda": self.find_selector(payload, StockCssSelectors.p_ebitda, [self.number_parser]),
            "p_ebit": self.find_selector(payload, StockCssSelectors.p_ebit, [self.number_parser]),
            "p_ativo": self.find_selector(payload, StockCssSelectors.p_ativo, [self.number_parser]),
            "daily_liquidity_avg": self.find_selector(payload, StockCssSelectors.daily_liquidity_avg, [self.currency_parser]),
            "ev_ebitda": self.find_selector(payload, StockCssSelectors.ev_ebitda, [self.number_parser]),
            "ev_ebit": self.find_selector(payload, StockCssSelectors.ev_ebit, [self.number_parser]),
            "psr": self.find_selector(payload, StockCssSelectors.psr, [self.number_parser]),
            "p_cap_giro": self.find_selector(payload, StockCssSelectors.p_cap_giro, [self.number_parser]),
            "p_ativo_circ_liq": self.find_selector(payload, StockCssSelectors.p_ativo_circ_liq, [self.number_parser]),
            "gross_margin": self.find_selector(payload, StockCssSelectors.gross_margin, [self.number_parser]),
            "ebitda_margin": self.find_selector(payload, StockCssSelectors.ebitda_margin, [self.number_parser]),
            "ebit_margin": self.find_selector(payload, StockCssSelectors.ebit_margin, [self.number_parser]),
            "net_margin": self.find_selector(payload, StockCssSelectors.net_margin, [self.number_parser]),
            "giro_ativo": self.find_selector(payload, StockCssSelectors.giro_ativo, [self.number_parser]),
            "roe": self.find_selector(payload, StockCssSelectors.roe, [self.number_parser]),
            "roa": self.find_selector(payload, StockCssSelectors.roa, [self.number_parser]),
            "roic": self.find_selector(payload, StockCssSelectors.roic, [self.number_parser]),
            "lpa": self.find_selector(payload, StockCssSelectors.lpa, [self.number_parser]),
            "vpa": self.find_selector(payload, StockCssSelectors.vpa, [self.number_parser]),

        }
        # fmt: on
        return stock_attrs

    def get_reit_attributes(self, payload):
        # fmt: of
        reit_attrs = {
            "type": "REIT",
            "daily_liquidity_avg": self.find_selector(payload, ReitCssSelectors.daily_liquidity_avg, [self.number_parser]),
            "patrimony_val_per_share": self.find_selector(payload, ReitCssSelectors.patrimony_val_per_share, [self.currency_parser]),
        }
        # fmt: on
        return reit_attrs

    @staticmethod
    def number_parser(value):
        value = value.replace(".", "")
        value = value.replace("%", "")
        if "," in value:
            value = value.replace(",", ".")
            return float(value)
        return int(value)

    @staticmethod
    def currency_parser(value):
        value = value.replace(".", "")
        match = re.search("\d+(,\d+)?", value)
        if match:
            return float(match[0].replace(",", "."))

    @staticmethod
    def name_parser(value):
        return [s.strip() for s in value.split("-")]

    @staticmethod
    def find_selector(payload, selector, parsers=None):
        if not parsers:
            parsers = []

        try:
            value = payload.html.find(selector)[0].text
            for parser in parsers:
                value = parser(value)

            return value

        except Exception as err:
            return None
