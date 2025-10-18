Getting Started
===============

Welcome to pollywog! This guide will help you install the library, understand the basics, run your first calculation, and explore further resources.

What You Need to Know
----------------------

Before using pollywog, it's helpful to understand:

- **Python basics**: Functions, lists, dictionaries, and imports
- **Leapfrog concepts**: Block models, drillholes, calculations
- **.lfcalc files**: Leapfrog calculation set files

You don't need to be a Python expert—pollywog is designed to be accessible to geologists and mining engineers with basic programming knowledge.

Installation
------------

Install from PyPI
~~~~~~~~~~~~~~~~~

The easiest way to install pollywog:

.. code-block:: bash

    pip install lf_pollywog

Install with Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For machine learning model conversion (scikit-learn):

.. code-block:: bash

    pip install lf_pollywog[conversion]

For development (includes testing tools):

.. code-block:: bash

    pip install lf_pollywog[dev]

Install from GitHub
~~~~~~~~~~~~~~~~~~~

To get the latest development version:

.. code-block:: bash

    pip install git+https://github.com/endarthur/pollywog.git

Verify Installation
~~~~~~~~~~~~~~~~~~~

Check that pollywog is installed correctly:

.. code-block:: python

    import pollywog as pw
    print(pw.__version__)  # Should print version number

Try in Your Browser
~~~~~~~~~~~~~~~~~~~

Don't want to install yet? Try pollywog in your browser using JupyterLite:

    https://endarthur.github.io/pollyweb

.. note::
    JupyterLite saves files in browser memory—download your work regularly to avoid losing it!

Basic Concepts
--------------

CalcSet
~~~~~~~

A ``CalcSet`` is a collection of calculation items that can be exported to a ``.lfcalc`` file:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    
    calcset = CalcSet([
        Number(name="Au_clean", children=["clamp([Au], 0)"]),
        Number(name="Au_log", children=["log([Au_clean] + 1e-6)"]),
    ])

Number
~~~~~~

``Number`` represents a numeric calculation (integers or floats):

.. code-block:: python

    from pollywog.core import Number
    
    # Simple calculation
    grade_calc = Number(name="Au_final", children=["[Au] * 0.95"])
    
    # With comment
    grade_calc = Number(
        name="Au_final",
        children=["[Au] * 0.95"],
        comment_equation="Apply 5% dilution factor"
    )

Category
~~~~~~~~

``Category`` represents a categorical/text calculation:

.. code-block:: python

    from pollywog.core import Category, If
    
    # Categorical output
    ore_type = Category(name="material_class", children=[
        If("[Au] >= 0.5", "'ore'", "'waste'")
    ])

Variable References
~~~~~~~~~~~~~~~~~~~

Variables are referenced using square brackets: ``[variable_name]``

.. code-block:: python

    # Reference drillhole assays
    Number(name="precious_metals", children=["[Au] + [Ag]"])
    
    # Reference block model variables
    Number(name="density_calc", children=["[block_density] * [block_volume]"])

Your First Calculation
-----------------------

Let's create a simple calculation set step by step:

Step 1: Import pollywog
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pollywog.core import CalcSet, Number

Step 2: Create Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Create individual calculations
    au_clean = Number(
        name="Au_clean",
        children=["clamp([Au], 0)"],
        comment_equation="Remove negative values"
    )
    
    au_scaled = Number(
        name="Au_scaled",
        children=["[Au_clean] * 0.95"],
        comment_equation="Apply 95% factor"
    )

Step 3: Build a CalcSet
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Combine into a CalcSet
    calcset = CalcSet([au_clean, au_scaled])

Step 4: Export to Leapfrog
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Export to .lfcalc file
    calcset.to_lfcalc("my_calculations.lfcalc")
    
    print(f"Exported {len(calcset.items)} calculations")

.. note::
    In JupyterLite and Jupyter Notebooks, Pollywog provides an extension that makes a download button appear below the cell when you export with ``to_lfcalc``. To enable this feature, first run ``%load_ext pollywog.magics`` in a cell, then ``%pollywog autodownload on``. When you export, simply click the button to save the file to your computer.

Step 5: Use in Leapfrog
~~~~~~~~~~~~~~~~~~~~~~~~

1. Open Leapfrog
2. Navigate to your block model, drillhole, or mesh
3. Right-click on "Evaluations" or "Numeric" section
4. Select "Import" → "From File"
5. Choose your ``my_calculations.lfcalc`` file
6. The calculations will appear in your evaluation tree

Common Workflows
----------------

Drillhole Preprocessing
~~~~~~~~~~~~~~~~~~~~~~~

Clean and transform drillhole assay data:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    
    preprocessing = CalcSet([
        # Remove outliers
        Number(name="Au_capped", children=["clamp([Au], 0, 100)"],
               comment_equation="Cap gold at 100 g/t"),
        Number(name="Cu_capped", children=["clamp([Cu], 0, 5)"],
               comment_equation="Cap copper at 5%"),
        
        # Log transforms for kriging
        Number(name="Au_log", children=["log([Au_capped] + 0.01)"]),
        Number(name="Cu_log", children=["log([Cu_capped] + 0.01)"]),
    ])
    
    preprocessing.to_lfcalc("drillhole_preprocessing.lfcalc")

