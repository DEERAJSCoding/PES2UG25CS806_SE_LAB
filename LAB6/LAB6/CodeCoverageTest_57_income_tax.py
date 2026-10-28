
import pytest

from income_tax import taxable_income, tax_due, refund_status


def test_taxable_income_new_regime():
    assert taxable_income(800000, "new", 0) == 725000


def test_taxable_income_old_regime():
    assert taxable_income(800000, "old", 100000) == 650000


def test_investment_limit():
    assert taxable_income(800000, "old", 200000) == 600000


def test_taxable_income_cannot_be_negative():
    assert taxable_income(10000, "new", 0) == 0


def test_negative_gross_income():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_unknown_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "other", 0)


def test_tax_due_negative_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


def test_tax_due_under_exemption():
    assert tax_due(200000, 30) == 0


def test_tax_due_five_percent_slab():
    assert tax_due(400000, 30) == 7500


def test_tax_due_twenty_percent_slab():
    assert tax_due(600000, 30) == 32500


def test_tax_due_senior_citizen():
    assert tax_due(400000, 65) == 5000


def test_tax_due_super_senior_citizen():
    assert tax_due(600000, 80) == 5000


def test_refund_on_time():
    assert refund_status(20000, 10000, True) == "refund"


def test_refund_delayed():
    assert refund_status(20000, 10000, False) == "refund delayed"


def test_pay_balance_on_time():
    assert refund_status(5000, 10000, True) == "pay balance"


def test_pay_balance_with_penalty():
    assert refund_status(5000, 10000, False) == "pay balance with penalty"


def test_settled():
    assert refund_status(10000, 10000, True) == "settled"
