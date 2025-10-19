"""Integration tests for pollywog - testing complete workflows."""

import pytest
from pollywog.core import CalcSet, Number, Variable, Category, Filter, If, IfRow
from pollywog.run import run_calcset
from pollywog.helpers import Sum, Average, WeightedAverage, CategoryFromThresholds
import tempfile
from pathlib import Path


def test_complete_mining_workflow():
    """Test a complete mining grade estimation workflow."""
    # Variables for input data
    block_au = Variable(name="block_au", children=[""])
    block_ag = Variable(name="block_ag", children=[""])
    block_cu = Variable(name="block_cu", children=[""])
    block_tonnage = Variable(name="block_tonnage", children=[""])

    # Calculations for metal values
    au_price = Number(name="au_price", children=["1800"])
    ag_price = Number(name="ag_price", children=["25"])
    cu_price = Number(name="cu_price", children=["3.5"])

    # Metal values per tonne
    au_value = Number(name="au_value", children=["[block_au] * [au_price] / 31.1035"])
    ag_value = Number(name="ag_value", children=["[block_ag] * [ag_price] / 31.1035"])
    cu_value = Number(name="cu_value", children=["[block_cu] * [cu_price] * 22.046"])

    # Total value
    total_value = Sum(["au_value", "ag_value", "cu_value"], name="total_value")

    # Economic filter
    cutoff = Number(name="cutoff_grade", children=["50"])
    economic_filter = Filter(
        name="is_economic", children=["[total_value] >= [cutoff_grade]"]
    )

    cs = CalcSet(
        [
            block_au,
            block_ag,
            block_cu,
            block_tonnage,
            au_price,
            ag_price,
            cu_price,
            au_value,
            ag_value,
            cu_value,
            total_value,
            cutoff,
            economic_filter,
        ]
    )

    # Test with sample data
    inputs = {"block_au": 2.5, "block_ag": 15.0, "block_cu": 0.8, "block_tonnage": 1000}

    results = run_calcset(cs, inputs=inputs)

    # Verify calculations
    assert results["au_value"] > 0
    assert results["total_value"] > 0
    assert results["is_economic"] is True or results["is_economic"] is False


def test_dataframe_workflow_with_filtering():
    """Test a complete workflow with DataFrame input and filtering."""
    import pandas as pd

    # Create test data
    data = {
        "x": [1, 2, 3, 4, 5],
        "y": [10, 20, 30, 40, 50],
        "category": ["A", "B", "A", "B", "A"],
    }
    df = pd.DataFrame(data)

    # Create calculation set
    x_var = Variable(name="x", children=[""])
    y_var = Variable(name="y", children=[""])
    cat_var = Variable(name="category", children=[""])

    # Calculations
    sum_xy = Number(name="sum", children=["[x] + [y]"])
    prod_xy = Number(name="product", children=["[x] * [y]"])
    ratio = Number(name="ratio", children=["[y] / ([x] + 0.001)"])

    # Conditional calculation
    ifrow = IfRow(condition=["[category] == 'A'"], value=["[sum] * 2"])
    conditional = Number(
        name="weighted_sum", children=[If(rows=[ifrow], otherwise=["[sum]"])]
    )

    cs = CalcSet([x_var, y_var, cat_var, sum_xy, prod_xy, ratio, conditional])

    result_df = run_calcset(cs, dataframe=df)

    # Verify results
    assert "sum" in result_df.columns
    assert "product" in result_df.columns
    assert "ratio" in result_df.columns
    assert "weighted_sum" in result_df.columns
    assert len(result_df) == 5

    # Check specific values
    assert result_df.loc[0, "sum"] == 11
    assert result_df.loc[0, "product"] == 10
    assert result_df.loc[0, "weighted_sum"] == 22  # Category A, so doubled


def test_file_roundtrip_workflow():
    """Test saving and loading a complete workflow."""
    # Create a complex calculation set
    vars = [Variable(name=f"v{i}", children=[""]) for i in range(3)]

    # Build calculations
    calc1 = Number(name="c1", children=["[v0] + [v1]"])
    calc2 = Number(name="c2", children=["[v1] * [v2]"])
    calc3 = Number(name="c3", children=["[c1] + [c2]"])

    # Add filter
    filt = Filter(name="f1", children=["[c3] > 10"])

    cs = CalcSet(vars + [calc1, calc2, calc3, filt])

    # Save to file
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".lfcalc") as f:
        temp_path = Path(f.name)

    try:
        cs.to_lfcalc(temp_path)

        # Load back
        cs_loaded = CalcSet.read_lfcalc(temp_path)

        # Verify structure is preserved
        assert len(cs_loaded.items) == len(cs.items)

        # Run calculations with both
        inputs = {"v0": 5, "v1": 3, "v2": 2}
        results_original = run_calcset(cs, inputs=inputs)
        results_loaded = run_calcset(cs_loaded, inputs=inputs)

        # Results should match
        assert results_original["c1"] == results_loaded["c1"]
        assert results_original["c2"] == results_loaded["c2"]
        assert results_original["c3"] == results_loaded["c3"]

    finally:
        temp_path.unlink(missing_ok=True)


