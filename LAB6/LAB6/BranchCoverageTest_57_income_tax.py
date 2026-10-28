
import pytest

from income_tax import taxable_income, tax_due, refund_status


# taxable_income: validation and regime branches
def test_negative_gross():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_new_regime():
    assert taxable_income(800000, "new", 0) == 725000


def test_new_regime_zero_taxable_income():
    assert taxable_income(75000, "new", 0) == 0


def test_old_regime_investments_below_limit():
    assert taxable_income(800000, "old", 100000) == 650000


def test_old_regime_investments_at_limit():
    assert taxable_income(800000, "old", 150000) == 600000


def test_old_regime_investments_above_limit():
    assert taxable_income(800000, "old", 200000) == 600000


def test_old_regime_negative_taxable_income():
    assert taxable_income(10000, "old", 0) == 0


def test_unknown_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "other", 0)


# tax_due: age exemptions and slab branches
def test_negative_taxable_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


def test_regular_exemption_boundary():
    assert tax_due(250000, 30) == 0


def test_regular_first_slab():
    assert tax_due(400000, 30) == 7500


def test_regular_second_slab_boundary():
    assert tax_due(500000, 30) == 12500


def test_regular_second_slab():
    assert tax_due(600000, 30) == 32500


def test_senior_age_59():
    assert tax_due(300000, 59) == 2500


def test_senior_age_60_exemption_boundary():
    assert tax_due(300000, 60) == 0


def test_senior_age_60_first_slab():
    assert tax_due(400000, 60) == 5000


def test_super_senior_age_79():
    assert tax_due(400000, 79) == 5000


def test_super_senior_age_80_exemption_boundary():
    assert tax_due(500000, 80) == 0


def test_super_senior_age_80_first_slab():
    assert tax_due(600000, 80) == 5000


# refund_status: positive, negative, and zero differences
def test_refund_filed_on_time():
    assert refund_status(20000, 10000, True) == "refund"


def test_refund_filed_late():
    assert refund_status(20000, 10000, False) == "refund delayed"


def test_balance_filed_on_time():
    assert refund_status(5000, 10000, True) == "pay balance"


def test_balance_filed_late():
    assert refund_status(5000, 10000, False) == "pay balance with penalty"


def test_settled_filed_on_time():
    assert refund_status(10000, 10000, True) == "settled"


def test_settled_filed_late():
    assert refund_status(10000, 10000, False) == "settled"
