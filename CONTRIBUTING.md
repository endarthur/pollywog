# Contributing to Pollywog

Thank you for your interest in contributing to Pollywog! This document provides guidelines and instructions for contributing.

## How to Contribute

Contributions are very welcome! Whether you're fixing bugs, adding features, improving documentation, or sharing use cases, your help is appreciated.

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/pollywog.git
   cd pollywog
   ```
3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```
4. **Set up pre-commit hooks** (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature-name
   ```

2. **Make your changes**:
   - Write clear, readable code
   - Add tests for new functionality
   - Update documentation as needed
   - Follow the existing code style

3. **Run tests locally**:
   ```bash
   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=pollywog

   # Run specific tests
   pytest tests/test_core.py::test_specific_function
   ```

4. **Format your code** (if not using pre-commit hooks):
   ```bash
   black pollywog/ tests/
   ruff --fix pollywog/ tests/
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Clear description of changes"
   ```

   Good commit messages:
   - Start with a verb (Add, Fix, Update, Remove, etc.)
   - Be concise but descriptive
   - Reference issues if applicable (#123)

6. **Push to your fork**:
   ```bash
   git push origin feature-name
   ```

7. **Submit a pull request** on GitHub with:
   - Clear description of changes
   - Reference to related issues
   - Examples or screenshots if applicable

## Code Style Guidelines

- **Python version**: Support Python 3.7+
- **Formatting**: Use `black` (88 character line length)
- **Linting**: Follow `ruff` recommendations
- **Imports**: Organize with `isort` (handled by ruff)
- **Type hints**: Encouraged but not required (yet)
- **Docstrings**: Use Google-style docstrings for public APIs

### Example Code Style

```python
def example_function(variable: str, threshold: float = 0.5) -> Number:
    """Create an example calculation.

    Args:
        variable: Variable name to process.
        threshold: Cutoff threshold value. Defaults to 0.5.

    Returns:
        Number: A Number calculation object.

    Example:
        >>> calc = example_function("Au", threshold=1.0)
        >>> calc.name
        'Au_processed'
    """
    return Number(f"{variable}_processed", f"clamp([{variable}], {threshold})")
```

## Testing Guidelines

- **Write tests** for all new features and bug fixes
- **Run tests** before submitting PRs
- **Test coverage**: Aim for >80% coverage on new code
- **Test files**: Mirror source structure (`test_core.py` for `core.py`)

### Test Structure

```python
def test_feature_name():
    """Test that feature does X correctly."""
    # Arrange
    input_data = CalcSet([...])

    # Act
    result = input_data.some_method()

    # Assert
    assert result.name == "expected_name"
    assert len(result.items) == 2
```

## Documentation

- Update documentation for new features
- Include examples in docstrings
- Add entries to CHANGELOG.md under [Unreleased]
- Update README.md if adding major features

### Documentation Locations

- **API docs**: Docstrings in source code
- **Tutorials**: `docs/` directory
- **Examples**: `examples/` directory (Jupyter notebooks)
- **CHANGELOG**: `CHANGELOG.md`

## Pre-commit Hooks

Pre-commit hooks automatically check your code before commits. They:
- Format code with `black`
- Lint with `ruff`
- Check for common issues (trailing whitespace, merge conflicts, etc.)
- Strip outputs from test notebooks (keeps git clean)

### Install hooks:
```bash
pip install pre-commit
pre-commit install
```

### Run manually:
```bash
pre-commit run --all-files
```

### Skip hooks (not recommended):
```bash
git commit --no-verify
```

## Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style (black + ruff)
- [ ] All tests pass (`pytest`)
- [ ] New code has tests
- [ ] Documentation updated
- [ ] CHANGELOG.md updated under [Unreleased]
- [ ] Commit messages are clear
- [ ] PR description explains changes

## LLM-Assisted Contributions

**It's okay to use LLMs** (ChatGPT, Claude, Copilot, etc.) to help write code or documentation! However:

- ✅ **Review all code** - Understand what you're submitting
- ✅ **Test thoroughly** - LLMs can make mistakes
- ✅ **Verify accuracy** - Especially for domain-specific code
- ✅ **Be transparent** - Mention LLM use if it helps explain issues

## Questions?

- **Issues**: Open an [issue](https://github.com/endarthur/pollywog/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact Arthur Endlein at endarthur@gmail.com

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to endarthur@gmail.com.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Pollywog! 🎉
