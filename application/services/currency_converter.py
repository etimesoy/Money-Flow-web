def convert_currency(amount: int, from_currency_abbreviation: str, to_currency_abbreviation: str):
    if from_currency_abbreviation == to_currency_abbreviation:
        return amount
    converter = {
        'RUB': {
            'USD': 1 / 72,
            'EUR': 1 / 82
        },
        'USD': {
            'RUB': 72,
            'EUR': 1.16
        },
        'EUR': {
            'RUB': 82,
            'USD': 1 / 1.16
        }
    }
    return amount * converter[from_currency_abbreviation][to_currency_abbreviation]
