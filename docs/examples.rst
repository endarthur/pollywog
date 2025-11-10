Example Notebooks
==================

Pollywog includes a comprehensive collection of Jupyter notebooks demonstrating common workflows and advanced features. All examples are available in the `examples/ folder on GitHub <https://github.com/endarthur/pollywog/tree/main/examples>`_ and can be run interactively in your browser at `JupyterLite <https://endarthur.github.io/pollyweb>`_.

.. note::
   **Try examples in your browser!**

   Visit https://endarthur.github.io/pollyweb to run all examples interactively without installing anything. Perfect for learning and experimentation!

Getting Started
---------------

**For beginners**, start with these notebooks in order:

1. :ref:`basic_usage` - Core concepts and file I/O
2. :ref:`item_types_guide` - Understanding Variable, Number, Category, Filter
3. :ref:`helper_functions` - Using helper functions for common patterns

**For experienced users**, explore specific topics:

- :ref:`conditional_logic` - Advanced If statements and nested conditions
- :ref:`pollywog_workflow_tutorial` - Complete mining workflow example
- :ref:`dependency_analysis` - Understanding calculation dependencies
- :ref:`modifying_lfcalc` - Read, modify, and save existing .lfcalc files

Core Concepts
-------------

.. _basic_usage:

Basic Usage
~~~~~~~~~~~

**File:** `basic_usage.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/basic_usage.ipynb>`_

**Topics covered:**

- Creating CalcSet objects
- Creating Number, Category, and Filter calculations
- Writing to .lfcalc files
- Reading existing .lfcalc files
- Postprocessing variable estimates
- Domain-weighted calculations
- Thresholding and classification
- Scikit-learn model conversion

**Best for:** First-time pollywog users, general reference

.. code-block:: python

    from pollywog.core import CalcSet, Number

    calcset = CalcSet([
        Number("Au_diluted", "[Au_est] * 0.95")
    ])
    calcset.to_lfcalc("output.lfcalc")

----

.. _item_types_guide:

Item Types Guide
~~~~~~~~~~~~~~~~

**File:** `item_types_guide.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/item_types_guide.ipynb>`_

**Topics covered:**

- Variable vs Number vs Category vs Filter
- When to use each type
- Visibility in Leapfrog (calculator vs everywhere)
- Decision flow for choosing types
- Complete workflow using all types

**Best for:** Understanding which item type to use when

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Type
     - Visible Outside Calculator?
     - Use Case
   * - Variable
     - ❌ No
     - Intermediate calculations
   * - Number
     - ✅ Yes
     - Final numeric outputs
   * - Category
     - ✅ Yes
     - Classifications and labels
   * - Filter
     - ✅ Yes
     - Boolean inclusion rules

----

.. _conditional_logic:

Conditional Logic
~~~~~~~~~~~~~~~~~

**File:** `conditional_logic.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/conditional_logic.ipynb>`_

**Topics covered:**

- Basic If/otherwise patterns
- Multiple conditions
- Complex conditions with logical operators
- Nested If statements
- Mill feed decision trees
- Handling missing data
- Practical mining examples

**Best for:** Building complex conditional logic

.. code-block:: python

    from pollywog.core import Number, Category, If

    # Multi-class classification
    ore_class = Category(
        "ore_class",
        If(
            [
                ("[Au] < 0.3", "'waste'"),
                ("[Au] < 1.0", "'low_grade'"),
                ("[Au] < 3.0", "'medium_grade'"),
            ],
            "'high_grade'"
        )
    )

Helper Functions
----------------

.. _helper_functions:

Helper Functions Showcase
~~~~~~~~~~~~~~~~~~~~~~~~~

**File:** `helper_functions.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/helper_functions.ipynb>`_

**Topics covered:**

- Mathematical helpers (Sum, Product, Average)
- **WeightedAverage** (critical for multi-domain modeling!)
- WeightedSum
- Scale (dilution, recovery, unit conversion)
- Normalize (proportions)
- CategoryFromThresholds (grade classification)
- Dual-mode usage (with/without name parameter)
- Composing helpers for complex expressions

**Best for:** Learning all available helper functions

