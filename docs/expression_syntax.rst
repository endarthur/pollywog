Leapfrog Expression Syntax Guide
=================================

This guide explains the expression syntax used in Leapfrog calculators and how pollywog represents them.

Understanding Leapfrog Calculations
------------------------------------

In Leapfrog, calculations are defined using a specialized expression language that allows you to:

- Reference variables using square brackets: ``[variable_name]``
- Apply mathematical operations: ``+``, ``-``, ``*``, ``/``, ``^`` (power)
- Use built-in functions for numerical transformations
- Create conditional logic with if/else statements
- Categorize data based on thresholds or conditions

Variable References
-------------------

Variables in Leapfrog expressions are referenced using square brackets. This allows Leapfrog to distinguish between variable names and other text.

.. code-block:: python

    # Reference a single variable
    Number(name="Au_scaled", children=["[Au] * 2.0"])
    
    # Reference multiple variables in an expression
    Number(name="total_grade", children=["[Au] + [Ag] + [Cu]"])
    
    # Reference block model variables
    Number(name="density_calc", children=["[block_density] * [block_volume]"])

Common variable contexts in Leapfrog:

- **Drillhole variables**: Assay data, downhole surveys, lithology codes
- **Block model variables**: Estimated grades, geological domains, density
- **Mesh variables**: Surface attributes, interpolated values
- **Points variables**: Discrete point data, sample locations

Mathematical Operations
-----------------------

Pollywog supports all standard mathematical operations used in Leapfrog:

.. code-block:: python

    # Addition and subtraction
    Number(name="net_grade", children=["[Au_est] - [Au_waste]"])
    
    # Multiplication and division
    Number(name="metal_content", children=["[grade] * [tonnage] / 1000"])
    
    # Exponentiation (power)
    Number(name="Au_squared", children=["[Au] ^ 2"])
    
    # Parentheses for order of operations
    Number(name="weighted_avg", children=["([Au] * [weight_Au] + [Ag] * [weight_Ag]) / ([weight_Au] + [weight_Ag])"])

Built-in Functions
------------------

Leapfrog provides many built-in functions that pollywog emulates. These functions are available in calculation expressions:

Mathematical Functions
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Logarithmic functions
    Number(name="Au_log10", children=["log([Au], 10)"])  # Base 10 logarithm
    Number(name="Au_ln", children=["ln([Au])"])           # Natural logarithm
    Number(name="Au_exp", children=["exp([Au])"])         # Exponential (e^x)
    
    # Square root
    Number(name="Au_sqrt", children=["sqrt([Au])"])
    
    # Absolute value
    Number(name="Au_abs", children=["abs([Au] - [Au_target])"])

Trigonometric Functions
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Basic trigonometry
    Number(name="sin_angle", children=["sin([angle])"])
    Number(name="cos_angle", children=["cos([angle])"])
    Number(name="tan_angle", children=["tan([angle])"])
    
    # Inverse trigonometry
    Number(name="asin_val", children=["asin([ratio])"])
    Number(name="acos_val", children=["acos([ratio])"])
    Number(name="atan_val", children=["atan([slope])"])

Rounding and Clamping
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Clamp values to a range
    Number(name="Au_clamped", children=["clamp([Au], 0)"])           # Minimum of 0
    Number(name="Au_range", children=["clamp([Au], 0, 10)"])         # Between 0 and 10
    
    # Round to decimal places
    Number(name="Au_round", children=["round([Au], 2)"])             # 2 decimal places
    Number(name="Au_round_int", children=["round([Au])"])            # Round to integer
    
    # Round to significant figures
    Number(name="Au_sf", children=["roundsf([Au], 3)"])              # 3 significant figures
    
    # Floor and ceiling
    Number(name="Au_floor", children=["floor([Au])"])                # Round down
    Number(name="Au_ceiling", children=["ceiling([Au])"])            # Round up
    
    # Truncate (remove decimal part)
    Number(name="Au_trunc", children=["truncate([Au])"])

Min and Max
~~~~~~~~~~~

.. code-block:: python

    # Minimum and maximum of multiple values
    Number(name="max_grade", children=["max([Au], [Ag], [Cu])"])
    Number(name="min_grade", children=["min([Au], [Ag], [Cu])"])
    
    # Useful for creating composite variables
    Number(name="best_estimate", children=["max([est_kriging], [est_idw])"])

String Functions
~~~~~~~~~~~~~~~~

String functions are useful for working with categorical data and text fields:

.. code-block:: python

    # Concatenate strings
    Category(name="full_code", children=["concat([domain], '_', [zone])"])
    
    # String tests (return true/false)
    # These are typically used in conditional expressions
    # startswith([text], 'prefix')
    # endswith([text], 'suffix')
    # contains([text], 'substring')
    # like([text], 'pattern')
    # regexp([text], 'regex_pattern')

Constants
~~~~~~~~~

Pollywog provides access to mathematical constants:

.. code-block:: python

    # Pi and e are available as constants
    Number(name="circle_area", children=["pi * [radius] ^ 2"])
    Number(name="exponential", children=["e ^ [rate]"])

Conditional Logic (If/Else)
---------------------------

Conditional logic is essential for domain-based calculations, classification, and applying business rules.

Basic If/Else
~~~~~~~~~~~~~

.. code-block:: python

    from pollywog.core import If, Number
    
    # Simple if/else using the shorthand syntax
    Number(name="Au_adjusted", children=[
        If("[Au] > 5", "[Au] * 0.9", "[Au]")
    ])
    
    # Multiple conditions
    Number(name="Au_category", children=[
        If([
            ("[Au] <= 0.5", "0.25"),      # If Au <= 0.5, return 0.25
            ("[Au] <= 2.0", "1.0"),       # Else if Au <= 2.0, return 1.0
            ("[Au] <= 5.0", "3.5"),       # Else if Au <= 5.0, return 3.5
        ], otherwise=["7.5"])             # Otherwise return 7.5
    ])

