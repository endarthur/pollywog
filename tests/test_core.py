import pytest
from pollywog.core import CalcSet, Number

from pollywog.core import Variable, Filter, If, IfRow, Category

def test_number_to_dict_and_from_dict():
    num = Number(name="n1", children=["1+2"])
    d = num.to_dict()
    num2 = Number.from_dict(d)
    assert num2.name == "n1"
    assert num2.children == ["1+2"]

def test_variable_and_filter():
    var = Variable(name="v1", children=["foo"])
    filt = Filter(name="f1", children=["bar"])
    assert var.to_dict()["type"] == "variable"
    assert filt.to_dict()["type"] == "filter"

def test_category():
    cat = Category(name="cat1", children=["'A'"])
    d = cat.to_dict()
    assert d["calculation_type"] == "string"

def test_ifrow_and_if():
    ifrow = IfRow(condition=["[x] > 0"], value=["1"])
    d = ifrow.to_dict()
    ifrow2 = IfRow.from_dict(d)
    assert ifrow2.condition == ["[x] > 0"]
    assert ifrow2.value == ["1"]

    ifexpr = If(rows=[ifrow], otherwise=["0"])
    d2 = ifexpr.to_dict()
    ifexpr2 = If.from_dict(d2)
    assert isinstance(ifexpr2, If)
    assert isinstance(ifexpr2.rows[0], IfRow)
    assert ifexpr2.otherwise == ["0"]

def test_calcset_serialization():
    num = Number(name="n1", children=["1+2"])
    var = Variable(name="v1", children=["foo"])
    cs = CalcSet([num, var])
    json_str = cs.to_json()
    cs2 = CalcSet.from_dict(cs.to_dict())
    assert isinstance(cs2, CalcSet)
    assert len(cs2.items) == 2

def test_calcset_repr():
    num = Number(name="n1", children=["1+2"])
    cs = CalcSet([num])
    s = repr(cs)
    assert s.startswith('{')

def test_calcset_add_multiple():
    num1 = Number(name="a", children=["2"])
    num2 = Number(name="b", children=["3"])
    var = Variable(name="v", children=["foo"])
    cs1 = CalcSet([num1])
    cs2 = CalcSet([num2, var])
    cs3 = cs1 + cs2
    assert len(cs3.items) == 3
    assert cs3.items[2].name == "v"

def test_error_handling():
    # Wrong type for CalcSet.from_dict
    with pytest.raises(ValueError):
        CalcSet.from_dict({"type": "not-calcset", "items": []})
    # Unknown item type
    with pytest.raises(ValueError):
        CalcSet.from_dict({"type": "calculation-set", "items": [{"type": "unknown"}]})

def test_ifrow_invalid_type():
    with pytest.raises(ValueError):
        IfRow.from_dict({"type": "not_if_row"})

def test_if_invalid_type():
    with pytest.raises(ValueError):
        If.from_dict({"type": "not_if"})

def test_calcset_to_dict():
    num = Number(name="test_num", children=["1+1"])
    calcset = CalcSet([num])
    d = calcset.to_dict()
    assert d["type"] == "calculation-set"
    assert isinstance(d["items"], list)
    assert d["items"][0]["name"] == "test_num"

def test_calcset_add():
    num1 = Number(name="a", children=["2"])
    num2 = Number(name="b", children=["3"])
    cs1 = CalcSet([num1])
    cs2 = CalcSet([num2])
    cs3 = cs1 + cs2
    assert len(cs3.items) == 2
    assert cs3.items[0].name == "a"
    assert cs3.items[1].name == "b"