def test_query_and_rename_workflow():
    """Test querying and renaming in a workflow."""
    # Create items with prefixes
    vars = [
        Variable(name="input_grade", children=[""]),
        Variable(name="input_tonnage", children=[""]),
    ]

    calcs = [
        Number(name="output_metal", children=["[input_grade] * [input_tonnage]"]),
        Number(name="output_value", children=["[output_metal] * 1000"]),
    ]

    filters = [
        Filter(name="filter_economic", children=["[output_value] > 50000"]),
    ]

    cs = CalcSet(vars + calcs + filters)

    # Query for outputs
    output_items = cs.query('name.startswith("output")')
    assert len(output_items.items) == 2
    assert all("output" in item.name for item in output_items.items)

    # Query for filters
    filter_items = cs.query('item_type == "filter"')
    assert len(filter_items.items) == 1

    # Rename variables
    cs_renamed = cs.rename(
        variables={"input_grade": "grade", "input_tonnage": "tonnage"}
    )

    # Check that references are updated
    metal_calc = cs_renamed["output_metal"]
    assert "[grade]" in metal_calc.children[0]
    assert "[tonnage]" in metal_calc.children[0]
    assert "[input_grade]" not in metal_calc.children[0]

    # Test with regex rename
    cs_prefixed = cs.rename(
        items={r"^output_": "final_"}, variables={r"^input_": "raw_"}, regex=True
    )

    assert cs_prefixed.items[2].name == "final_metal"
    assert cs_prefixed.items[3].name == "final_value"


def test_complex_conditional_workflow():
    """Test complex nested conditional logic."""
    # Create a grading system with multiple nested conditions
    score = Variable(name="score", children=[""])
    attendance = Variable(name="attendance", children=[""])

    # Nested conditions: grade depends on both score and attendance
    # A: score >= 90 and attendance >= 90
    # B: score >= 80 and attendance >= 80
    # C: score >= 70 and attendance >= 70
    # F: otherwise

    a_cond = IfRow(
        condition=["([score] >= 90) and ([attendance] >= 90)"], value=["'A'"]
    )
    b_cond = IfRow(
        condition=["([score] >= 80) and ([attendance] >= 80)"], value=["'B'"]
    )
    c_cond = IfRow(
        condition=["([score] >= 70) and ([attendance] >= 70)"], value=["'C'"]
    )

    grade = Number(
        name="final_grade",
        children=[If(rows=[a_cond, b_cond, c_cond], otherwise=["'F'"])],
    )

    cs = CalcSet([score, attendance, grade])

    # Test various scenarios
    test_cases = [
        ({"score": 95, "attendance": 95}, "A"),
        ({"score": 85, "attendance": 85}, "B"),
        ({"score": 75, "attendance": 75}, "C"),
        ({"score": 65, "attendance": 65}, "F"),
    ]

    for inputs, expected_grade in test_cases:
        result = run_calcset(cs, inputs=inputs)
        assert (
            result["final_grade"] == expected_grade
        ), f"Failed for {inputs}: expected {expected_grade}, got {result['final_grade']}"


def test_helper_integration():
    """Test integration of multiple helper functions."""
    # Create dataset with multiple measurements
    v1 = Variable(name="measurement1", children=[""])
    v2 = Variable(name="measurement2", children=[""])
    v3 = Variable(name="measurement3", children=[""])
    weight1 = Variable(name="weight1", children=[""])
    weight2 = Variable(name="weight2", children=[""])
    weight3 = Variable(name="weight3", children=[""])

    # Use helpers to create calculations
    total = Sum(["measurement1", "measurement2", "measurement3"], name="total")
    avg = Average(["measurement1", "measurement2", "measurement3"], name="average")
    weighted = WeightedAverage(
        ["measurement1", "measurement2", "measurement3"],
        ["weight1", "weight2", "weight3"],
        name="weighted_average",
    )

    cs = CalcSet([v1, v2, v3, weight1, weight2, weight3, total, avg, weighted])

    inputs = {
        "measurement1": 10,
        "measurement2": 20,
        "measurement3": 30,
        "weight1": 0.5,
        "weight2": 0.3,
        "weight3": 0.2,
    }

    results = run_calcset(cs, inputs=inputs)

    assert results["total"] == 60
    assert results["average"] == 20
    # Weighted average: (10*0.5 + 20*0.3 + 30*0.2) / (0.5 + 0.3 + 0.2) = 17/1.0 = 17
    assert abs(results["weighted_average"] - 17.0) < 0.001


def test_topological_sort_integration():
    """Test that topological sort enables correct calculation order."""
    # Create calculations in wrong order
    c3 = Number(name="result", children=["[intermediate1] + [intermediate2]"])
    v1 = Variable(name="input1", children=[""])
    c2 = Number(name="intermediate2", children=["[input2] * 2"])
    v2 = Variable(name="input2", children=[""])
    c1 = Number(name="intermediate1", children=["[input1] + 1"])

    # Add in scrambled order
    cs = CalcSet([c3, v1, c2, v2, c1])

    # Should still work due to automatic topological sorting
    inputs = {"input1": 5, "input2": 10}
    results = run_calcset(cs, inputs=inputs)

    assert results["intermediate1"] == 6  # 5 + 1
    assert results["intermediate2"] == 20  # 10 * 2
    assert results["result"] == 26  # 6 + 20


def test_error_recovery_integration():
    """Test that errors in some calculations don't break the entire workflow."""
    v1 = Variable(name="x", children=[""])
    v2 = Variable(name="y", children=[""])

    # This will fail with division by zero
    bad_calc = Number(name="bad", children=["[x] / 0"])

    # These should succeed
    good_calc1 = Number(name="good1", children=["[x] + [y]"])
    good_calc2 = Number(name="good2", children=["[x] * [y]"])

    cs = CalcSet([v1, v2, bad_calc, good_calc1, good_calc2])

    inputs = {"x": 10, "y": 5}
    results = run_calcset(cs, inputs=inputs)

    # Bad calculation should return None
    assert results["bad"] is None

    # Good calculations should succeed
    assert results["good1"] == 15
    assert results["good2"] == 50
