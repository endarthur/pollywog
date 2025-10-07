# pollywog

**pollywog** is a Python library for working with Leapfrog calculation sets, including reading, writing, and manipulating `.lfcalc` files.
It provides a much needed layer of automation for creating and managing complex calculation workflows in Leapfrog.

Pollywog is still very much a work in progress, so take care in its use and make sure to not have anything important open and not saved in Leapfrog while testing it out. Also, please report any issues you encounter. Suggestions and contributions are very welcome!

## Features

- Read and write Leapfrog `.lfcalc` files.
- Manipulate calculation sets, variables, calculations, filters, and conditional logic.
- Convert scikit-learn models (decision trees, linear models) to Leapfrog calculation format.


## Installation

Install from pypi (not available yet, but soon):

```bash
pip install lf_pollywog
```

Or install the latest development version from GitHub:

```bash
pip install git+https://github.com/endarthur/pollywog.git
```

## Usage

### Reading and Writing `.lfcalc` files

```python
import pollywog as pw
calcset = pw.CalcSet.read_lfcalc("path/to/file.lfcalc")
calcset.to_lfcalc("output.lfcalc")
```

### Creating a Simple Calculation Set

```python
from pollywog.core import Number, CalcSet
calcset = CalcSet([
    Number(name="Au_final", children=["clamp([Au_est], 0)"]),
    Number(name="Ag_final", children=["clamp([Ag_est], 0)"])
])
calcset.to_lfcalc("postprocessed.lfcalc")
```

### Converting a scikit-learn model

Currently supports decision trees (both classification and regression) and linear models:

```python
from pollywog.conversion.sklearn import convert_tree
from sklearn.tree import DecisionTreeRegressor
import numpy as np
X = np.array([[0.2, 1.0, 10], [0.5, 2.0, 20]])
y = np.array([0.7, 0.8])
feature_names = ["Cu_final", "Au_final", "Ag_final"]
reg = DecisionTreeRegressor(max_depth=2)
reg.fit(X, y)
recovery_calc = convert_tree(reg, feature_names, "recovery_ml")
CalcSet([recovery_calc]).to_lfcalc("recovery_ml.lfcalc")
```

For more advanced workflows (domain dilution, conditional logic, economic value, combining CalcSets, etc.), see the Jupyter notebooks in the `examples/` folder of this repository.

## File Structure

- `core.py`: Main classes for calculation sets and items.
- `conversion/sklearn.py`: Conversion utilities for scikit-learn models.
- `utils.py`: Helper functions.

## License

MIT License

<!-- ## Authors

See `AUTHORS` file or repository contributors. -->