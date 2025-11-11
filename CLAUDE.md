# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Pollywog** is a Python library for programmatically building, manipulating, and automating Leapfrog calculation sets (`.lfcalc` files). It provides a way to define geological modeling calculations in version-controlled Python code instead of manual point-and-click operations in Leapfrog software.

Key capabilities:
- Read/write `.lfcalc` files (compressed JSON with custom binary header)
- Create calculations with Python classes (Number, Category, Variable, If, Filter)
- Query and filter calculation sets with pandas-like syntax
- Convert scikit-learn models (decision trees, random forests, linear models) to Leapfrog calculations
- Rich Jupyter notebook display with interactive calculation trees
- Helper functions for common operations (Sum, WeightedAverage, Product, etc.)

## Development Commands

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run specific test function
pytest tests/test_core.py::test_query_with_external_variable

# Run with verbose output
pytest -v
```

### Building Package
```bash
# Install in development mode
pip install -e .

# Install with optional dependencies
pip install -e ".[conversion]"  # For scikit-learn conversion
pip install -e ".[dev]"         # For development (includes pytest, pandas)
```

### Documentation
```bash
# Build Sphinx documentation
cd docs
make html

# View built docs (Windows)
start _build/html/index.html
```

## Code Architecture

### Core Module (`pollywog/core.py`)

The foundation of the library with two main concepts:

1. **CalcSet**: Container for calculation workflows
   - `items`: List of calculation items
   - `query()`: Filter items with pandas-like expressions using `@var` syntax
   - `topological_sort()`: Resolve dependencies and sort items
   - `read_lfcalc()` / `to_lfcalc()`: I/O for `.lfcalc` files
   - `.lfcalc` format: Binary header (`HEADER` constant) + compressed JSON

2. **Item Classes**: Calculation building blocks
   - `Variable`: Simple variable reference
   - `Number`: Numeric calculation with expression(s)
   - `Category`: Categorical calculation
   - `Filter`: Data filtering
   - `If` / `IfRow`: Conditional logic (nested vs flat structures)

   All items have:
   - `name`: Identifier
   - `expression`: Calculation formula(s) as list of strings
   - `dependencies`: Auto-extracted from `[variable_name]` references in expressions
   - `to_dict()` / `from_dict()`: Serialization

### Helpers Module (`pollywog/helpers.py`)

Helper functions with **dual-mode operation**:
- **With `name` parameter**: Returns complete Item object (Number/Category)
- **Without `name` parameter**: Returns expression string for composition

Key helpers:
- `Sum`, `Product`, `Average`: Basic aggregations
- `WeightedAverage`, `WeightedSum`: Domain-weighted calculations
- `Normalize`, `Scale`: Data transformations
- `CategoryFromThresholds`: Classification from numeric thresholds

All helpers use `ensure_variables()` to wrap variable names in brackets (`[var]`) and handle function calls via `ignore_functions` parameter.

### Conversion Module (`pollywog/conversion/sklearn.py`)

Converts scikit-learn models to Leapfrog calculations:
- `convert_tree()`: DecisionTreeRegressor/Classifier → Number/Category with nested If structures
- `convert_forest()`: RandomForestRegressor/Classifier → averaged ensemble calculations
- `convert_linear_model()`: LinearRegression/LogisticRegression → weighted sum formulas

The `flat` parameter controls whether If structures are nested (default) or flattened into a single condition list.

### Decompilation Module (`pollywog/decomp.py`)

**New in 0.3.0** - Converts .lfcalc files back to Python code:
- `decompile()`: Read .lfcalc file and generate Python code that recreates it
- `decompile_to_string()`: Convert a CalcSet to Python code string

**Phase 1 Implementation**: Direct conversion with no pattern detection. Generates valid Python code that exactly recreates the calculation set structure using pollywog classes (Number, Category, If, etc.).

**Use cases**:
- Migration path: Convert existing .lfcalc files to version-controlled Python code
- Learning tool: See how to write complex calculations in pollywog
- Refactoring aid: Get a pollywog starting point to manually optimize
- Enables git-based workflows for legacy calculation sets

**Future phases** (not yet implemented):
- Phase 2: Pattern detection (WeightedAverage, Sum, etc.)
- Phase 3: Variable family detection (domain-based loops)

### Display Module (`pollywog/display.py`)

Jupyter notebook integration:
- `display_calcset()`: Renders calculation trees with HTML/SVG
- `display_item()`: Renders individual items
- `set_theme()`: Global theme switching ("light"/"dark")
- Color-coded syntax for variables, functions, and references

### Utility Modules

- `utils.py`: Helper utilities (`ensure_list`, `ensure_brackets`, `to_dict`, etc.)
- `magics.py`: Jupyter magic commands for interactive workflows
  - `%pollywog autodownload on/off/status` - Auto-display download buttons in JupyterLite
  - `%pw.load file.lfcalc` - Load and decompile .lfcalc file into current cell (works like `%load`)
- `leapfrog_env.py`: Leapfrog environment variable handling
- `jupyterlite_utils.py`: Browser-based JupyterLite support (https://endarthur.github.io/pollyweb)

## Key Design Patterns

### Expression Syntax
All Leapfrog expressions use bracket notation for variables: `[variable_name]`
- Functions: `max([Au], [Ag])`, `clamp([grade], 0)`
- Operations: `[Au] * 0.95 + [Ag] * 0.85`
- Conditionals: In If structures with condition-expression tuples

### Dependency Resolution
Variables referenced in expressions (anything in `[brackets]`) are automatically extracted as dependencies. The `topological_sort()` method uses this to order calculations correctly.

### Helper Composition Pattern
Helpers can be nested without `name` to build complex expressions:
```python
Number("NSR",
    f"{Product(['grade', 'recovery', 'price'])} + {Product(['byproduct', 'recovery2', 'price2'])}"
)
```

### File Format
`.lfcalc` files structure:
1. Binary header (32 bytes, stored in `HEADER` constant)
2. zlib-compressed JSON payload with structure:
   - `type`: "calculation-set"
   - `items`: Sorted list (variables → calculations → filters)

## Testing Guidelines

- Test files mirror source structure: `tests/test_core.py` for `pollywog/core.py`
- `conftest.py`: Adds parent directory to Python path for imports
- Tests use pytest fixtures and parametrization
- Key test areas:
  - I/O roundtrip (read → modify → write → read)
  - Query expressions with `@external_vars`
  - Topological sorting with cyclic dependency detection
  - Helper dual-mode behavior (with/without `name`)
  - ML model conversion accuracy
  - Decompilation roundtrip (.lfcalc → Python → exec → CalcSet → .lfcalc)

## Important Implementation Notes

- **Item Sorting**: When writing `.lfcalc`, items are sorted by type (variables, calculations, filters) via `ITEM_ORDER` dict
- **Query Safety**: The `query()` method uses restricted `eval()` with `SAFE_EVAL_HELPERS` (len, any, all, min, max, sorted, re, str)
- **Bracket Wrapping**: Helper functions auto-wrap variable names in brackets unless `ignore_functions=True` and the string looks like a function call
- **Cyclic Dependencies**: `topological_sort()` detects cycles using temporary marks during depth-first traversal
- **Optional Dependencies**: scikit-learn is optional (only required for `conversion` subpackage)

## Documentation

Full documentation at https://pollywog.readthedocs.io:
- Expression syntax reference (Leapfrog-specific functions and operators)
- Workflow patterns (domain-based modeling, ML integration)
- Helper function guide (detailed examples of dual-mode usage)
- Best practices (naming conventions, testing, performance)

## Package Metadata

- Package name on PyPI: `lf_pollywog`
- License: MIT
- Python compatibility: >=3.7
- Main dependencies: None (stdlib only for core functionality)
- Optional dependencies: scikit-learn (conversion), pytest/pandas (dev)
