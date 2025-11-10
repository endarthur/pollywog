Common Workflow Patterns
========================

This guide presents common workflow patterns in geological modeling and resource estimation, demonstrating how to implement them using pollywog.

Grade Estimation Workflows
---------------------------

Pattern 1: Preprocessing → Estimation → Postprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the most common workflow in resource estimation:

.. code-block:: python

    from pollywog.core import CalcSet, Number

    # Step 1: Preprocess drillhole data
    # Create a calcset for drillhole composites
    preprocess = CalcSet([
        # Remove outliers using clamping
        Number(name="Au_clamped", "clamp([Au], 0, 100)",
               comment_equation="Cap gold at 100 g/t to remove outliers"),
        Number(name="Cu_clamped", "clamp([Cu], 0, 5)",
               comment_equation="Cap copper at 5% to remove outliers"),

        # Log transforms for geostatistics
        Number(name="Au_log", "log([Au_clamped] + 0.01)",
               comment_equation="Log transform for kriging"),
        Number(name="Cu_log", "log([Cu_clamped] + 0.01)",
               comment_equation="Log transform for kriging"),
    ])

    # Export for drillhole calculations
    preprocess.to_lfcalc("01_drillhole_preprocessing.lfcalc")

    # Step 2: Perform estimation in Leapfrog
    # (This happens in Leapfrog UI - estimate Au_log and Cu_log)

    # Step 3: Postprocess block model
    # Back-transform and apply recovery
    postprocess = CalcSet([
        # Back-transform from log space
        Number(name="Au_est", "exp([Au_log_kriged]) - 0.01",
               comment_equation="Back-transform from log space"),
        Number(name="Cu_est", "exp([Cu_log_kriged]) - 0.01",
               comment_equation="Back-transform from log space"),

        # Apply minimum mining width dilution
        Number(name="Au_diluted", "[Au_est] * 0.95",
               comment_equation="5% dilution factor"),
        Number(name="Cu_diluted", "[Cu_est] * 0.95",
               comment_equation="5% dilution factor"),

        # Apply metallurgical recovery
        Number(name="Au_recovered", "[Au_diluted] * 0.88",
               comment_equation="88% Au recovery"),
        Number(name="Cu_recovered", "[Cu_diluted] * 0.82",
               comment_equation="82% Cu recovery"),
    ])

    postprocess.to_lfcalc("03_block_postprocessing.lfcalc")

Pattern 2: Multi-Domain Estimation with Proportions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When estimating across geological domains with varying proportions:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    from pollywog.helpers import WeightedAverage

    # Define your domains and metals
    domains = ["oxide", "transition", "sulfide"]
    metals = ["Au", "Ag", "Cu"]

    # Assume Leapfrog has estimated:
    # - Au_oxide, Au_transition, Au_sulfide (and same for Ag, Cu)
    # - prop_oxide, prop_transition, prop_sulfide

    # Create weighted averages by domain proportions
    weighted_estimates = CalcSet([
        WeightedAverage(
            variables=[f"{metal}_{domain}" for domain in domains],
            weights=[f"prop_{domain}" for domain in domains],
            name=f"{metal}_final",
            comment=f"Weighted {metal} grade by domain proportions"
        )
        for metal in metals
    ])

    weighted_estimates.to_lfcalc("weighted_domain_grades.lfcalc")

Pattern 3: Conditional Estimation by Rock Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apply different estimation approaches based on rock type:

.. code-block:: python

    from pollywog.core import CalcSet, Number, If

    calcset = CalcSet([
        # Use different estimation methods based on rock type
        Number(name="Au_final", expression=[
            If([
                ("[rocktype] = 'basalt'", "[Au_ordinary_kriging]"),
                ("[rocktype] = 'breccia'", "[Au_indicator_kriging]"),
                ("[rocktype] = 'skarn'", "[Au_nearest_neighbor]"),
            ], otherwise=["[Au_inverse_distance]"])
        ], comment_equation="Select estimation method by rock type"),
    ])

    calcset.to_lfcalc("conditional_estimation.lfcalc")

Geometallurgy Workflows
------------------------

Pattern 4: Recovery Models from Test Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate metallurgical test data to predict recovery:

.. code-block:: python

    from pollywog.core import CalcSet, Number, If

    # Based on geometallurgical domains and test work
    recovery_model = CalcSet([
        # Gold recovery as a function of grind size and domain
        Number(name="Au_recovery", expression=[
            If([
                ("([geo_domain] = 'free_milling') and ([p80] <= 75)", "0.92"),
                ("([geo_domain] = 'free_milling') and ([p80] > 75)", "0.88"),
                ("([geo_domain] = 'refractory') and ([p80] <= 75)", "0.78"),
                ("([geo_domain] = 'refractory') and ([p80] > 75)", "0.72"),
            ], otherwise=["0.70"])
        ], comment_equation="Recovery by geo-domain and grind size"),

        # Copper recovery based on mineralogy
        Number(name="Cu_recovery", expression=[
            If([
                ("[Cu_sulfide_pct] > 80", "0.85"),
                ("[Cu_sulfide_pct] > 50", "0.78"),
                ("[Cu_sulfide_pct] > 20", "0.65"),
            ], otherwise=["0.45"])
        ], comment_equation="Recovery based on sulfide content"),

        # Recoverable metal
        Number(name="Au_payable", "[Au_est] * [Au_recovery]",
               comment_equation="Payable gold"),
        Number(name="Cu_payable", "[Cu_est] * [Cu_recovery]",
               comment_equation="Payable copper"),
    ])

    recovery_model.to_lfcalc("geometallurgy_recovery.lfcalc")

Pattern 5: Process Plant Feed Blending
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model mill throughput and blending constraints:

.. code-block:: python

    from pollywog.core import CalcSet, Number

    mill_performance = CalcSet([
        # Hardness-based throughput adjustment
        Number(name="relative_throughput", expression=[
            "100 / (([bond_wi] / 15) ^ 0.82)"
        ], comment_equation="Throughput relative to 15 kWh/t reference"),

        # Tonnes per hour
        Number(name="tph", expression=[
            "[relative_throughput] * [base_tph]"
        ], comment_equation="Estimated mill throughput"),

        # Metals production per hour
        Number(name="Au_oz_per_hour", expression=[
            "[Au_payable] * [tph] / 31.1035"
        ], comment_equation="Gold ounces per hour"),
    ])

    mill_performance.to_lfcalc("mill_throughput.lfcalc")

Economic Evaluation Workflows
------------------------------

Pattern 6: Net Smelter Return (NSR)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate the value of ore based on multiple commodities:

.. code-block:: python

    from pollywog.core import CalcSet, Number

    # Define metal prices and costs
    nsr_model = CalcSet([
        # Gross revenue per tonne
        Number(name="Au_revenue_per_t", expression=[
            "[Au_recovered] * [Au_price] / 31.1035"
        ], comment_equation="Gold revenue ($/t), price in $/oz"),

        Number(name="Ag_revenue_per_t", expression=[
            "[Ag_recovered] * [Ag_price] / 31.1035"
        ], comment_equation="Silver revenue ($/t), price in $/oz"),

        Number(name="Cu_revenue_per_t", expression=[
            "[Cu_recovered] * [Cu_price] * 10"
        ], comment_equation="Copper revenue ($/t), price in $/lb, grade in %"),

        # Total gross revenue
        Number(name="gross_revenue", expression=[
            "[Au_revenue_per_t] + [Ag_revenue_per_t] + [Cu_revenue_per_t]"
        ], comment_equation="Total revenue per tonne"),

        # Deduct costs
        Number(name="mining_cost", "35",
               comment_equation="Mining cost $/t"),
        Number(name="processing_cost", "18",
               comment_equation="Processing cost $/t"),
        Number(name="admin_cost", "5",
               comment_equation="G&A cost $/t"),

        # NSR calculation
        Number(name="nsr", expression=[
            "[gross_revenue] - [mining_cost] - [processing_cost] - [admin_cost]"
        ], comment_equation="Net Smelter Return ($/t)"),
    ])

    nsr_model.to_lfcalc("economic_nsr.lfcalc")

Pattern 7: Cut-off Grade Classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Classify blocks as ore or waste based on economic cut-off:

.. code-block:: python

    from pollywog.core import CalcSet, Number, Category, If
    from pollywog.helpers import CategoryFromThresholds

    cutoff_classification = CalcSet([
        # Economic value (NSR from previous example)
        # Assume [nsr] is already calculated

        # Simple ore/waste classification
        Category(name="ore_waste", expression=[
            If("[nsr] >= [cutoff_grade]", "'ore'", "'waste'")
        ], comment_equation="Binary ore/waste flag"),

        # Multi-tier classification
        CategoryFromThresholds(
            variable="nsr",
            thresholds=[0, 20, 40],
            categories=["waste", "marginal", "ore", "high_grade"],
            "material_type",
            comment="Material classification by NSR value"
        ),

        # Tonnage flag (1 for ore, 0 for waste)
        Number(name="ore_tonnes_flag", expression=[
            If("[nsr] >= [cutoff_grade]", "1", "0")
        ], comment_equation="Flag for ore tonnage reporting"),
    ])

    cutoff_classification.to_lfcalc("cutoff_classification.lfcalc")