.. code-block:: python

    from pollywog.helpers import WeightedAverage, Scale, CategoryFromThresholds

    # Domain-weighted grade
    au_composite = WeightedAverage(
        variables=["Au_oxide", "Au_sulfide", "Au_transition"],
        weights=["prop_oxide", "prop_sulfide", "prop_transition"],
        name="Au_composite"
    )

    # Apply dilution
    au_diluted = Scale("Au_composite", 0.95, name="Au_diluted")

    # Classify
    ore_class = CategoryFromThresholds(
        variable="Au_diluted",
        thresholds=[0.5, 2.0],
        categories=["waste", "low_grade", "high_grade"],
        name="ore_class"
    )

Complete Workflows
------------------

.. _pollywog_workflow_tutorial:

Complete Mining Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~

**File:** `pollywog_workflow_tutorial.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/pollywog_workflow_tutorial.ipynb>`_

**Topics covered:**

- Preprocessing drillhole data
- Postprocessing block model grades
- Domain-weighted calculations
- Scikit-learn regression trees for recovery
- Helper functions in practice
- Visualization in Jupyter

**Best for:** End-to-end resource estimation workflow

----

.. _dependency_analysis:

Dependency Analysis
~~~~~~~~~~~~~~~~~~~

**File:** `dependency_analysis.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/dependency_analysis.ipynb>`_

**Topics covered:**

- Automatic dependency extraction
- Topological sorting (resolving calculation order)
- External dependencies (variables from Leapfrog)
- Circular dependency detection
- Analyzing complex workflows
- Debugging dependency issues

**Best for:** Understanding and debugging calculation order

.. code-block:: python

    # Dependencies are automatically extracted
    calc = Number("result", "[a] + [b] * [c]")
    print(calc.dependencies)  # {'a', 'b', 'c'}

    # Sort calculations by dependencies
    sorted_calcset = calcset.topological_sort()

----

.. _modifying_lfcalc:

Modifying .lfcalc Files
~~~~~~~~~~~~~~~~~~~~~~~

**File:** `modifying_lfcalc_files.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/modifying_lfcalc_files.ipynb>`_

**Topics covered:**

- Reading .lfcalc files
- Querying and filtering calculations
- Modifying existing calculations
- Adding new calculations
- Removing calculations
- Batch modifications
- Merging multiple files
- Version control workflows

**Best for:** Working with existing Leapfrog calculations

.. code-block:: python

    # Load existing file
    calcset = CalcSet.read_lfcalc("existing.lfcalc")

    # Query by name
    au_calcs = calcset.query('name.startswith("Au")')

    # Modify
    for item in calcset.items:
        if "diluted" in item.name:
            item.expression = ["[Au_est] * 0.95"]

    # Save
    calcset.to_lfcalc("modified.lfcalc")

Advanced Topics
---------------

Querying CalcSets
~~~~~~~~~~~~~~~~~

**File:** `querying_calcsets.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/querying_calcsets.ipynb>`_

**Topics covered:**

- Query method basics
- Filtering by name, type, or attributes
- Using external variables in queries
- Practical query examples

.. code-block:: python

    # Query by name pattern
    subset = calcset.query('name.startswith("Au")')

    # Query by comment
    estimates = calcset.query('"estimate" in comment_equation')

    # Use external variable
    prefix = "Cu"
    subset = calcset.query('name.startswith(@prefix)')

----

Running with DataFrames
~~~~~~~~~~~~~~~~~~~~~~~

**File:** `running_with_dataframe.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/running_with_dataframe.ipynb>`_

**Topics covered:**

- Running calculations on pandas DataFrames
- Using ``run_calcset()`` function
- Using pandas accessor (``df.pw.run()``)
- Testing calculations before deploying

.. code-block:: python

    import pandas as pd
    from pollywog.run import run_calcset

    # Test on DataFrame
    df = pd.DataFrame({"Au": [1.0, 2.0, 3.0]})
    result = run_calcset(calcset, dataframe=df)

    # Or use accessor
    result = df.pw.run(calcset)

----

Scikit-learn Conversion
~~~~~~~~~~~~~~~~~~~~~~~

