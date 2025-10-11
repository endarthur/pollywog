
Welcome to pollywog's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents

   api_reference
   tutorials

Introduction
------------

pollywog is a Python library designed to make it easy to build, manipulate, and visually inspect Leapfrog-style calculation sets—especially when those sets are large, complex, or involve repetitive logic.

### Problems pollywog solves

- **Building large calculation sets:** Writing and maintaining hundreds of calculations by hand in Leapfrog can be error-prone and tedious. pollywog lets you generate, organize, and refactor these sets programmatically in Python.
- **Complicated logic:** Many workflows require conditional logic, grouping, and dependencies between variables. pollywog provides constructs like `If` blocks, `Category` grouping, and dependency analysis to help you manage complexity.
- **Repetitive tasks:** When you need to apply similar logic to many variables (e.g., clamping, scaling, filtering), pollywog enables you to automate these patterns with Python code, reducing manual effort and mistakes.
- **Visual inspection:** pollywog can render calculation sets as rich HTML trees in Jupyter, making it easy to review and debug logic before exporting to Leapfrog.

By using pollywog, you can:
- Automate the creation and modification of calculation sets
- Refactor and query calculations with code
- Export directly to Leapfrog `.lfcalc` format
- Visualize and validate logic interactively

See the API Reference for details on all classes and functions.

