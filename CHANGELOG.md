# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2025-11-11

### Added
- **Decompilation Module** (`pollywog/decomp.py`) - Convert .lfcalc files back to Python code
  - `decompile()` - Read .lfcalc file and generate Python code
  - `decompile_to_string()` - Convert CalcSet to Python code string
  - Phase 1: Direct conversion (exact structure recreation)
  - Phase 2: Pattern detection (automatic helper recognition)
- **Pattern Detection** (`pollywog/patterns.py`) - Smart recognition of common calculation patterns
  - WeightedAverage pattern detection
  - Sum pattern detection
  - Product pattern detection
  - Average pattern detection
  - Confidence scoring (>90% threshold)
  - Graceful fallback to direct code
- **Jupyter Magic Command** - `%pw.load` for interactive .lfcalc loading
  - Behaves like built-in `%load` command
  - First run: decompiles and replaces cell content
  - Second run: executes loaded Python code
  - Integrated with pattern detection
- Examples and documentation for decompilation workflows
  - `examples/decompile_example.py` - Comprehensive usage examples
  - `examples/pw_load_magic_demo.ipynb` - Jupyter magic demonstration

### Changed
- Decompilation now automatically detects and uses helper functions (WeightedAverage, Sum, Product, Average)
- Generated Python code imports helpers when patterns are detected
- Enhanced CLAUDE.md with decompilation architecture details

### Testing
- Added 28 new tests (21 pattern detection + 7 integration tests)
- All 146 tests passing
- Roundtrip validation: .lfcalc → Python → exec → CalcSet → .lfcalc

## [0.2.0] - 2025-11-10

### Added
- Automated notebook execution testing infrastructure (`test_notebooks.py`)
- `__version__` attribute accessible from package root (`import pollywog; pollywog.__version__`)
- Dynamic version management using `importlib.metadata` (single source of truth in `pyproject.toml`)
- `__all__` export list in `__init__.py` for explicit public API
- Added `pytest-cov` to dev dependencies for code coverage support
- Enhanced PyPI metadata with keywords and classifiers for better discoverability
- Additional project URLs (Documentation, Repository, Issues, Changelog, Try Online)

### Fixed
- Fixed `convert_tree()` parameter names in example notebooks (`input_names`/`output_name` → `feature_names`/`target_name`)
- Corrected `Normalize()` helper usage in notebooks (min-max scaling to [0,1], not sum-to-1 normalization)
- Updated `Normalize()` documentation to accurately describe min-max scaling behavior
- Made matplotlib visualization optional in `basic_usage.ipynb` for environments without plotting libraries

### Changed
- Updated version to 0.2.0 (PEP 440 compliant)
- Added `.claude/` directory to `.gitignore` for cleaner repository
- Added `nbconvert>=7.0` and `ipykernel` to dev dependencies for notebook testing

### Infrastructure
- Added automated PyPI publishing workflow (GitHub Actions with trusted publishing)
- Added automated pollyweb sync workflow for example notebooks
- Removed `.claude/settings.local.json` from version control

### Testing
- All 110 tests passing (99 existing + 11 new notebook tests)
- 10/10 example notebooks execute successfully without errors
- Comprehensive test coverage across core, helpers, conversion, and integration modules

## [0.1.2] - 2025-10-20

### Added
- Comprehensive documentation overhaul with tutorials and examples
- Rich Jupyter notebook display with interactive calculation trees
- Helper functions for common patterns (Sum, Product, Average, WeightedAverage, etc.)
- Dual-mode helpers (with/without `name` parameter)
- Query functionality for CalcSet with pandas-like syntax
- Topological sorting for dependency resolution

### Changed
- Improved API consistency across core classes
- Enhanced error messages and validation

## [0.1.1] - 2025-10-15

### Added
- Basic sklearn model conversion support
- Initial documentation structure

### Fixed
- Various bug fixes and improvements

## [0.1.0] - 2025-10-07

### Added
- Initial release
- Core functionality for reading/writing `.lfcalc` files
- Basic calculation classes (Number, Category, Variable, Filter, If, IfRow)
- CalcSet container for managing calculations
- Basic serialization/deserialization support

[Unreleased]: https://github.com/endarthur/pollywog/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/endarthur/pollywog/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/endarthur/pollywog/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/endarthur/pollywog/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/endarthur/pollywog/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/endarthur/pollywog/releases/tag/v0.1.0
