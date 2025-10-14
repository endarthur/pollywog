# Automating Leapfrog Workflows with Pollywog – An Independent Open-Source Tool

[![DOI-badge]][DOI] [![docs-badge]][docs] [![lite-badge]][lite]

[DOI-badge]: https://zenodo.org/badge/1071742254.svg
[DOI]: https://doi.org/10.5281/zenodo.173138
[docs-badge]: https://readthedocs.org/projects/pollywog/badge/?version=latest
[docs]: https://pollywog.readthedocs.io/en/latest/?
[lite-badge]: https://jupyterlite.rtfd.io/en/latest/_static/badge.svg
[lite]: https://endarthur.github.io/pollyweb


Professionals using Seequent solutions for geological modeling and resource estimation often work with .lfcalc files. These files can be repetitive to manage and prone to manual errors. This is especially true when dealing with conditional logic, domain-based dilution calculations, or predictive model integration.

Pollywog was developed to support this technical audience. It is a Python package that enables:

- Programmatic reading and writing of .lfcalc files, making calculations more standardized and reproducible
- Automation of complex workflows, including conditional equations and post-processing of results
- Integration with machine learning models via scikit-learn, allowing classifiers or regressions to be applied directly within Leapfrog calculations
- Creation of reusable scripts, which can be versioned and audited, providing greater control over modeling processes

Pollywog aims to reduce time spent on manual tasks, minimize input errors, and increase efficiency in geological modeling.

The documentation includes practical examples and tutorials to help technical teams get started quickly.

If you work with Leapfrog and are looking to optimize your workflows, Pollywog is worth exploring.

Pollywog is still very much a work in progress, so take care in its use and make sure to not have anything important open and not saved in Leapfrog while testing it out. Also, please report any issues you encounter. Suggestions and contributions are very welcome!

## Legal Disclaimer

Pollywog is an independent open-source tool developed to support the automation of workflows involving .lfcalc files used in Leapfrog software by Seequent.
This tool does not perform reverse engineering, does not modify Leapfrog, and does not access its source code or proprietary libraries. Pollywog operates exclusively on user-generated files and is designed to complement Leapfrog through external automation.

Important:
- Pollywog is not affiliated with, endorsed by, or sponsored by Seequent or any company associated with Leapfrog
- Use of this tool does not violate Leapfrog’s license terms or Seequent’s policies
- Users are encouraged to review Leapfrog’s terms of use before integrating Pollywog into commercial or corporate environments
- The author is not responsible for any misuse of the tool that may breach Seequent’s licensing terms


## Installation

Install from pypi:

```bash
pip install lf_pollywog
```

Or install the latest development version from GitHub:

```bash
pip install git+https://github.com/endarthur/pollywog.git
```

### JupyterLite

You can also try Pollywog in your browser without any installation using JupyterLite: https://endarthur.github.io/pollyweb

Please be aware that JupyterLite has some limitations, such as restricted file system access and limited support for certain libraries. It also saves files in the browser's memory, which may not persist across sessions, and will be deleted if you clear your browser's cache. For full functionality and to avoid losing work, it is recommended to install Pollywog in a local Python environment.

Having said that, if you take care to download your notebooks and lfcalc files from time to time, JupyterLite can be a convenient way to experiment with Pollywog without any installation. Check the quickstart notebook in the JupyterLite environment for a brief introduction and some helper functions to automatically download lfcalc files you export.

## Usage

Pollywog makes it easy to automate Leapfrog calculation workflows. Here are some common use cases:

### Reading and Writing `.lfcalc` files

Read existing calculation files, modify them, and write them back:

```python
import pollywog as pw

# Read existing file
calcset = pw.CalcSet.read_lfcalc("path/to/file.lfcalc")

# Modify or add calculations
from pollywog.core import Number
calcset.items.append(Number(name="new_calc", children=["[Au] * 2"]))

# Export modified version
calcset.to_lfcalc("output.lfcalc")
```

### Creating a Simple Calculation Set

Build calculation sets programmatically with clear, version-controlled code:

```python
from pollywog.core import Number, CalcSet

# Create calculations for drillhole preprocessing
calcset = CalcSet([
    Number(name="Au_clean", children=["clamp([Au], 0)"],
           comment_equation="Remove negative values"),
    Number(name="Au_log", children=["log([Au_clean] + 1e-6)"],
           comment_equation="Log transform for kriging"),
])

calcset.to_lfcalc("drillhole_preprocessing.lfcalc")
```

### Using Helper Functions

Simplify common patterns with helper functions:

```python
from pollywog.helpers import WeightedAverage, Sum, CategoryFromThresholds
from pollywog.core import CalcSet

# Domain-weighted grades
calcset = CalcSet([
    WeightedAverage(
        variables=["Au_oxide", "Au_sulfide", "Au_transition"],
        weights=["prop_oxide", "prop_sulfide", "prop_transition"],
        name="Au_composite",
        comment="Domain-weighted gold grade"
    ),
    
    Sum("Au", "Ag", "Cu", name="total_metals"),
    
    CategoryFromThresholds(
        variable="Au_composite",
        thresholds=[0.5, 2.0],
        categories=["low", "medium", "high"],
        name="grade_class"
    ),
])

calcset.to_lfcalc("resource_model.lfcalc")
```

