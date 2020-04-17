import copy
from .parsers import number_parser, name_parser, ticker_parser
from .units import CURRENCY, PERCENTAGE
from .formatters import fmt_currency, fmt_percentage

# fmt: off
_DEFAULT_SELECTORS = {
    "ticker": {
        "selector": "h1.lh-4",
        "parsers": [ticker_parser],
        "unit": None,
        "formatter": None,
    },
    "name": {
        "selector": "h1.lh-4",
        "parsers": [name_parser],
        "unit": None,
        "formatter": None,
    },
    "valorAtual": {
        "selector": ".special > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)",
        "parsers": [number_parser],
        "unit": CURRENCY,
        "formatter": fmt_currency,
    },
    "min52Semanas": {
        "selector": "div.w-50:nth-child(2) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "max52Semanas": {
        "selector": "div.w-50:nth-child(3) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(3)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "minMes": {
        "selector": "div.w-50:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "maxMes": {
        "selector": "div.w-50:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "dividendYield": {
        "selector": "div.w-50:nth-child(4) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
}


_STOCK_SPECIFIC_SELECTORS = {
    "tipo": {
        "selector": ".top-info-md-3 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [],
        "unit": None,
        "formatter": None,
    },
    "liquidezMediaDiaria": {
        "selector": ".top-info-md-3 > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "participacaoIbov": {
        "selector": ".top-info-md-3 > div:nth-child(4) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(3) > strong:nth-child(1)",
        "parsers": [number_parser],
        "unit": PERCENTAGE,
        "formatter": fmt_percentage,
    },
    "mercadoDeOpcoes": {
        "selector": "strong.mr-1",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "P_VP": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "P_L": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "P_EBITDA": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "P_EBIT": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "P_ATIVO": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "EV_EBITDA": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(6) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "EV_EBIT": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(7) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "PSR": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(8) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "P_CapGiro": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(9) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "P_AtivoCircularLiquido": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(10) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "margemBruta": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(11) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "margemEbitda": {
        "selector": "div.width-auto:nth-child(2) > div:nth-child(12) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "margemEbit": {
        "selector": "div.info:nth-child(13) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "margemLiquida": {
        "selector": "div.info:nth-child(14) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "giroAtivo": {
        "selector": "div.info:nth-child(15) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "roe": {
        "selector": "div.info:nth-child(16) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "roa": {
        "selector": "div.info:nth-child(17) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "roic": {
        "selector": "div.info:nth-child(18) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "lpa": {
        "selector": "div.info:nth-child(19) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "vpa": {
        "selector": "div.info:nth-child(20) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },

}

_REIT_SPECIFIC_SELECTORS = {
    "liquidezMediaDiaria": {
        "selector": ".p-0 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > strong:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
    "valorPatrimonialPorCota": {
        "selector": ".top-info-md-3 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)",
        "parsers": [number_parser],
        "unit": None,
        "formatter": None,
    },
}

STOCK_SELECTORS = copy.deepcopy(_DEFAULT_SELECTORS)
REIT_SELECTORS = copy.deepcopy(_DEFAULT_SELECTORS)

STOCK_SELECTORS.update(_STOCK_SPECIFIC_SELECTORS)
REIT_SELECTORS.update(_REIT_SPECIFIC_SELECTORS)

# fmt: on
