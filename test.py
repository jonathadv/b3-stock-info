from b3stockinfo import StockFactory

stocks = ["flry3", "lren3"]

base_url = "https://statusinvest.com.br/acoes/%s"

factory = StockFactory(base_url)

for i in stocks:
    stock = factory.create(i)
    print(stock)