**File:** `sklearn_conversion.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/sklearn_conversion.ipynb>`_

**Topics covered:**

- Converting decision trees to calculations
- Converting random forests
- Converting linear models
- Inspecting converted calculations

.. code-block:: python

    from sklearn.tree import DecisionTreeRegressor
    from pollywog.conversion.sklearn import convert_tree

    # Train model
    reg = DecisionTreeRegressor().fit(X, y)

    # Convert to calculation
    calc = convert_tree(reg, feature_names, "prediction")

    # Add to CalcSet
    calcset = CalcSet([calc])

----

Display and Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~

**File:** `display_final_workflow.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/display_final_workflow.ipynb>`_

**Topics covered:**

- Loading and displaying .lfcalc files
- Interactive visualization in Jupyter
- Theming (light/dark mode)

.. code-block:: python

    from pollywog.display import display_calcset, set_theme

    set_theme("dark")
    display_calcset(calcset)

JupyterLite Specific
--------------------

JupyterLite Quickstart
~~~~~~~~~~~~~~~~~~~~~~

**File:** `jupyterlite_quickstart.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/jupyterlite_quickstart.ipynb>`_

**Topics covered:**

- Running pollywog in the browser
- Creating simple workflows
- Exporting files for download

**Best for:** First-time JupyterLite users

----

JupyterLite Demo
~~~~~~~~~~~~~~~~

**File:** `jupyterlite_demo.ipynb <https://github.com/endarthur/pollywog/blob/main/examples/jupyterlite_demo.ipynb>`_

**Topics covered:**

- Pollywog magic commands
- Autodownload feature
- Manual download utilities
- Working with browser storage

.. code-block:: python

    # Enable autodownload
    %load_ext pollywog.magics
    %pollywog autodownload on

    # Now exports trigger download
    calcset.to_lfcalc("output.lfcalc")

Quick Reference by Task
-----------------------

**I want to...**

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Task
     - See Example
   * - Create my first calculation set
     - :ref:`basic_usage`
   * - Understand Variable vs Number vs Category
     - :ref:`item_types_guide`
   * - Use If statements and conditions
     - :ref:`conditional_logic`
   * - Apply dilution and recovery factors
     - :ref:`helper_functions` (Scale helper)
   * - Combine domain estimates
     - :ref:`helper_functions` (WeightedAverage)
   * - Classify by grade thresholds
     - :ref:`helper_functions` (CategoryFromThresholds)
   * - Build a complete resource workflow
     - :ref:`pollywog_workflow_tutorial`
   * - Fix calculation order issues
     - :ref:`dependency_analysis`
   * - Update existing .lfcalc files
     - :ref:`modifying_lfcalc`
   * - Filter calculations by name
     - Querying CalcSets
   * - Test calculations on data
     - Running with DataFrames
   * - Use machine learning models
     - Scikit-learn Conversion
   * - Try pollywog without installing
     - :ref:`JupyterLite Quickstart`

Running the Examples
--------------------

**Option 1: JupyterLite (No Installation)**

Visit https://endarthur.github.io/pollyweb and open any notebook. Everything runs in your browser!

**Option 2: Local Installation**

.. code-block:: bash

    # Install pollywog
    pip install lf_pollywog

    # Clone repository for examples
    git clone https://github.com/endarthur/pollywog.git
    cd pollywog/examples

    # Start Jupyter
    jupyter notebook

**Option 3: Individual Files**

Download individual notebooks from `GitHub <https://github.com/endarthur/pollywog/tree/main/examples>`_ and run locally.

Next Steps
----------

After exploring the examples:

1. **Read the guides:**

   - :doc:`expression_syntax` - Leapfrog expression syntax reference
   - :doc:`helpers_guide` - Detailed helper function documentation
   - :doc:`workflow_patterns` - Common patterns and best practices

2. **Check the API:**

   - :doc:`api_reference` - Complete API documentation

3. **Get help:**

   - `GitHub Issues <https://github.com/endarthur/pollywog/issues>`_ - Report bugs or request features
   - `GitHub Discussions <https://github.com/endarthur/pollywog/discussions>`_ - Ask questions and share ideas
