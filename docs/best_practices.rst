Best Practices
===============

This guide provides recommendations for effectively using pollywog in production geological modeling and resource estimation workflows.

Code Organization
-----------------

Project Structure
~~~~~~~~~~~~~~~~~

Organize your pollywog scripts in a consistent directory structure:

.. code-block:: text

    project/
    ├── scripts/
    │   ├── 01_drillhole_preprocessing.py
    │   ├── 02_block_postprocessing.py
    │   ├── 03_geometallurgy.py
    │   └── 04_economics.py
    ├── outputs/
    │   ├── drillhole_preprocessing.lfcalc
    │   ├── block_postprocessing.lfcalc
    │   └── ...
    ├── config/
    │   ├── parameters.py
    │   └── thresholds.py
    ├── tests/
    │   └── test_calculations.py
    └── README.md

Script Organization
~~~~~~~~~~~~~~~~~~~

Structure your scripts consistently:

.. code-block:: python

    """
    Drillhole Preprocessing
    =======================
    
    Purpose: Clean and transform drillhole assay data before estimation
    Author: Your Name
    Date: 2024-01-15
    Updated: 2024-03-20
    
    Inputs:
    - Au, Ag, Cu: Raw assay grades
    
    Outputs:
    - Au_clean, Ag_clean, Cu_clean: Cleaned grades
    - Au_log, Ag_log, Cu_log: Log-transformed grades for kriging
    """
    
    from pollywog.core import CalcSet, Number
    
    # Configuration
    OUTLIER_THRESHOLDS = {
        "Au": 100,  # g/t
        "Ag": 500,  # g/t
        "Cu": 5,    # %
    }
    
    EPSILON = 1e-6  # For log transforms
    
    # Main calculation set
    def create_preprocessing_calcset(metals=None, thresholds=None):
        """
        Create preprocessing calculations for drillhole data.
        
        Args:
            metals: List of metal names (default: ["Au", "Ag", "Cu"])
            thresholds: Dict of outlier thresholds (default: OUTLIER_THRESHOLDS)
        
        Returns:
            CalcSet ready to export
        """
        if metals is None:
            metals = ["Au", "Ag", "Cu"]
        if thresholds is None:
            thresholds = OUTLIER_THRESHOLDS
        
        calcs = []
        
        # Clean data
        for metal in metals:
            calcs.append(Number(
                name=f"{metal}_clean",
                children=[f"clamp([{metal}], 0, {thresholds[metal]})"],
                comment_equation=f"Remove negatives and cap at {thresholds[metal]}"
            ))
        
        # Log transforms
        for metal in metals:
            calcs.append(Number(
                name=f"{metal}_log",
                children=[f"log([{metal}_clean] + {EPSILON})"],
                comment_equation="Log transform for kriging"
            ))
        
        return CalcSet(calcs)
    
    if __name__ == "__main__":
        # Create and export
        calcset = create_preprocessing_calcset()
        calcset.to_lfcalc("outputs/drillhole_preprocessing.lfcalc")
        print(f"Exported {len(calcset.items)} calculations")

Naming Conventions
------------------

Variables
~~~~~~~~~

Use descriptive, consistent names:

.. code-block:: python

    # Good
    Au_estimated_kriging
    Cu_recovered_payable
    domain_geological
    nsr_breakeven_cutoff
    
    # Bad
    au1
    x
    temp
    calc

Follow these patterns:

- **Metal grades**: ``Au_est``, ``Cu_final``, ``Ag_recovered``
- **Transformed grades**: ``Au_log``, ``Cu_sqrt``, ``Au_normalized``
- **Domain/category**: ``domain_geo``, ``rocktype``, ``alteration_zone``
- **Economic**: ``nsr``, ``revenue_per_tonne``, ``cutoff_grade``
- **QA/QC**: ``flag_negative``, ``flag_outlier``, ``qa_status``
- **Intermediate**: ``Au_step1``, ``temp_calculation`` (minimize these)

Calculation Sets
~~~~~~~~~~~~~~~~

Name your ``.lfcalc`` files clearly:

.. code-block:: python

    # Good
    drillhole_preprocessing.lfcalc
    block_postprocessing_domain_weighted.lfcalc
    geometallurgy_recovery_model.lfcalc
    economics_nsr_calculation.lfcalc
    
    # Bad
    calcs.lfcalc
    output.lfcalc
    final.lfcalc

Include context in the filename:

- Stage: drillhole, block, mesh
- Purpose: preprocessing, postprocessing, qa_qc
- Method: domain_weighted, ml_predicted
- Version: Optional date or version number

Data Quality and Validation
----------------------------

Input Validation
~~~~~~~~~~~~~~~~

Always validate and clean input data:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    
    # Remove negative values
    Number(name="Au_positive", children=["clamp([Au], 0)"])
    
    # Cap extreme outliers
    Number(name="Au_capped", children=["clamp([Au], 0, 100)"])
    
    # Handle missing values (NaN != NaN in Leapfrog)
    Number(name="Au_default", children=[
        "if([Au] != [Au], 0.001, [Au])"  # If NaN, use 0.001
    ])

Range Checking
~~~~~~~~~~~~~~

Create flags for out-of-range values:

.. code-block:: python

    from pollywog.core import CalcSet, Number, If
    
    qa_checks = CalcSet([
        # Flag impossible values
        Number(name="flag_impossible", children=[
            If("([Au] < 0) or ([Cu] < 0) or ([density] < 0)", "1", "0")
        ]),
        
        # Flag extreme values for review
        Number(name="flag_extreme", children=[
            If("([Au] > 100) or ([Cu] > 10)", "1", "0")
        ]),
        
        # Flag missing critical data
        Number(name="flag_incomplete", children=[
            If("([domain] = '') or ([density] != [density])", "1", "0")
        ]),
    ])

Avoiding Common Errors
----------------------

Division by Zero
~~~~~~~~~~~~~~~~

Always protect against division by zero:

.. code-block:: python

    # Bad
    Number(name="ratio", children=["[numerator] / [denominator]"])
    
    # Good - add small epsilon
    Number(name="ratio", children=["[numerator] / ([denominator] + 1e-10)"])
    
    # Good - use conditional
    Number(name="ratio", children=[
        If("[denominator] != 0", "[numerator] / [denominator]", "0")
    ])
    
    # Good - clamp denominator
    Number(name="ratio", children=["[numerator] / clamp([denominator], 0.001)"])

Logarithms of Zero/Negative
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add epsilon before taking logarithms:

.. code-block:: python

    # Bad
    Number(name="Au_log", children=["log([Au])"])
    
    # Good
    Number(name="Au_log", children=["log([Au] + 1e-6)"])
    
    # Good - clamp first
    Number(name="Au_log", children=["log(clamp([Au], 1e-6))"])

Expression Complexity
~~~~~~~~~~~~~~~~~~~~~

Break complex expressions into steps:

.. code-block:: python

    # Bad - hard to read and debug
    Number(name="value", children=[
        "(([Au] * 1800 / 31.1035 * 0.88) + ([Cu] * 3.5 * 22.046 * 0.85)) * [tonnes] - ([mining_cost] + [processing_cost])"
    ])
    
    # Good - break into logical steps
    CalcSet([
        Number(name="Au_value_per_t", children=["[Au] * 1800 / 31.1035 * 0.88"]),
        Number(name="Cu_value_per_t", children=["[Cu] * 3.5 * 22.046 * 0.85"]),
        Number(name="revenue_per_t", children=["[Au_value_per_t] + [Cu_value_per_t]"]),
        Number(name="total_cost", children=["[mining_cost] + [processing_cost]"]),
        Number(name="nsr", children=["[revenue_per_t] - [total_cost]"]),
        Number(name="block_value", children=["[nsr] * [tonnes]"]),
    ])

Parentheses
~~~~~~~~~~~

Use parentheses liberally for clarity:

.. code-block:: python

    # Ambiguous
    Number(name="result", children=["[a] + [b] * [c] / [d]"])
    
    # Clear
    Number(name="result", children=["[a] + (([b] * [c]) / [d])"])

Documentation and Comments
--------------------------

Code Comments
~~~~~~~~~~~~~

Document your intent:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    
    # Create domain-weighted grades
    # Assumption: prop_oxide + prop_sulfide + prop_transition may be < 1 (waste not estimated)
    # The weighted average automatically normalizes by sum of proportions
    calcset = CalcSet([
        WeightedAverage(
            variables=["Au_oxide", "Au_sulfide", "Au_transition"],
            weights=["prop_oxide", "prop_sulfide", "prop_transition"],
            name="Au_composite",
            comment="Domain-weighted Au grade, normalized by proportion sum"
        ),
    ])