Quality Control Workflows
--------------------------

Pattern 8: Data Validation and Flagging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create flags to identify data quality issues:

.. code-block:: python

    from pollywog.core import CalcSet, Number, Category, If

    qa_qc = CalcSet([
        # Flag negative grades
        Number(name="flag_negative", expression=[
            If("([Au] < 0) or ([Cu] < 0) or ([Ag] < 0)", "1", "0")
        ], comment_equation="Flag negative assays"),

        # Flag extreme values (potential outliers)
        Number(name="flag_extreme", expression=[
            If("([Au] > 100) or ([Cu] > 10) or ([Ag] > 500)", "1", "0")
        ], comment_equation="Flag extreme values"),

        # Flag missing critical data
        Number(name="flag_missing", expression=[
            If("(not is_normal([density])) or ([domain] = '')", "1", "0")
        ], comment_equation="Flag missing density or domain"),

        # Overall QA/QC status
        Category(name="qa_status", expression=[
            If([
                ("[flag_negative] = 1", "'FAILED_NEGATIVE'"),
                ("[flag_extreme] = 1", "'REVIEW_OUTLIER'"),
                ("[flag_missing] = 1", "'FAILED_MISSING'"),
            ], otherwise=["'PASSED'"])
        ], comment_equation="Overall QA/QC status"),
    ])

    qa_qc.to_lfcalc("qa_qc_flags.lfcalc")

Pattern 9: Grade Control and Reconciliation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare estimated vs. actual grades for reconciliation:

.. code-block:: python

    from pollywog.core import CalcSet, Number

    reconciliation = CalcSet([
        # Calculate difference between estimate and actual
        Number(name="Au_variance", expression=[
            "[Au_actual] - [Au_estimated]"
        ], comment_equation="Grade variance"),

        # Percent difference
        Number(name="Au_pct_diff", expression=[
            "100 * ([Au_actual] - [Au_estimated]) / [Au_estimated]"
        ], comment_equation="Percentage difference"),

        # Tonnage difference
        Number(name="tonnes_variance", expression=[
            "[tonnes_actual] - [tonnes_estimated]"
        ], comment_equation="Tonnage variance"),

        # Metal difference
        Number(name="metal_variance_oz", expression=[
            "([Au_actual] * [tonnes_actual] - [Au_estimated] * [tonnes_estimated]) / 31.1035"
        ], comment_equation="Metal variance in ounces"),

        # Reconciliation ratio
        Number(name="recon_ratio", expression=[
            "[Au_actual] / [Au_estimated]"
        ], comment_equation="Actual to estimated ratio"),
    ])

    reconciliation.to_lfcalc("reconciliation.lfcalc")

Machine Learning Integration
-----------------------------

Pattern 10: Scikit-learn Model Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate trained ML models into Leapfrog calculations:

.. code-block:: python

    import numpy as np
    from sklearn.ensemble import RandomForestRegressor
    from pollywog.conversion.sklearn import convert_tree, convert_forest
    from pollywog.core import CalcSet

    # Example: Predict density from geochemistry
    # Training data (from lab measurements)
    X_train = np.array([
        [0.5, 1.2, 45],  # Au, Cu, SiO2
        [1.0, 0.8, 52],
        [0.3, 2.1, 38],
        # ... more training data
    ])
    y_train = np.array([2.7, 2.65, 2.8])  # Measured densities

    # Train random forest model
    rf_model = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)
    rf_model.fit(X_train, y_train)

    # Convert to Leapfrog calculation
    feature_names = ["Au_est", "Cu_est", "SiO2_est"]
    density_calc = convert_forest(
        rf_model,
        feature_names,
        "density_predicted",
        comment_equation="ML-predicted density from geochemistry"
    )

    # Create calcset with ML model
    ml_calcset = CalcSet([density_calc])
    ml_calcset.to_lfcalc("ml_density_prediction.lfcalc")

Pattern 11: Classification Models for Domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ML to predict geological domains:

.. code-block:: python

    from sklearn.tree import DecisionTreeClassifier
    from pollywog.conversion.sklearn import convert_tree
    from pollywog.core import CalcSet

    # Train domain classifier
    # Features: Au, Cu, Ag, Zn, Fe
    X_train = np.array([
        [0.2, 0.1, 5, 0.5, 3],   # Oxide
        [1.5, 0.8, 20, 1.2, 5],  # Sulfide
        [0.8, 0.4, 10, 0.8, 4],  # Transition
        # ... more training data
    ])
    y_train = ["oxide", "sulfide", "transition", ...]  # Domain labels

    # Train decision tree classifier
    dt_classifier = DecisionTreeClassifier(max_depth=8, random_state=42)
    dt_classifier.fit(X_train, y_train)

    # Convert to Leapfrog calculation
    feature_names = ["Au_composite", "Cu_composite", "Ag_composite", "Zn_composite", "Fe_composite"]
    domain_calc = convert_tree(
        dt_classifier,
        feature_names,
        "domain_predicted",
        comment_equation="ML-predicted geological domain"
    )

    domain_calcset = CalcSet([domain_calc])
    domain_calcset.to_lfcalc("ml_domain_classification.lfcalc")

