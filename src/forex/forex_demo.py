from forex_python.converter import CurrencyRates
c = CurrencyRates()
print(c.get_rates('USD'))
print(c.get_rate('USD', 'GBT'))