
Tutorials
=========

This section provides step-by-step tutorials demonstrating complete workflows using pollywog. Each tutorial builds on the previous one, progressing from basic concepts to advanced techniques.

.. note::
    Many of these tutorials are also available as Jupyter notebooks. See :doc:`examples` for a complete catalog of all available notebooks, or try them interactively in your browser at `JupyterLite <https://endarthur.github.io/pollyweb>`_!

Tutorial Overview
-----------------

1. **Complete Resource Estimation Workflow**: Preprocessing, estimation, and postprocessing
2. **Working with Helper Functions**: Simplify common calculation patterns
3. **Machine Learning Integration**: Deploy ML models in Leapfrog calculations
4. **Querying and Filtering CalcSets**: Advanced CalcSet manipulation

Complete Resource Estimation Workflow
--------------------------------------

This tutorial demonstrates a complete workflow using pollywog: preprocessing multivariate drillhole data, estimating grades in Leapfrog, postprocessing results on a block model using domain proportions, and adding geometallurgical recovery using regression trees.

Step 1: Preprocessing Drillhole Data (Drillhole CalcSet)
--------------------------------------------------------
Suppose you have raw drillhole assays for gold (Au), silver (Ag), and copper (Cu). We'll clean and transform these variables before estimation.

.. code-block:: python

    from pollywog.core import CalcSet, Number
    variables = ["Au", "Ag", "Cu"]
    preprocess = CalcSet([
        *[Number(f"{v}_clean", [f"clamp([{v}], 0)"]) for v in variables],
        *[Number(f"{v}_log", [f"log([{v}_clean] + 1e-6)"]) for v in variables],
    ])

    # Export for use in Leapfrog (drillholes)
    preprocess.to_lfcalc("drillhole_preprocessing.lfcalc")

Step 2: Estimation in Leapfrog
------------------------------
Estimation of grades (e.g., interpolation, regression, or geostatistics) is performed in Leapfrog using the preprocessed variables. This step is not handled by pollywog.

Assume Leapfrog produces block model variables for each domain, e.g. `Au_high`, `Au_medium`, `Au_low`, and proportion variables `prop_high`, `prop_medium`, `prop_low`. The sum of proportions may be less than 1 (waste domain not estimated).

Step 3: Percentile Postprocessing on Block Model (Block CalcSet)
----------------------------------------------------------------
Calculate the final grade as a weighted sum of domain grades, normalized by the sum of the weights (proportions). Two approaches are shown:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    from pollywog.helpers import WeightedAverage
    variables = ["Au", "Ag", "Cu"]
    domains = ["high", "medium", "low"]
    # Manual normalization
    postprocess_manual = CalcSet([
        *[Number(f"{v}_final", [
            f"(({' + '.join([f'[prop_{d}] * [{v}_{d}]' for d in domains])}) / ({' + '.join([f'[prop_{d}]' for d in domains])}))"
        ]) for v in variables],
    ])
    # Using WeightedAverage helper
    postprocess_helper = CalcSet([
        *[WeightedAverage(
            variables=[f"{v}_{d}" for d in domains],
            weights=[f"prop_{d}" for d in domains],
            name=f"{v}_final_weighted"
        ) for v in variables],
    ])

    # Export for use in Leapfrog (block model)
    postprocess_manual.to_lfcalc("blockmodel_postprocessing_manual.lfcalc")
    postprocess_helper.to_lfcalc("blockmodel_postprocessing_weighted.lfcalc")

Step 4: Geometallurgical Recovery with Regression Trees
--------------------------------------------------------

.. note::
   **Machine learning conversion requires scikit-learn:**

   Install with: ``pip install lf_pollywog[conversion]``

   This includes scikit-learn for model conversion features.

Create example data for metal recovery, fit a regression tree, and add the tree-based recovery calculation to the block model calcset.