Advanced Patterns
-----------------

Pattern 12: Combining Multiple CalcSets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build complex workflows by combining calculation sets:

.. code-block:: python

    from pollywog.core import CalcSet, Number

    # Create separate calculation sets for different purposes
    data_prep = CalcSet([
        Number(name="Au_clamped", expression=["clamp([Au], 0, 50)"]),
        Number(name="Cu_clamped", expression=["clamp([Cu], 0, 5)"]),
    ])

    estimation_support = CalcSet([
        Number(name="Au_log", expression=["log([Au_clamped] + 0.01)"]),
        Number(name="Cu_log", expression=["log([Cu_clamped] + 0.01)"]),
    ])

    # Combine them
    combined = CalcSet(data_prep.items + estimation_support.items)
    combined.to_lfcalc("combined_preprocessing.lfcalc")

Pattern 13: Modular Workflow with Reusable Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create reusable calculation components:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    from pollywog.helpers import WeightedAverage

    def create_metal_calcs(metal, domains, apply_recovery=True):
        """Generate standard calculations for a metal across domains."""
        calcs = [
            # Weighted average by domain
            WeightedAverage(
                variables=[f"{metal}_{d}" for d in domains],
                weights=[f"prop_{d}" for d in domains],
                name=f"{metal}_composite"
            ),
        ]

        if apply_recovery:
            calcs.append(
                Number(name=f"{metal}_recovered",
                       expression=[f"[{metal}_composite] * [recovery_{metal}]"])
            )

        return calcs

    # Use the function to generate calculations
    domains = ["oxide", "transition", "sulfide"]
    all_metals = CalcSet([
        *create_metal_calcs("Au", domains, apply_recovery=True),
        *create_metal_calcs("Ag", domains, apply_recovery=True),
        *create_metal_calcs("Cu", domains, apply_recovery=True),
    ])

    all_metals.to_lfcalc("modular_metals.lfcalc")

Pattern 14: Topological Sorting for Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure calculations are ordered correctly:

.. code-block:: python

    from pollywog.core import CalcSet, Number

    # Create calculations in any order
    unordered = CalcSet([
        Number(name="final_value", expression=["[intermediate] * 2"]),
        Number(name="intermediate", expression=["[Au] + [Ag]"]),
    ])

    # Sort by dependencies
    ordered = unordered.topological_sort()

    # Now intermediate will be calculated before final_value
    ordered.to_lfcalc("properly_ordered.lfcalc")

Tips for Building Effective Workflows
--------------------------------------

1. **Start Simple**: Begin with basic calculations and add complexity incrementally
2. **Use Descriptive Names**: Make variable names self-documenting
3. **Add Comments**: Use ``comment_equation`` parameter to explain business logic
4. **Test in Stages**: Export and test each stage of the workflow in Leapfrog
5. **Validate Results**: Use QA/QC calculations to verify outputs
6. **Version Control**: Keep your Python scripts in version control (Git)
7. **Document Assumptions**: Record cut-off grades, prices, recoveries in your code
8. **Modularize**: Break complex workflows into reusable functions
9. **Handle Edge Cases**: Use clamp, conditional logic to handle invalid inputs
10. **Review Dependencies**: Use ``topological_sort()`` to ensure proper calculation order

Common Pitfalls to Avoid
-------------------------

1. **Missing Parentheses**: Always use parentheses in complex expressions
2. **Division by Zero**: Clamp denominators away from zero
3. **Log of Zero/Negative**: Add small epsilon before taking logarithms
4. **Incorrect Order**: Ensure dependent calculations come after their dependencies
5. **Type Mismatches**: Use Number for numeric outputs, Category for text
6. **Hardcoded Values**: Use variables for parameters that might change
7. **Missing Back-transforms**: Remember to back-transform after log-domain estimation
8. **Ignoring Units**: Keep track of units (%, ppm, g/t, oz/t, etc.)

See Also
--------

- :doc:`expression_syntax` - Detailed syntax reference
- :doc:`tutorials` - Step-by-step tutorials
- :doc:`api_reference` - Complete API documentation
- :doc:`helpers_guide` - Helper function reference
