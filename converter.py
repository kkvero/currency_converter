# Пример реализации функцианала конвертации валют.

from decimal import ROUND_HALF_UP, Decimal, getcontext

# Задаем точность для внутренних расчетов
getcontext().prec = 20


# Получаем курс по API
def get_rate(from_currency: str, to_currency: str) -> Decimal:
    # http request
    pass


# Основная функция приложения
def convert(amount: float, route: str) -> float:
    if amount < 0:
        raise ValueError("Значение не должно быть отрицательным.")

    supported_routes = {
        "USD->EUR",
        "GBP->BTC",
        "EUR->ETH",
        "BTC->USD",
        "ETH->GBP",
        "USD->BTC->GBP",
    }

    if route not in supported_routes:
        raise ValueError("Неподдерживаемая конвертация.")

    def round_result(value: Decimal) -> float:
        # Round to 8 decimal places using financial rounding
        return float(value.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP))

    amount = Decimal(str(amount))
    parts = route.split("->")

    if len(parts) == 2:
        rate = get_rate(parts[0], parts[1])
        return round_result(amount * rate)

    elif len(parts) == 3:
        rate1 = get_rate(parts[0], parts[1])
        intermediate = amount * rate1
        rate2 = get_rate(parts[1], parts[2])
        return round_result(intermediate * rate2)
