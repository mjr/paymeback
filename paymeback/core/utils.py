import locale


def format_currency(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(value, symbol=False, grouping=True)
