import pytest
from pollywog.core import CalcSet, Number, Category, Variable, Filter, If, IfRow
from pollywog.conversion.decomp import decompile_calcset, CalcSetDecompiler

def exec_snippet(snippet):
    ns = {}
    exec(snippet, ns)
    return ns["calcset"]

def test_basic_number():
    calcset = CalcSet([
        Number("foo", ["[bar] * 2"]),
    ])
    snippet = decompile_calcset(calcset)
    regenerated = exec_snippet(snippet)
    assert [item.to_dict() for item in calcset.items] == [item.to_dict() for item in regenerated.items]

def test_grouped_loop():
    calcset = CalcSet([
        Number("out1", ["[a] + [b]"]),
        Number("out2", ["[c] + [d]"]),
    ])
    snippet = decompile_calcset(calcset)
    assert "for name, inputs, consts in" in snippet
    regenerated = exec_snippet(snippet)
    assert [item.to_dict() for item in calcset.items] == [item.to_dict() for item in regenerated.items]

def test_if_expression():
    calcset = CalcSet([
        Category(
            "grade_class",
            [If(
                rows=[IfRow(["[Au] > 1"], ["High"])],
                otherwise=["Low"]
            )]
        )
    ])
    snippet = decompile_calcset(calcset)
    regenerated = exec_snippet(snippet)
    assert [item.to_dict() for item in calcset.items] == [item.to_dict() for item in regenerated.items]