Block Model Postprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Process estimated grades in a block model:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    from pollywog.helpers import WeightedAverage
    
    postprocessing = CalcSet([
        # Back-transform from log space
        Number(name="Au_est", children=["exp([Au_log_kriged]) - 0.01"]),
        
        # Apply dilution
        Number(name="Au_diluted", children=["[Au_est] * 0.95"]),
        
        # Apply recovery
        Number(name="Au_recovered", children=["[Au_diluted] * 0.88"]),
    ])
    
    postprocessing.to_lfcalc("block_postprocessing.lfcalc")

Domain Weighting
~~~~~~~~~~~~~~~~

Combine estimates from multiple domains:

.. code-block:: python

    from pollywog.helpers import WeightedAverage
    from pollywog.core import CalcSet
    
    domain_weighted = CalcSet([
        WeightedAverage(
            variables=["Au_oxide", "Au_sulfide", "Au_transition"],
            weights=["prop_oxide", "prop_sulfide", "prop_transition"],
            name="Au_composite"
        )
    ])
    
    domain_weighted.to_lfcalc("domain_weighted.lfcalc")

Working with Helpers
--------------------

Pollywog provides helper functions to simplify common patterns:

.. code-block:: python

    from pollywog.helpers import Sum, Product, Scale, CategoryFromThresholds
    from pollywog.core import CalcSet
    
    helpers_example = CalcSet([
        # Sum multiple variables
        Sum("Au", "Ag", "Cu", name="total_metals"),
        
        # Multiply variables
        Product("grade", "tonnage", name="metal_content"),
        
        # Scale by a factor
        Scale("Au", 0.95, name="Au_diluted"),
        
        # Categorize by thresholds
        CategoryFromThresholds(
            variable="Au",
            thresholds=[0.5, 2.0],
            categories=["low", "medium", "high"],
            name="grade_class"
        ),
    ])
    
    helpers_example.to_lfcalc("helpers_example.lfcalc")

Visualization in Jupyter
-------------------------

Display calculation sets as interactive HTML in Jupyter notebooks:

.. code-block:: python

    from pollywog.display import display_calcset, set_theme
    
    # Set theme (optional)
    set_theme("light")  # or "dark"
    
    # Display the calcset
    display_calcset(calcset)

This creates an interactive tree view showing:

- Calculation names
- Expressions
- Dependencies between calculations
- Comments and metadata

Reading Existing Files
----------------------

Load and modify existing .lfcalc files:

.. code-block:: python

    from pollywog.core import CalcSet
    
    # Read existing file
    existing = CalcSet.read_lfcalc("existing_calculations.lfcalc")
    
    # View contents
    print(f"Loaded {len(existing.items)} calculations")
    for item in existing.items:
        print(f"  - {item.name}")
    
    # Modify
    from pollywog.core import Number
    existing.items.append(
        Number(name="new_calc", children=["[existing_var] * 2"])
    )
    
    # Save modified version
    existing.to_lfcalc("modified_calculations.lfcalc")

Tips for Success
----------------

1. **Start Simple**: Begin with basic calculations and add complexity incrementally
2. **Use Comments**: Document your logic with ``comment_equation`` parameter
3. **Test Small**: Export small test files and verify in Leapfrog before scaling up
4. **Check Dependencies**: Use ``item.dependencies`` to see what variables are referenced
5. **Organize Code**: Keep related calculations together in the same CalcSet
6. **Version Control**: Store your Python scripts in Git for traceability
7. **Validate Data**: Use ``clamp()`` to handle invalid inputs (negatives, outliers)
8. **Break It Down**: Split complex expressions into multiple simple calculations

Common Pitfalls
---------------

**Forgetting Square Brackets**

.. code-block:: python

    # Wrong - Au is treated as undefined variable
    Number(name="result", children=["Au * 2"])
    
    # Correct - Au is a reference to existing variable
    Number(name="result", children=["[Au] * 2"])

**Division by Zero**

.. code-block:: python

    # Risky
    Number(name="ratio", children=["[a] / [b]"])
    
    # Safe
    Number(name="ratio", children=["[a] / ([b] + 1e-10)"])
    Number(name="ratio", children=["[a] / clamp([b], 0.001)"])

**Log of Zero**

.. code-block:: python

    # Risky
    Number(name="Au_log", children=["log([Au])"])
    
    # Safe
    Number(name="Au_log", children=["log([Au] + 1e-6)"])

**Missing Parentheses**

.. code-block:: python

    # Ambiguous - may not compute as intended
    Number(name="result", children=["[a] + [b] * [c]"])
    
    # Clear
    Number(name="result", children=["[a] + ([b] * [c])"])

Next Steps
----------

Now that you understand the basics, explore:

- :doc:`tutorials` - Step-by-step workflow examples
- :doc:`expression_syntax` - Complete expression syntax reference
- :doc:`helpers_guide` - Detailed helper function documentation
- :doc:`workflow_patterns` - Common patterns and best practices
- :doc:`best_practices` - Production workflow recommendations
- :doc:`api_reference` - Full API documentation

Additional Resources
--------------------

- **GitHub Repository**: https://github.com/endarthur/pollywog
- **JupyterLite Demo**: https://endarthur.github.io/pollyweb
- **Example Notebooks**: Check the ``examples/`` folder in the repository
- **Issue Tracker**: Report bugs or request features on GitHub

Getting Help
------------

If you encounter issues:

1. Check the documentation for similar examples
2. Review the example notebooks in the repository
3. Search existing GitHub issues
4. Open a new issue with a minimal reproducible example
