Getting Started
===============

Welcome to pollywog! This guide will help you install the library, run your first calculation, and explore further resources.

Installation
------------

.. code-block:: bash

    pip install lf_pollywog

Basic Usage
-----------

.. code-block:: python

    from pollywog.core import CalcSet, Number
    calcset = CalcSet([
        Number(name="Au_est", children=["block[Au] * 0.95"]),
        Number(name="Ag_est", children=["block[Ag] * 0.85"])
    ])

    # Display in Jupyter
    from pollywog.display import display_calcset
    display_calcset(calcset)

    # Export to Leapfrog format
    calcset.to_lfcalc("my_calcset.lfcalc")

Next Steps
----------

- Read the :doc:`tutorials` for step-by-step guides
- See the :doc:`api_reference` for all classes and functions
- Explore example notebooks in the `examples/` folder

Troubleshooting
---------------

If you encounter issues, check the FAQ (coming soon) or open an issue on GitHub.
