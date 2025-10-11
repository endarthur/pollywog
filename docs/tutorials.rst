Tutorials
=========

This section provides step-by-step guides for using pollywog in real-world scenarios. Each tutorial demonstrates a key feature or workflow.

Creating a Basic Calculation Set
--------------------------------

.. code-block:: python

    from pollywog.core import CalcSet, Number
    calcset = CalcSet([
        Number(name="Au_est", children=["block[Au] * 0.95"]),
        Number(name="Ag_est", children=["block[Ag] * 0.85"])
    ])

Displaying Calculations in Jupyter
----------------------------------

.. code-block:: python

    from pollywog.display import display_calcset, set_theme
    set_theme("light")
    display_calcset(calcset)

Using Categories and Conditional Logic
--------------------------------------

.. code-block:: python

    from pollywog.core import Category, If, Number
    calcset = CalcSet([
        Category("Metals", [
            Number("Au_est", ["block[Au] * 0.95"]),
            Number("Ag_est", ["block[Ag] * 0.85"])
        ]),
        If("block[Au] > 1", then=[Number("High_Au", ["block[Au] * 1.1"])], else_=[Number("Low_Au", ["block[Au] * 0.9"])])
    ])

Exporting to Leapfrog Format
----------------------------

.. code-block:: python

    calcset.to_lfcalc("my_calcset.lfcalc")

Querying Calculation Sets
-------------------------

.. code-block:: python

    result = calcset.query("Au_est")
    print(result)

Postprocessing Calculations
--------------------------

.. code-block:: python

    variables = ["Ag_est", "Au_est"]
    postprocessed = [
        Number(name=f"{v}_corr", children=[f"clamp([{v}], 0.01)"]) for v in variables
    ]
    calcset_post = CalcSet(postprocessed)

For more examples, see the ``examples/`` folder in the repository.
