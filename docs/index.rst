
Welcome to pollywog's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting_started
   geologist_tutorial
   tutorials

.. note::
   **Choose your learning path:**

   - **Python users**: Start with :doc:`getting_started` for a quick overview
   - **Geologists new to Python**: Start with :doc:`geologist_tutorial` for step-by-step guidance
   - **Advanced workflows**: See :doc:`tutorials` for complete project examples

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   expression_syntax
   workflow_patterns
   helpers_guide
   best_practices
   examples

.. toctree::
   :maxdepth: 2
   :caption: Reference

   api_reference

Introduction
------------

**pollywog** is a Python library designed to make it easy to build, manipulate, and visually inspect Leapfrog-style calculation sets—especially when those sets are large, complex, or involve repetitive logic.

When to Use Pollywog
~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   flowchart TD
      A{How many calculations?} -->|1-5| B[Use Leapfrog UI]
      A -->|10+| C{Repetitive pattern?}
      C -->|Yes| D[✓ Use pollywog]
      C -->|No| E{Complex logic?}
      E -->|Yes| D
      E -->|No| B

      F{Need version control?} -->|Yes| D
      F -->|No| G{Reuse across projects?}
      G -->|Yes| D
      G -->|No| B

      H{ML model integration?} --> D

      style D fill:#7cb342,stroke:#333,stroke-width:2px,color:#fff
      style B fill:#999,stroke:#333,stroke-width:2px,color:#fff

What is Leapfrog?
~~~~~~~~~~~~~~~~~

`Leapfrog <https://www.seequent.com/products-solutions/leapfrog-geo/>`_ is industry-leading 3D geological modeling software developed by Seequent. It is widely used in mining and resource estimation for:

- **Drillhole database management** and visualization
- **Geological modeling** (surfaces, solids, block models)
- **Grade estimation** (kriging, IDW, nearest neighbor) with Leapfrog Edge
- **Resource and reserve calculation**

Leapfrog uses **calculation sets** (``.lfcalc`` files) to define formulas and transformations applied to data. These calculations can become complex when dealing with multiple domains, conditional logic, and multi-commodity resources.

Why pollywog?
~~~~~~~~~~~~~

**Problems pollywog solves:**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Challenge
     - Solution
   * - 📝 **Large calculation sets**
     - Generate hundreds of calculations programmatically instead of point-and-click
   * - 🔀 **Complex logic**
     - Use Python's control flow (loops, conditionals) to build calculations
   * - 🔁 **Repetitive tasks**
     - Automate patterns with helper functions and templates
   * - 🔍 **Hard to review**
     - Display calculation trees interactively in Jupyter notebooks
   * - 🤖 **ML integration**
     - Deploy scikit-learn models directly as Leapfrog calculations
   * - 📋 **Version control**
     - Keep calculation logic in Git-trackable Python scripts
   * - 🧪 **Testing**
     - Write unit tests for calculation logic before deploying

**By using pollywog, you can:**

- ✅ Automate creation and modification of calculation sets
- ✅ Refactor and query calculations with code
- ✅ Export directly to Leapfrog ``.lfcalc`` format
- ✅ Visualize and validate logic interactively
- ✅ Deploy machine learning models in resource models
- ✅ Maintain calculation logic in version-controlled scripts

Quick Example
~~~~~~~~~~~~~

Here's a simple example showing pollywog's power – creating a complete resource estimation postprocessing workflow in just a few lines:

.. code-block:: python

    from pollywog.core import CalcSet, Number
    from pollywog.helpers import WeightedAverage, CategoryFromThresholds

    # Build a complete calculation set
    calcset = CalcSet([
        # 1. Weighted average across geological domains
        WeightedAverage(
            variables=["Au_oxide", "Au_sulfide", "Au_transition"],
            weights=["prop_oxide", "prop_sulfide", "prop_transition"],
            name="Au_composite",
            comment="Domain-weighted gold grade"
        ),

        # 2. Apply dilution and recovery
        Number(name="Au_diluted", expression=["[Au_composite] * 0.95"],
               comment_equation="5% dilution factor"),
        Number(name="Au_recovered", expression=["[Au_diluted] * 0.88"],
               comment_equation="88% metallurgical recovery"),

        # 3. Classify by grade
        CategoryFromThresholds(
            variable="Au_recovered",
            thresholds=[0.3, 1.0, 3.0],
            categories=["waste", "low_grade", "medium_grade", "high_grade"],
            name="ore_class",
            comment="Material classification"
        ),
    ])

    # Export to Leapfrog - done!
    calcset.to_lfcalc("resource_model.lfcalc")

**Compare this to manually creating 6+ calculations in Leapfrog's UI!** 🎉

.. note::
   This example creates 6 calculations that would take 10-15 minutes to build manually in Leapfrog. With pollywog, it takes seconds and is version-controlled, testable, and reusable!

Key Features
~~~~~~~~~~~~

**Core Functionality:**

- Read and write Leapfrog ``.lfcalc`` files
- Programmatically create calculations with ``Number``, ``Category``, ``Variable``, and ``Filter`` types
- Build conditional logic with ``If``/``Else`` statements
- Query and filter calculation sets like pandas DataFrames

**Helper Functions:**

- ``Sum``, ``Product``, ``Average`` - Basic mathematical operations
- ``WeightedAverage`` - Domain proportion weighting
- ``Scale``, ``Normalize`` - Data transformations
- ``CategoryFromThresholds`` - Threshold-based classification

**Machine Learning:**

- Convert scikit-learn decision trees to calculations
- Convert random forests to calculation ensembles
- Convert linear models to equations
- Full support for both regression and classification

**Advanced Features:**

- Topological sorting for dependency resolution
- Dependency analysis and visualization
- Interactive display in Jupyter notebooks
- Calculation validation and testing

Where to Start
~~~~~~~~~~~~~~

- **New users**: Start with :doc:`getting_started` for installation and basic usage
- **Learning the syntax**: See :doc:`expression_syntax` for Leapfrog expression syntax
- **Building workflows**: Check :doc:`workflow_patterns` for common use cases
- **Using helpers**: Read :doc:`helpers_guide` for helper function details
- **Best practices**: Review :doc:`best_practices` before production use
- **Step-by-step guides**: Follow :doc:`tutorials` for complete examples
- **API details**: Consult :doc:`api_reference` for technical reference

Legal Notice
~~~~~~~~~~~~

Pollywog is an independent open-source tool developed to support automation of workflows involving .lfcalc files used in Leapfrog software by Seequent. This tool is not affiliated with, endorsed by, or sponsored by Seequent. Users should review Leapfrog's terms of use before integrating pollywog into their workflows.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