Calculation Comments
~~~~~~~~~~~~~~~~~~~~

Use ``comment_equation`` for business rules:

.. code-block:: python

    Number(
        name="Au_recovered",
        children=["[Au_diluted] * 0.88"],
        comment_equation="88% recovery per metallurgical test work (Report XYZ-2023)"
    )
    
    Number(
        name="cutoff_grade",
        children=["0.3"],
        comment_equation="Economic cutoff at $1800/oz Au, $3.50/lb Cu (Jan 2024 prices)"
    )

README Documentation
~~~~~~~~~~~~~~~~~~~~

Create a README for your project:

.. code-block:: markdown

    # Project Name - Resource Estimation Calculations
    
    ## Overview
    Automated calculation sets for [Project Name] resource estimation.
    
    ## Workflow
    1. Drillhole preprocessing: `01_drillhole_preprocessing.py`
    2. Block postprocessing: `02_block_postprocessing.py`
    3. Geometallurgy: `03_geometallurgy.py`
    4. Economics: `04_economics.py`
    
    ## Key Assumptions
    - Gold price: $1800/oz
    - Copper price: $3.50/lb
    - Gold recovery: 88%
    - Copper recovery: 85%
    - Dilution: 5%
    
    ## Dependencies
    - Python 3.8+
    - pollywog 0.1.2+
    - scikit-learn (for ML models)
    
    ## Usage
    ```bash
    python scripts/01_drillhole_preprocessing.py
    # Import outputs/drillhole_preprocessing.lfcalc into Leapfrog
    # Run estimation in Leapfrog
    python scripts/02_block_postprocessing.py
    ```

Version Control
---------------

Git Best Practices
~~~~~~~~~~~~~~~~~~

Use version control for all pollywog scripts:

.. code-block:: bash

    # Initialize repository
    git init
    git add scripts/ config/ README.md
    git commit -m "Initial commit - resource estimation calculations"
    
    # Create .gitignore
    echo "*.lfcalc" >> .gitignore  # Optional: exclude generated files
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore

Commit Messages
~~~~~~~~~~~~~~~

Write clear commit messages:

.. code-block:: bash

    # Good
    git commit -m "Update Au outlier threshold from 50 to 100 g/t"
    git commit -m "Add copper recovery model from metallurgical tests"
    git commit -m "Fix division by zero in NSR calculation"
    
    # Bad
    git commit -m "Update"
    git commit -m "Fix bug"
    git commit -m "Changes"

Configuration Management
------------------------

External Configuration
~~~~~~~~~~~~~~~~~~~~~~

Store parameters separately from code:

.. code-block:: python

    # config/parameters.py
    METAL_PRICES = {
        "Au": 1800,  # $/oz
        "Ag": 24,    # $/oz
        "Cu": 3.50,  # $/lb
    }
    
    RECOVERIES = {
        "Au": 0.88,
        "Ag": 0.75,
        "Cu": 0.85,
    }
    
    OUTLIER_CAPS = {
        "Au": 100,  # g/t
        "Ag": 500,  # g/t
        "Cu": 5,    # %
    }
    
    DILUTION_FACTOR = 0.95
    
    # scripts/02_block_postprocessing.py
    from config.parameters import METAL_PRICES, RECOVERIES, DILUTION_FACTOR
    from pollywog.core import CalcSet, Number
    
    calcset = CalcSet([
        Number(name="Au_diluted", children=[f"[Au_est] * {DILUTION_FACTOR}"]),
        Number(name="Au_recovered", children=[f"[Au_diluted] * {RECOVERIES['Au']}"]),
    ])

Environment-Specific Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Support different environments (dev, prod):

.. code-block:: python

    import os
    from pathlib import Path
    
    # Determine environment
    ENV = os.getenv("LEAPFROG_ENV", "development")
    
    # Set paths based on environment
    if ENV == "production":
        OUTPUT_DIR = Path("/shared/leapfrog/calculations")
    else:
        OUTPUT_DIR = Path("./outputs")
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Export to appropriate location
    calcset.to_lfcalc(OUTPUT_DIR / "preprocessing.lfcalc")

Testing and Validation
----------------------

Unit Testing Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~

Test your calculation logic:

