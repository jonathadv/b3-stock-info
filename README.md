# B3 Stock Info

Work in progress...


### Setup

Run Pipenv
```
pipenv install --dev

```

### Example:


```python
>>> from b3stockinfo import StockFactory


>>> stocks = ["flry3", "petr4"]
>>> reits = ["bcff11"]
>>> base_url = "https://somesource.com.br/%s"

>>> factory = StockFactory(base_url)

>>> for i in stocks:
>>>     stock = factory.create(i)
>>>     print(stock)

>>> for i in reits:
>>>     reit = factory.create(i, is_reit=True)
>>>     print(reit)

{
    "ticker": "FLRY3",
    "nome": "FLEURY",
    "valorAtual": 22.72,
    "min52Semanas": 18.43,
    "max52Semanas": 32.8,
    "minMes": 19.21,
    "maxMes": 22.72,
    "dividendYield": 4.12,
    "tipo": "ON",
    "liquidezMediaDiaria": 87994842.79,
    "participacaoIbov": 0.494,
    "mercadoDeOpcoes": 29,
    "P_VP": 4.09,
    "P_L": 23.05,
    "P_EBITDA": 8.17,
    "P_EBIT": 12.85,
    "P_ATIVO": 1.41,
    "EV_EBITDA": 9.02,
    "EV_EBIT": 14.19,
    "PSR": 2.48,
    "P_CapGiro": 9.75,
    "P_AtivoCircularLiquido": -1.99,
    "margemBruta": 30.58,
    "margemEbitda": 30.33,
    "margemEbit": 19.28,
    "margemLiquida": 10.75,
    "giroAtivo": 0.57,
    "roe": 17.76,
    "roa": 6.13,
    "roic": 13.46,
    "lpa": 0.99,
    "vpa": 5.55
}
{
    "ticker": "PETR4",
    "nome": "PETROLEO BRASILEIRO S.A. PETROBRAS",
    "valorAtual": 15.72,
    "min52Semanas": 11.29,
    "max52Semanas": 30.81,
    "minMes": 14.3,
    "maxMes": 17.32,
    "dividendYield": 6.12,
    "tipo": "PN",
    "liquidezMediaDiaria": 2067314512.3,
    "participacaoIbov": 5.346,
    "mercadoDeOpcoes": 1092,
    "P_VP": 0.69,
    "P_L": 5.01,
    "P_EBITDA": 1.36,
    "P_EBIT": 2.51,
    "P_ATIVO": 0.22,
    "EV_EBITDA": 3.5,
    "EV_EBIT": 6.44,
    "PSR": 0.68,
    "P_CapGiro": -50.68,
    "P_AtivoCircularLiquido": -0.25,
    "margemBruta": 40.4,
    "margemEbitda": 49.74,
    "margemEbit": 27.03,
    "margemLiquida": 13.56,
    "giroAtivo": 0.33,
    "roe": 13.7,
    "roa": 4.42,
    "roic": 10.04,
    "lpa": 3.14,
    "vpa": 22.93
}
{
    "ticker": "BCFF11",
    "nome": "BTG Fundo de Fundos",
    "valorAtual": 83.35,
    "min52Semanas": 64.15,
    "max52Semanas": 118.0,
    "minMes": 76.32,
    "maxMes": 84.5,
    "dividendYield": 7.76,
    "liquidezMediaDiaria": 5771788.85,
    "valorPatrimonialPorCota": 1655218418
}

```
