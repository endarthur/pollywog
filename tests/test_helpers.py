from pollywog.helpers import (
    Average,
    Sum,
    Product,
    Normalize,
    WeightedAverage,
    Scale,
    CategoryFromThresholds,
)
from pollywog.core import Number


def test_average_helper():
    n = Average("Au", "Ag", name="avg_Au_Ag")
    assert isinstance(n, Number)
    assert n.name == "avg_Au_Ag"
    assert "/ 2" in n.children[0]
    assert "[Au]" in n.children[0] and "[Ag]" in n.children[0]


def test_sum_helper():
    n = Sum("Au", "Ag", name="sum_Au_Ag")
    assert isinstance(n, Number)
    assert n.name == "sum_Au_Ag"
    assert "[Au]" in n.children[0] and "[Ag]" in n.children[0]
    assert "+" in n.children[0]


def test_product_helper():
    n = Product("Au", "Ag", name="prod_Au_Ag")
    assert isinstance(n, Number)
    assert n.name == "prod_Au_Ag"
    assert "[Au]" in n.children[0] and "[Ag]" in n.children[0]
    assert "*" in n.children[0]


def test_normalize_helper():
    n = Normalize("Au", 0, 10, name="norm_Au")
    assert isinstance(n, Number)
    assert n.name == "norm_Au"
    assert "[Au]" in n.children[0]
    assert "/ (10 - 0)" in n.children[0]


def test_weighted_average_helper():
    # Test with constant weights
    n = WeightedAverage(["Au", "Ag"], [0.7, 0.3], name="wavg_Au_Ag")
    assert isinstance(n, Number)
    assert n.name == "wavg_Au_Ag"
    assert "[Au] * 0.7" in n.children[0]
    assert "[Ag] * 0.3" in n.children[0]
    assert "/ (0.7 + 0.3)" in n.children[0] or "/ (1.0)" in n.children[0]

    # Test with variable weights
    n2 = WeightedAverage(["Au", "Ag"], ["w1", "w2"], name="wavg_Au_Ag_varw")
    assert isinstance(n2, Number)
    assert n2.name == "wavg_Au_Ag_varw"
    assert "[Au] * [w1]" in n2.children[0]
    assert "[Ag] * [w2]" in n2.children[0]
    assert "/ ([w1] + [w2])" in n2.children[0]


def test_scale_helper():
    n = Scale("Au", 2, name="Au_scaled")
    assert isinstance(n, Number)
    assert n.name == "Au_scaled"
    assert "[Au] * 2" in n.children[0]

    n2 = Scale("Ag", "factor", name="Ag_scaled")
    assert isinstance(n2, Number)
    assert n2.name == "Ag_scaled"
    assert "[Ag] * [factor]" in n2.children[0]


def test_category_from_thresholds_helper():
    n = CategoryFromThresholds(
        "Au", [0.5, 1.0], ["Low", "Medium", "High"], name="Au_class"
    )
    assert n.name == "Au_class"
    # Should contain If block
    assert hasattr(n, "children")
    assert "Classify Au by thresholds [0.5, 1.0]" in n.comment_equation


def test_sum_with_single_variable():
    """Test Sum with just one variable."""
    n = Sum("Au", name="single_sum")
    assert isinstance(n, Number)
    assert "[Au]" in n.children[0]


def test_product_with_three_variables():
    """Test Product with multiple variables."""
    n = Product("length", "width", "height", name="volume")
    assert isinstance(n, Number)
    assert "[length]" in n.children[0]
    assert "[width]" in n.children[0]
    assert "[height]" in n.children[0]


def test_average_with_many_variables():
    """Test Average with many variables."""
    n = Average("a", "b", "c", "d", "e", name="avg_five")
    assert isinstance(n, Number)
    assert "/ 5" in n.children[0]
    for var in ["a", "b", "c", "d", "e"]:
        assert f"[{var}]" in n.children[0]


def test_normalize_with_negative_range():
    """Test Normalize with negative min value."""
    n = Normalize("temperature", -10, 30, name="norm_temp")
    assert isinstance(n, Number)
    assert "[temperature]" in n.children[0]
    # Range should be 30 - (-10) = 40
    assert "40" in n.children[0] or "- -10" in n.children[0]


def test_scale_with_negative_factor():
    """Test Scale with negative factor."""
    n = Scale("value", -2.5, name="negative_scale")
    assert isinstance(n, Number)
    assert "[value]" in n.children[0]
    assert "-2.5" in n.children[0]


def test_weighted_average_edge_cases():
    """Test WeightedAverage with edge cases."""
    # Single variable
    n = WeightedAverage(["Au"], [1.0], name="single_weighted")
    assert isinstance(n, Number)
    assert "[Au]" in n.children[0]
    
    # Unequal weights
    n2 = WeightedAverage(["Au", "Ag", "Cu"], [0.5, 0.3, 0.2], name="multi_weighted")
    assert "[Au] * 0.5" in n2.children[0]
    assert "[Ag] * 0.3" in n2.children[0]
    assert "[Cu] * 0.2" in n2.children[0]


def test_category_from_thresholds_two_categories():
    """Test CategoryFromThresholds with just two categories."""
    n = CategoryFromThresholds(
        "grade", [1.0], ["Below", "Above"], name="grade_cat"
    )
    assert n.name == "grade_cat"
    assert "Classify grade by thresholds" in n.comment_equation