### Converting a scikit-learn model

Deploy machine learning models directly in Leapfrog calculations:

```python
from pollywog.conversion.sklearn import convert_tree, convert_forest
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from pollywog.core import CalcSet
import numpy as np

# Example: Predict metallurgical recovery from grade and mineralogy
X = np.array([
    [1.2, 0.3, 75],  # Au grade, Cu grade, grind size (P80)
    [0.8, 0.5, 100],
    [2.0, 0.2, 75],
])
y = np.array([0.88, 0.82, 0.91])  # Recovery values

# Train decision tree
tree_model = DecisionTreeRegressor(max_depth=3, random_state=42)
tree_model.fit(X, y)

# Convert to Leapfrog calculation
feature_names = ["Au_composite", "Cu_composite", "P80"]
recovery_calc = convert_tree(tree_model, feature_names, "Au_recovery_predicted")

# Export to .lfcalc file
CalcSet([recovery_calc]).to_lfcalc("ml_recovery_model.lfcalc")

# Or use random forest for ensemble predictions
rf_model = RandomForestRegressor(n_estimators=5, max_depth=3, random_state=42)
rf_model.fit(X, y)
rf_calc = convert_forest(rf_model, feature_names, "Au_recovery_rf")
CalcSet([rf_calc]).to_lfcalc("rf_recovery_model.lfcalc")
```

### Domain-Based Calculations

Handle multi-domain resource estimation with ease:

```python
from pollywog.core import CalcSet, Number, If
from pollywog.helpers import WeightedAverage

domains = ["oxide", "transition", "sulfide"]
metals = ["Au", "Ag", "Cu"]

# Create weighted averages for all metals across all domains
domain_calcs = CalcSet([
    WeightedAverage(
        variables=[f"{metal}_{domain}" for domain in domains],
        weights=[f"prop_{domain}" for domain in domains],
        name=f"{metal}_composite",
        comment=f"Domain-weighted {metal} grade"
    )
    for metal in metals
])

# Apply domain-specific recovery factors
recovery_calcs = CalcSet([
    Number(name="Au_recovered", children=[
        If([
            ("[domain] = 'oxide'", "[Au_composite] * 0.92"),
            ("[domain] = 'transition'", "[Au_composite] * 0.85"),
            ("[domain] = 'sulfide'", "[Au_composite] * 0.78"),
        ], otherwise=["[Au_composite] * 0.75"])
    ], comment_equation="Domain-specific Au recovery"),
])

# Combine and export
combined = CalcSet(domain_calcs.items + recovery_calcs.items)
combined.to_lfcalc("multi_domain_workflow.lfcalc")
```

For more advanced workflows and complete tutorials, see the [documentation](https://pollywog.readthedocs.io/en/latest/).

## Querying CalcSets

Pollywog provides a powerful query method for filtering items in a `CalcSet`, inspired by pandas' DataFrame.query. You can use Python-like expressions to select items based on their attributes and external variables.

### Syntax
- Use item attributes (e.g., `name`, `item_type`) in expressions.
- Reference external variables using `@var` syntax (e.g., `name.startswith(@prefix)`).
- Supported helpers: `len`, `any`, `all`, `min`, `max`, `sorted`, `re`, `str`.

### Examples

```python
# Select items whose name starts with 'Au'
calcset.query('name.startswith("Au")')

# Select items whose name starts with an external variable 'prefix'
prefix = "Ag"
calcset.query('name.startswith(@prefix)')

# Select items with more than one child
calcset.query('len(children) > 1')

# Use regular expressions
calcset.query('re.match(r"^A", name)')
```

### Notes
- External variables (`@var`) are resolved from the caller's scope or passed as keyword arguments.
- Only items matching the query expression are returned in the new `CalcSet`.

## License

MIT License

<!-- ## Authors

See `AUTHORS` file or repository contributors. -->

## Contributions

Contributions are very welcome!
If you'd like to collaborate on Pollywog, whether through bug fixes, feature enhancements, new use cases, or documentation, please follow these steps:

- Fork the repository
- Create a feature branch (git checkout -b feature-name)
- Make your changes and commit (git commit -m 'Add new feature')
- Submit a pull request with a clear explanation of your changes

Before contributing, please:
- Ensure your changes align with the project’s goals
- Maintain consistent code style
- Test your modifications whenever possible

Feel free to open an issue if you have questions or suggestions.

## Acknowledgements

Thanks to Debora Roldão for helping with organization of the project, documentation and design, Eduardo Takafuji for the initial discussion of the feasability of this all those years ago and Jessica da Matta for support and sanity checks along the way.