.. code-block:: python

    # tests/test_calculations.py
    import pytest
    from pollywog.core import CalcSet, Number
    from pollywog.run import run_calcset
    
    def test_nsr_calculation():
        """Test NSR calculation with known inputs."""
        calcset = CalcSet([
            Number(name="revenue", children=["[grade] * [price]"]),
            Number(name="cost", children=["35"]),
            Number(name="nsr", children=["[revenue] - [cost]"]),
        ])
        
        # Test with known values
        result = run_calcset(calcset, inputs={"grade": 2.0, "price": 50})
        
        assert result["revenue"] == 100
        assert result["cost"] == 35
        assert result["nsr"] == 65
    
    def test_domain_weighting():
        """Test weighted average calculation."""
        from pollywog.helpers import WeightedAverage
        
        calcset = CalcSet([
            WeightedAverage(
                variables=["Au_oxide", "Au_sulfide"],
                weights=["prop_oxide", "prop_sulfide"],
                name="Au_composite"
            )
        ])
        
        result = run_calcset(calcset, inputs={
            "Au_oxide": 1.5,
            "Au_sulfide": 0.8,
            "prop_oxide": 0.3,
            "prop_sulfide": 0.7,
        })
        
        expected = (1.5 * 0.3 + 0.8 * 0.7) / (0.3 + 0.7)
        assert abs(result["Au_composite"] - expected) < 0.001

Validation Against Leapfrog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Export small test cases and validate in Leapfrog:

.. code-block:: python

    # Create simple test case
    test_calcset = CalcSet([
        Number(name="test_sum", children=["[a] + [b]"]),
        Number(name="test_product", children=["[a] * [b]"]),
    ])
    
    test_calcset.to_lfcalc("test_calculations.lfcalc")
    
    # Import into Leapfrog with known values (a=2, b=3)
    # Verify test_sum = 5, test_product = 6

Performance Considerations
--------------------------

Minimize Calculations
~~~~~~~~~~~~~~~~~~~~~

Avoid redundant calculations:

.. code-block:: python

    # Bad - calculates Au + Ag twice
    CalcSet([
        Number(name="sum_scaled", children=["([Au] + [Ag]) * 2"]),
        Number(name="sum_offset", children=["([Au] + [Ag]) + 10"]),
    ])
    
    # Good - calculate once, reuse
    CalcSet([
        Number(name="sum_Au_Ag", children=["[Au] + [Ag]"]),
        Number(name="sum_scaled", children=["[sum_Au_Ag] * 2"]),
        Number(name="sum_offset", children=["[sum_Au_Ag] + 10"]),
    ])

Topological Sorting
~~~~~~~~~~~~~~~~~~~

Ensure correct calculation order:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    
    # Create calculations (order doesn't matter)
    calcset = CalcSet([
        Number(name="final", children=["[intermediate] * 2"]),
        Number(name="intermediate", children=["[Au] + [Ag]"]),
        Number(name="Au", children=["clamp([raw_Au], 0)"]),
    ])
    
    # Sort by dependencies before exporting
    sorted_calcset = calcset.topological_sort()
    sorted_calcset.to_lfcalc("properly_ordered.lfcalc")

Common Pitfalls to Avoid
------------------------

1. **Hardcoding Values**: Use configuration files for parameters that may change
2. **Missing Back-transforms**: Remember to back-transform after log/sqrt estimation
3. **Ignoring Units**: Keep track of units (g/t, %, oz/t, etc.) in comments
4. **No Version Control**: Always use Git for calculation scripts
5. **Insufficient Testing**: Test edge cases (zero, negative, very large values)
6. **Poor Documentation**: Future you will thank present you for good comments
7. **Complex Single Scripts**: Break large workflows into logical modules
8. **No Validation**: Always validate against manual calculations or Leapfrog

Workflow Checklist
------------------

Before deploying calculations to production:

1. ☐ Code is organized and well-structured
2. ☐ Variable names are descriptive and consistent
3. ☐ All hardcoded values are moved to configuration
4. ☐ Edge cases are handled (div by zero, log of zero, etc.)
5. ☐ Comments explain business logic and assumptions
6. ☐ Unit tests validate calculation logic
7. ☐ Results validated against manual calculations
8. ☐ Code is in version control with clear commit history
9. ☐ README documents workflow and assumptions
10. ☐ Dependencies are documented (Python version, packages)

See Also
--------

- :doc:`workflow_patterns` - Common workflow examples
- :doc:`expression_syntax` - Expression syntax reference
- :doc:`tutorials` - Step-by-step tutorials
- :doc:`api_reference` - Complete API documentation
