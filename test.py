from b3stockinfo import StockFactory

stocks = ["flry3", "petr4"]
reits = ["bcff11"]
base_url = "https://statusinvest.com.br/acoes/%s"

factory = StockFactory(base_url)

for i in stocks:
    stock = factory.create(i)
    print(stock)

for i in reits:
    reit = factory.create(i, is_reit=True)
    print(reit)