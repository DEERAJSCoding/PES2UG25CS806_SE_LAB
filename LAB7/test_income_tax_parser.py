
from hypothesis import given, strategies as st
from income_tax_parser import clean_pan, parse_amount, parse_tax_slab


@given(st.one_of(st.text(), st.none()))
def test_clean_pan_no_crash(s):
    result = clean_pan(s)
    assert isinstance(result, str)


@given(st.one_of(st.text(), st.none()))
def test_parse_amount_no_crash(s):
    result = parse_amount(s)
    assert result is None or isinstance(result, int)


@given(st.one_of(st.text(), st.none()))
def test_parse_tax_slab_no_crash(s):
    result = parse_tax_slab(s)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 3
        and all(isinstance(value, int) for value in result)
    )
