
Tutorials
=========

This tutorial demonstrates a complete workflow using pollywog: preprocessing multivariate drillhole data (for drillholes), estimating grades in Leapfrog, postprocessing results on a block model (for blocks) using domain proportions for percentile estimation, and adding geometallurgical recovery using regression trees.

.. note::
    This tutorial is also available as a Jupyter notebook: `examples/pollywog_workflow_tutorial.ipynb <https://github.com/endarthur/pollywog/examples/pollywog_workflow_tutorial.ipynb>`_

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
            values=[f"[{v}_{d}]" for d in domains],
            weights=[f"[prop_{d}]" for d in domains],
            name=f"{v}_final_weighted"
        ) for v in variables],
    ])

    # Export for use in Leapfrog (block model)
    postprocess_manual.to_lfcalc("blockmodel_postprocessing_manual.lfcalc")
    postprocess_helper.to_lfcalc("blockmodel_postprocessing_weighted.lfcalc")

Step 4: Geometallurgical Recovery with Regression Trees
------------------------------------------------------
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
-------------------------------
You can visualize any CalcSet in Jupyter for inspection.

.. code-block:: python

    from pollywog.display import display_calcset, set_theme
    set_theme("light")
    display_calcset(preprocess)
    display_calcset(postprocess_manual)
    display_calcset(postprocess_helper)

For more advanced notebooks and real data examples, see the ``examples/`` folder in the repository.

Step 6: More Helper Function Examples
-------------------------------------
Pollywog provides several helpers to simplify common calculation patterns. Here are some examples:

.. code-block:: python

    from pollywog.helpers import Sum, Product, Normalize, Scale, IfElse, CategoryFromThresholds

    # Sum: Add several variables together
    sum_example = Sum(["[Au_final]", "[Ag_final]", "[Cu_final]"], name="Total_Metals")

    # Product: Multiply variables (e.g., grade * recovery)
    product_example = Product(["[Au_final]", "[Au_recovery]"], name="Au_payable")

    # Normalize: Normalize proportions so they sum to 1
    normalize_example = Normalize(["[prop_high]", "[prop_medium]", "[prop_low]"], name="DomainProportionsNorm")

    # Scale: Apply a scaling factor to a variable
    scale_example = Scale("[Au_final]", 0.95, name="Au_final_scaled")

    # CategoryFromThresholds: Categorize based on thresholds
    cat_example = CategoryFromThresholds(
        value="[Au_final]",
        thresholds=[0.3, 1.0],
        categories=["Low", "Medium", "High"],
        name="AuCategory"
    )

    # Add these to a CalcSet and export
    helpers_calcset = CalcSet([
        sum_example,
        product_example,
        normalize_example,
        scale_example,
        cat_example,
    ])
    helpers_calcset.to_lfcalc("blockmodel_helpers_examples.lfcalc")

    # Visualize in Jupyter
    display_calcset(helpers_calcset)