Domain-Based Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~

A common pattern in resource estimation is applying different formulas based on geological domains:

.. code-block:: python

    from pollywog.core import If, IfRow, Number
    
    # Apply different recovery factors by domain
    Number(name="Au_recovered", children=[
        If([
            ("[domain] == 'oxide'", "[Au_est] * 0.92"),
            ("[domain] == 'transition'", "[Au_est] * 0.85"),
            ("[domain] == 'sulfide'", "[Au_est] * 0.78"),
        ], otherwise=["[Au_est] * 0.75"])  # Default recovery
    ])
    
    # Combine conditions
    Number(name="dilution_factor", children=[
        If([
            ("([domain] == 'high_grade') and ([Au] > 3)", "1.05"),
            ("([domain] == 'high_grade') and ([Au] <= 3)", "1.10"),
            ("[domain] == 'low_grade'", "1.20"),
        ], otherwise=["1.15"])
    ])

Categorical Outputs
~~~~~~~~~~~~~~~~~~~

Use the ``Category`` class for text-based outputs:

.. code-block:: python

    from pollywog.core import If, Category
    
    Category(name="ore_type", children=[
        If([
            ("[Au] > 2 and [domain] == 'oxide'", "'high_grade_oxide'"),
            ("[Au] > 2", "'high_grade'"),
            ("[Au] > 0.5", "'medium_grade'"),
        ], otherwise=["'low_grade'"])
    ])

Boolean Comparisons
~~~~~~~~~~~~~~~~~~~

Comparison operators available in expressions:

- ``==`` : Equal to
- ``!=`` : Not equal to
- ``>`` : Greater than
- ``>=`` : Greater than or equal to
- ``<`` : Less than
- ``<=`` : Less than or equal to
- ``and`` : Logical AND
- ``or`` : Logical OR
- ``not`` : Logical NOT

.. code-block:: python

    # Complex condition
    Number(name="mineable", children=[
        If("([Au] >= 0.3) and ([thickness] >= 2) and ([depth] <= 300)", "1", "0")
    ])

Working with Missing Values
----------------------------

In Leapfrog, missing or null values can occur in various contexts. Here are strategies for handling them:

.. code-block:: python

    # Provide default values for missing data
    Number(name="Au_clean", children=["clamp([Au], 0)"])
    
    # Use conditional logic to handle nulls
    # (In Leapfrog, you might check if a value exists)
    Number(name="Au_default", children=[
        If("[Au] != [Au]", "0.001", "[Au]")  # NaN != NaN is true
    ])
    
    # Add small epsilon to avoid log(0) errors
    Number(name="Au_log_safe", children=["log([Au] + 1e-6)"])

Best Practices for Expressions
-------------------------------

1. **Use descriptive variable names**: ``Au_final_recovered`` is better than ``af``
2. **Add comments**: Use the ``comment_equation`` parameter to document complex logic
3. **Avoid magic numbers**: Define threshold values clearly or use variables
4. **Break complex calculations into steps**: Multiple simple calculations are easier to debug than one complex expression
5. **Use helper functions**: Pollywog's helpers (Sum, Product, WeightedAverage, etc.) make code more readable
6. **Clamp inputs**: Protect against invalid values (negative grades, divide by zero)
7. **Test edge cases**: Ensure your expressions handle boundary conditions correctly

Example: Complete Workflow
---------------------------

Here's a comprehensive example showing various expression types:

.. code-block:: python

    from pollywog.core import CalcSet, Number, Category, If
    from pollywog.helpers import WeightedAverage, CategoryFromThresholds
    
    calcset = CalcSet([
        # 1. Data cleaning
        Number(name="Au_clean", children=["clamp([Au], 0)"], 
               comment_equation="Remove negative values"),
        Number(name="density_clean", children=["clamp([density], 1.5, 5.0)"],
               comment_equation="Clamp density to realistic range"),
        
        # 2. Transformations
        Number(name="Au_log", children=["log([Au_clean] + 1e-6)"],
               comment_equation="Log transform with epsilon for zeros"),
        
        # 3. Domain-based adjustments
        Number(name="Au_adjusted", children=[
            If([
                ("[domain] == 'oxide'", "[Au_clean] * 0.95"),
                ("[domain] == 'sulfide'", "[Au_clean] * 0.90"),
            ], otherwise=["[Au_clean]"])
        ], comment_equation="Apply domain-specific scaling"),
        
        # 4. Weighted average from multiple estimates
        WeightedAverage(
            variables=["Au_kriging", "Au_idw", "Au_nn"],
            weights=[0.6, 0.3, 0.1],
            name="Au_composite",
            comment="Weighted combination of estimation methods"
        ),
        
        # 5. Economic calculations
        Number(name="metal_tonnes", children=["[Au_composite] * [tonnes] / 31.1035"],
               comment_equation="Convert grade to troy ounces"),
        Number(name="revenue", children=["[metal_tonnes] * [Au_price] * [recovery]"],
               comment_equation="Estimated revenue per block"),
        
        # 6. Classification
        CategoryFromThresholds(
            variable="Au_composite",
            thresholds=[0.3, 1.0, 3.0],
            categories=["waste", "low_grade", "medium_grade", "high_grade"],
            name="ore_class",
            comment="Classify blocks by gold grade"
        ),
    ])
    
    # Export to Leapfrog
    calcset.to_lfcalc("comprehensive_example.lfcalc")

See Also
--------

- :doc:`tutorials` - Complete workflow examples
- :doc:`helpers_guide` - Pollywog helper functions
- :doc:`api_reference` - Full API documentation