.. code-block:: python

    import numpy as np
    from sklearn.tree import DecisionTreeRegressor
    from pollywog.conversion.sklearn import convert_tree
    from pollywog.core import CalcSet

    # Example data: columns are Au_final, Ag_final, Cu_final
    X = np.array([
        [1.2, 5.0, 0.3],
        [0.8, 2.5, 0.1],
        [2.0, 1.0, 0.5],
        [0.5, 3.2, 0.2],
        [1.5, 4.1, 0.4],
        [0.3, 0.8, 0.05],
        [2.5, 2.0, 0.7],
        [1.8, 3.5, 0.6],
        [0.9, 1.2, 0.2],
        [1.0, 2.8, 0.3],
    ])
    # Example recoveries for Au (could be based on lab tests)
    y_au = np.array([0.85, 0.78, 0.92, 0.75, 0.88, 0.65, 0.95, 0.90, 0.80, 0.83])

    # Fit regression tree for Au recovery
    tree_au = DecisionTreeRegressor(max_depth=3)
    tree_au.fit(X, y_au)

    # Convert tree to CalcSet
    tree_calcset = CalcSet(convert_tree(tree_au, input_names=["Au_final", "Ag_final", "Cu_final"], output_name="Au_recovery"))

    # Add recovery calculation to block model calcset
    postprocess_manual.items += tree_calcset.items
    postprocess_helper.items += tree_calcset.items

    # Export updated block model calcsets
    postprocess_manual.to_lfcalc("blockmodel_postprocessing_with_recovery_manual.lfcalc")
    postprocess_helper.to_lfcalc("blockmodel_postprocessing_with_recovery_weighted.lfcalc")

Step 5: Visualization (Optional)
---------------------------------
You can visualize any CalcSet in Jupyter for inspection.

.. code-block:: python

    from pollywog.display import display_calcset, set_theme
    set_theme("light")
    display_calcset(preprocess)
    display_calcset(postprocess_manual)
    display_calcset(postprocess_helper)

.. TODO: Add screenshot showing calcset visualization in Jupyter
.. .. image:: _static/tutorial_visualization_example.png
..    :alt: CalcSet visualization in Jupyter notebook
..    :align: center
..    :width: 90%
..
.. |

For more advanced topics and real data examples, see:

- :doc:`examples` - Complete catalog of all example notebooks
- `examples/ folder on GitHub <https://github.com/endarthur/pollywog/tree/main/examples>`_ - Direct access to notebook files
- `JupyterLite <https://endarthur.github.io/pollyweb>`_ - Run examples in your browser

Step 6: More Helper Function Examples
--------------------------------------
Pollywog provides several helpers to simplify common calculation patterns. Here are some examples:

.. code-block:: python

    from pollywog.helpers import Sum, Product, Scale, CategoryFromThresholds

    # Sum: Combine multiple Au estimates for validation
    sum_example = Sum(["Au_kriging", "Au_idw", "Au_nn"], name="Au_estimates_total")

    # Product: Calculate recovered gold (grade × recovery)
    product_example = Product(["Au_final", "Au_recovery"], name="Au_payable")

    # Scale: Apply dilution factor
    scale_example = Scale("Au_final", 0.95, name="Au_diluted")

    # Note: For normalizing proportions to sum to 1, use manual calculation:
    # normalize_example = Number(
    #     "prop_high_norm",
    #     expression=["[prop_high] / ([prop_high] + [prop_medium] + [prop_low])"]
    # )

    # CategoryFromThresholds: Categorize based on grade thresholds
    cat_example = CategoryFromThresholds(
        variable="Au_final",
        thresholds=[0.3, 1.0],
        categories=["Low_Grade", "Medium_Grade", "High_Grade"],
        name="Au_OreClass"
    )

    # Add these to a CalcSet and export
    helpers_calcset = CalcSet([
        sum_example,
        product_example,
        scale_example,
        cat_example,
    ])
    helpers_calcset.to_lfcalc("blockmodel_helpers_examples.lfcalc")

    # Visualize in Jupyter
    display_calcset(helpers_calcset)

Tutorial 2: Advanced Helper Functions
--------------------------------------

This tutorial explores the full power of pollywog's helper functions for building complex workflows efficiently.

Using WeightedAverage for Domain Compositing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When working with multiple geological domains, you often need to combine estimates weighted by domain proportions:

.. code-block:: python

    from pollywog.core import CalcSet
    from pollywog.helpers import WeightedAverage

    # Define your metals and domains
    metals = ["Au", "Ag", "Cu", "Pb", "Zn"]
    domains = ["oxide", "transition", "sulfide"]

    # Generate weighted averages for all metals
    # Assumes variables like Au_oxide, Au_transition, Au_sulfide exist
    # and prop_oxide, prop_transition, prop_sulfide
    weighted_calcs = CalcSet([
        WeightedAverage(
            variables=[f"{metal}_{domain}" for domain in domains],
            weights=[f"prop_{domain}" for domain in domains],
            name=f"{metal}_composite",
            comment=f"Domain-weighted {metal} grade"
        )
        for metal in metals
    ])

    weighted_calcs.to_lfcalc("domain_weighted_grades.lfcalc")

Creating Complex Workflows with Multiple Helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Combine multiple helpers to build sophisticated calculations:

.. code-block:: python

    from pollywog.core import CalcSet
    from pollywog.helpers import (
        WeightedAverage, Product, Sum, Scale,
        CategoryFromThresholds, Normalize
    )

    # Multi-commodity resource model with economics
    resource_model = CalcSet([
        # 1. Domain-weighted grades
        WeightedAverage(
            variables=["Au_oxide", "Au_sulfide", "Au_transition"],
            weights=["prop_oxide", "prop_sulfide", "prop_transition"],
            name="Au_composite"
        ),
        WeightedAverage(
            variables=["Cu_oxide", "Cu_sulfide", "Cu_transition"],
            weights=["prop_oxide", "prop_sulfide", "prop_transition"],
            name="Cu_composite"
        ),

        # 2. Apply dilution
        Scale("Au_composite", 0.95, name="Au_diluted",
              comment="5% dilution from minimum mining width"),
        Scale("Cu_composite", 0.95, "Cu_diluted",
              comment="5% dilution from minimum mining width"),

        # 3. Apply recovery
        Scale("Au_diluted", 0.88, "Au_recovered",
              comment="88% metallurgical recovery"),
        Scale("Cu_diluted", 0.82, "Cu_recovered",
              comment="82% metallurgical recovery"),

        # 4. Calculate payable metal (ounces)
        Product("Au_recovered", "tonnes", "Au_ounces_total",
                comment="Total gold ounces in block"),
        Product("Cu_recovered", "tonnes", "Cu_pounds_total",
                comment="Total copper pounds in block"),

        # 5. Revenue per tonne (simplified)
        Product("Au_recovered", "1800", name="Au_revenue_raw"),  # $/oz price
        Product("Cu_recovered", "3.5", name="Cu_revenue_raw"),   # $/lb price

        # 6. Total revenue
        Sum("Au_revenue_raw", "Cu_revenue_raw", name="total_revenue"),

        # 7. Classify blocks
        CategoryFromThresholds(
            variable="total_revenue",
            thresholds=[20, 50, 100],
            categories=["waste", "low_grade", "medium_grade", "high_grade"],
            name="block_classification"
        ),
    ])

    resource_model.to_lfcalc("comprehensive_resource_model.lfcalc")

Tutorial 3: Machine Learning Integration
-----------------------------------------

Pollywog can convert scikit-learn models into Leapfrog calculations, enabling ML-powered predictions directly in your block model.

Decision Tree for Recovery Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Train a decision tree to predict metallurgical recovery:

.. code-block:: python

    import numpy as np
    from sklearn.tree import DecisionTreeRegressor
    from pollywog.conversion.sklearn import convert_tree
    from pollywog.core import CalcSet

    # Training data from metallurgical test work
    # Features: Au grade, Cu grade, grind size (P80), sulfide content (%)
    X_train = np.array([
        [1.2, 0.3, 75, 65],   # Au, Cu, P80, sulfide%
        [0.8, 0.5, 100, 45],
        [2.0, 0.2, 75, 80],
        [0.5, 0.8, 120, 30],
        [1.5, 0.4, 90, 55],
        [0.3, 0.1, 150, 20],
        [2.5, 0.6, 75, 85],
        [1.8, 0.3, 85, 70],
    ])

    # Recovery values from test work
    y_recovery = np.array([0.88, 0.82, 0.91, 0.76, 0.85, 0.72, 0.93, 0.89])

    # Train model
    model = DecisionTreeRegressor(max_depth=4, random_state=42)
    model.fit(X_train, y_recovery)

    # Convert to pollywog calculation
    feature_names = ["Au_composite", "Cu_composite", "P80", "sulfide_pct"]
    recovery_calc = convert_tree(
        model,
        feature_names,
        "Au_recovery_predicted",
        comment_equation="ML-predicted Au recovery from test work data"
    )

    # Create calcset
    ml_calcset = CalcSet([recovery_calc])
    ml_calcset.to_lfcalc("ml_recovery_model.lfcalc")

    print(f"Model exported with max depth: {model.get_depth()}")
    print(f"Feature importances: {dict(zip(feature_names, model.feature_importances_))}")

Random Forest for Grade Estimation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use random forest ensemble for more robust predictions:

.. code-block:: python

    from sklearn.ensemble import RandomForestRegressor
    from pollywog.conversion.sklearn import convert_forest
    from pollywog.core import CalcSet

    # Prepare training data
    # Features: X, Y, Z coordinates and nearby sample grades
    X_train = np.array([
        [100, 200, 50, 1.2, 0.8],  # x, y, z, nearby_Au_1, nearby_Au_2
        [150, 200, 50, 1.5, 1.0],
        [100, 250, 50, 0.9, 1.1],
        # ... more training data
    ])

    y_train = np.array([1.0, 1.3, 1.0])  # Actual Au grades

    # Train random forest
    rf = RandomForestRegressor(n_estimators=5, max_depth=3, random_state=42)
    rf.fit(X_train, y_train)

    # Convert to calcset
    feature_names = ["X", "Y", "Z", "nearby_Au_1", "nearby_Au_2"]
    rf_calc = convert_forest(
        rf,
        feature_names,
        "Au_rf_estimate",
        comment_equation="Random Forest grade estimate"
    )

    # Export
    CalcSet([rf_calc]).to_lfcalc("rf_estimation.lfcalc")

Classification Models for Geological Domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use decision trees to classify geological domains:

.. code-block:: python

    from sklearn.tree import DecisionTreeClassifier
    from pollywog.conversion.sklearn import convert_tree
    from pollywog.core import CalcSet

    # Training data - geochemical signatures
    X_train = np.array([
        [0.2, 0.1, 5, 3],    # Low Au, Low Cu -> oxide
        [1.5, 0.8, 20, 5],   # High Au, High Cu -> sulfide
        [0.8, 0.4, 10, 4],   # Medium Au, Cu -> transition
        [0.3, 0.05, 3, 2.5], # Low values -> oxide
        [2.0, 1.0, 25, 6],   # High values -> sulfide
        # ... more training data
    ])

    y_train = ["oxide", "sulfide", "transition", "oxide", "sulfide"]

    # Train classifier
    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)

    # Convert to pollywog (Category output)
    feature_names = ["Au_composite", "Cu_composite", "Ag_composite", "Fe_pct"]
    domain_calc = convert_tree(
        clf,
        feature_names,
        "predicted_domain",
        comment_equation="ML-predicted geological domain from geochemistry"
    )

    # Export
    CalcSet([domain_calc]).to_lfcalc("ml_domain_prediction.lfcalc")

Tutorial 4: Querying and Filtering CalcSets
--------------------------------------------

Pollywog provides powerful querying capabilities similar to pandas DataFrames, allowing you to filter and manipulate calculation sets programmatically.

Basic Querying
~~~~~~~~~~~~~~

Filter calculations by name or attributes:

.. code-block:: python

    from pollywog.core import CalcSet, Number

    # Create a large calcset
    all_calcs = CalcSet([
        Number(name="Au_clean", expression=["clamp([Au], 0)"]),
        Number(name="Au_log", expression=["log([Au_clean] + 1e-6)"]),
        Number(name="Ag_clean", expression=["clamp([Ag], 0)"]),
        Number(name="Ag_log", expression=["log([Ag_clean] + 1e-6)"]),
        Number(name="Cu_clean", expression=["clamp([Cu], 0)"]),
        Number(name="Cu_log", expression=["log([Cu_clean] + 1e-6)"]),
    ])

    # Get only gold calculations
    au_calcs = all_calcs.query('name.startswith("Au")')
    print(f"Gold calculations: {[item.name for item in au_calcs.items]}")
    # Output: ['Au_clean', 'Au_log']

    # Get all log transforms
    log_calcs = all_calcs.query('"log" in name')
    print(f"Log transforms: {[item.name for item in log_calcs.items]}")
    # Output: ['Au_log', 'Ag_log', 'Cu_log']

.. TODO: Add screenshot showing query results in Jupyter
.. .. image:: _static/query_example.png
..    :alt: Query results showing filtered calculations
..    :align: center
..    :width: 85%
..
.. |

Advanced Queries with External Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use external variables in queries:

.. code-block:: python

    # Define metals of interest
    metals_of_interest = ["Au", "Ag"]

    # Query using external variable
    selected = all_calcs.query('any(name.startswith(metal) for metal in @metals_of_interest)')

    # Or pass as keyword argument
    selected = all_calcs.query('any(name.startswith(metal) for metal in metals)',
                                metals=metals_of_interest)

Using Regular Expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~

Filter using regex patterns:

.. code-block:: python

    import re

    # Find all calculations ending with _clean or _log
    pattern = r'_(clean|log)$'
    filtered = all_calcs.query('re.match(@pattern, name)', pattern=pattern)

Combining Query Results
~~~~~~~~~~~~~~~~~~~~~~~~

Build new calcsets from filtered results:

.. code-block:: python

    # Get preprocessing steps
    preprocessing = all_calcs.query('"clean" in name')

    # Get transformation steps
    transformations = all_calcs.query('"log" in name')

    # Combine into separate exports
    preprocessing.to_lfcalc("01_preprocessing.lfcalc")
    transformations.to_lfcalc("02_transformations.lfcalc")

Tutorial 5: Working with Conditional Logic
-------------------------------------------

Master the use of If/Else statements for domain-based and conditional calculations.

Simple Conditionals
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pollywog.core import CalcSet, Number, If

    # Simple threshold
    calcset = CalcSet([
        Number(name="mineable", expression=[
            If("[Au] >= 0.3", "1", "0")
        ], comment_equation="Binary mineable flag, cutoff = 0.3 g/t"),
    ])

Multi-Condition Logic
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pollywog.core import CalcSet, Number, If, IfRow

    # Multiple conditions with different outcomes
    calcset = CalcSet([
        Number(name="recovery_factor", expression=[
            If([
                ("[domain] = 'oxide' and [grind] <= 75", "0.92"),
                ("[domain] = 'oxide' and [grind] > 75", "0.88"),
                ("[domain] = 'sulfide' and [grind] <= 75", "0.85"),
                ("[domain] = 'sulfide' and [grind] > 75", "0.78"),
            ], otherwise=["0.75"])
        ], comment_equation="Recovery based on domain and grind size"),
    ])

Nested Conditionals
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pollywog.core import CalcSet, Category, If

    # Complex classification
    calcset = CalcSet([
        Category(name="material_type", expression=[
            If([
                ("[Au] >= 3", "'high_grade_ore'"),
                ("[Au] >= 1 and [depth] <= 300", "'medium_grade_ore'"),
                ("[Au] >= 0.5 and [depth] <= 200", "'low_grade_ore'"),
                ("[Au] >= 0.5", "'stockpile'"),
            ], otherwise=["'waste'"])
        ], comment_equation="Material classification by grade and depth"),
    ])

Next Steps
----------

After completing these tutorials, you should be comfortable with:

- Building complete resource estimation workflows
- Using helper functions effectively
- Integrating machine learning models
- Querying and filtering calculation sets
- Implementing conditional logic

For more information:

- :doc:`expression_syntax` - Detailed guide to Leapfrog expression syntax
- :doc:`workflow_patterns` - Common workflow patterns and examples
- :doc:`helpers_guide` - Complete helper function reference
- :doc:`best_practices` - Best practices for production workflows
- :doc:`api_reference` - Full API documentation
