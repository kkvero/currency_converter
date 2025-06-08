from decimal import Decimal

import pytest

from converter import convert

# Курсы валют для тестирования.
mock_rates = {
    ("USD", "EUR"): Decimal("0.9"),
    ("GBP", "BTC"): Decimal("0.000045"),
    ("EUR", "ETH"): Decimal("0.00035"),
    ("BTC", "USD"): Decimal("67000"),
    ("ETH", "GBP"): Decimal("2800"),
    ("USD", "BTC"): Decimal("0.000015"),
    ("BTC", "GBP"): Decimal("22000"),
}


def fake_get_rate(from_currency, to_currency):
    return mock_rates[(from_currency, to_currency)]


# Заменяем get_rate на patch_get_tate перед каждым тестом.
@pytest.fixture(autouse=True)
def patch_get_rate(monkeypatch):
    monkeypatch.setattr("converter.get_rate", fake_get_rate)


##### Обычные случаи
# 1. Конвертация USD -> EUR
# Ввод: 100 USD
# Ожидаемый результат: Корректное значение в EUR по текущему курсу.
# 2. Конвертация GBP -> BTC
# Ввод: 100 GBP
# Ожидаемый результат: Корректное значение в BTC.
# 3. Конвертация EUR -> ETH
# Ввод: 1000 EUR
# Ожидаемый результат: Корректное значение в ETH.
# 4. Конвертация BTC -> USD
# Ввод: 0.01 BTC
# Ожидаемый результат: Корректное значение в USD.
# 5. Конвертация ETH -> GBP
# Ввод: 1 ETH
# Ожидаемый результат: Корректное значение в GBP.
# 6. Конвертация USD -> BTC -> GBP
# Ввод: 100 USD
# Ожидаемый результат: Промежуточный результат в BTC, финальный результат в GBP.


def test_usd_to_eur():
    assert convert(100, "USD->EUR") == pytest.approx(90.0, rel=1e-9)


def test_gbp_to_btc():
    assert convert(100, "GBP->BTC") == pytest.approx(0.0045, rel=1e-9)


def test_eur_to_eth():
    assert convert(1000, "EUR->ETH") == pytest.approx(0.35, rel=1e-9)


def test_btc_to_usd():
    assert convert(0.01, "BTC->USD") == pytest.approx(670.0, rel=1e-9)


def test_eth_to_gbp():
    assert convert(1, "ETH->GBP") == pytest.approx(2800.0, rel=1e-9)


def test_usd_to_btc_to_gbp():
    assert convert(100, "USD->BTC->GBP") == pytest.approx(33.0, rel=1e-9)


##### Крайние случаи.
# Ввод нуля
# Ввод: 0 USD -> EUR
# Ожидаемый результат: 0 EUR, без ошибок.


def test_zero_amount():
    assert convert(0, "USD->EUR") == 0.0


# Очень большая сумма (также можно протестировать очень маленькую сумму.)
# Ввод: 1,000,000,000 USD
# Ожидаемый результат: Корректная конвертация или сообщение об ограничении API.
def test_large_amount():
    assert convert(1_000_000_000, "USD->EUR") == pytest.approx(900_000_000.0, rel=1e-9)


# Высокая точность дробных значений
# Ввод: 123.456789 ETH -> GBP
# Ожидаемый результат: Точное значение с нужной точностью, без округлений раньше времени.
def test_high_precision():
    val = convert(123.456789, "USD->EUR")
    assert val == pytest.approx(float(Decimal("123.456789") * Decimal("0.9")), rel=1e-9)


# Ошибочные входные данные (Invalid Input)
# Отрицательная сумма (другие сценарии: текст вместо цифр, пустой ввод, ввод с пробелами)
# Ввод: -100 USD -> EUR
# Ожидаемый результат: Сообщение об ошибке
def test_negative_amount():
    with pytest.raises(ValueError, match="Значение не должно быть отрицательным."):
        convert(-100, "USD->EUR")


# Неподдерживаемое направление
def test_unsupported_route():
    with pytest.raises(ValueError, match="Неподдерживаемая конвертация."):
        convert(100, "EUR->USD")


# Неверный формат направления
def test_unsupported_format():
    with pytest.raises(ValueError, match="Неподдерживаемая конвертация."):
        convert(100, "USDEUR")
