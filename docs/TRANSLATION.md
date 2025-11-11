# Translation Guide

This document explains how to contribute translations to pollywog's documentation.

## Overview

Pollywog uses **sphinx-intl** with gettext for internationalization (i18n). This allows the documentation to be translated into multiple languages while maintaining a single source of truth in English.

Currently supported languages:
- English (en) - Default (complete)
- Brazilian Portuguese (pt_BR) - In progress (~80% complete)
  - ✅ index.po - Complete
  - ✅ geologist_tutorial.po - Complete
  - ⏳ Other pages - Available for translation

## Translation Workflow

### For Translators

If you want to contribute translations, follow these steps:

#### 1. Setup your environment

```bash
# Install dev dependencies (includes sphinx-intl)
pip install -e ".[dev]"

# Install sphinx dependencies
pip install -r docs/requirements.txt
```

#### 2. Update translation files (if needed)

If the English documentation has been updated since the last translation:

```bash
cd docs

# Extract latest translatable strings
sphinx-build -M gettext . _build

# Update .po files for your language
sphinx-intl update -p _build/gettext -l pt_BR
```

#### 3. Translate the .po files

Open the `.po` files in `docs/locale/pt_BR/LC_MESSAGES/` and translate the strings:

```po
#: ../../index.rst:3
msgid "Welcome to pollywog's documentation!"
msgstr "Bem-vindo à documentação do pollywog!"

#: ../../index.rst:5
msgid "Getting Started"
msgstr "Primeiros Passos"
```

**Translation tools:**
- **Manual editing**: Use any text editor
- **Poedit**: GUI tool for editing .po files (https://poedit.net/)
- **Lokalize**: KDE translation tool
- **Online platforms**: Consider Weblate, Transifex, or Crowdin for collaborative translation

#### 4. Build and preview translated docs

```bash
cd docs

# Build Portuguese documentation
sphinx-build -b html -D language=pt_BR . _build/html-pt_BR

# Or use the Makefile target (Linux/macOS with make)
make html-i18n LANG=pt_BR

# Open in browser
# Windows: start _build/html-pt_BR/index.html
# Linux: xdg-open _build/html-pt_BR/index.html
# macOS: open _build/html-pt_BR/index.html
```

#### 5. Submit your translation

1. Fork the repository
2. Create a branch: `git checkout -b translate-pt-br`
3. Commit your .po files: `git add docs/locale/pt_BR/`
4. Push and create a Pull Request

**Important:** Only commit `.po` files, not `.mo` files (compiled translations).

## File Structure

```
docs/
├── source/              # English documentation source
│   ├── index.rst
│   ├── getting_started.rst
│   └── ...
├── locale/              # Translations
│   └── pt_BR/
│       └── LC_MESSAGES/
│           ├── index.po           # Translation for index.rst
│           ├── getting_started.po # Translation for getting_started.rst
│           └── ...
├── _build/
│   ├── gettext/         # Extracted message catalogs (.pot files)
│   ├── html/            # English build
│   └── html-pt_BR/      # Portuguese build
├── conf.py              # Sphinx configuration
└── Makefile             # Build commands
```

## Translation Format (.po files)

Each `.po` file contains translation units like this:

```po
# Comment indicating source location
#: ../../getting_started.rst:10
msgid "Original English text"
msgstr "Texto traduzido em português"
```

- `msgid`: Original English string (DO NOT CHANGE)
- `msgstr`: Your translation (EDIT THIS)
- Comments (`#:`) show where the string appears in the source

## Best Practices

### 1. Preserve formatting

Keep ReStructuredText markup intact:

```po
msgid "**Bold text** and *italic text*"
msgstr "**Texto em negrito** e *texto em itálico*"
```

### 2. Keep code examples in English

Don't translate code, variable names, or function names:

```po
msgid "Use ``CalcSet()`` to create a calculation set"
msgstr "Use ``CalcSet()`` para criar um conjunto de cálculos"
#       ↑ Code stays in English ↑
```

### 3. Preserve links and references

Keep Sphinx cross-references untranslated:

```po
msgid "See :doc:`getting_started` for details"
msgstr "Veja :doc:`getting_started` para detalhes"
#       ↑ Reference stays the same ↑
```

### 4. Use natural language

Translate the meaning, not word-for-word:

```po
# ✗ Literal translation (awkward)
msgid "Getting started is easy"
msgstr "Ficando começado é fácil"

# ✓ Natural translation
msgid "Getting started is easy"
msgstr "Começar é fácil"
```

### 5. Be consistent with terminology

Create a glossary for technical terms:

| English | Portuguese (pt_BR) |
|---------|-------------------|
| calculation set | conjunto de cálculos |
| helper function | função auxiliar |
| workflow | fluxo de trabalho |
| decompilation | descompilação |

## For Maintainers

### Adding a new language

```bash
cd docs

# Extract messages
sphinx-build -M gettext . _build

# Initialize new language (e.g., Spanish)
sphinx-intl update -p _build/gettext -l es

# Add to ReadTheDocs configuration
# Edit .readthedocs.yml to include new language
```

### Updating translations after docs changes

```bash
cd docs

# Extract new strings
sphinx-build -M gettext . _build

# Update all languages
sphinx-intl update -p _build/gettext

# Or update specific language
sphinx-intl update -p _build/gettext -l pt_BR
```

### Building all languages

```bash
cd docs

# English (default)
sphinx-build -b html . _build/html

# Portuguese
sphinx-build -b html -D language=pt_BR . _build/html-pt_BR

# Spanish (if added)
sphinx-build -b html -D language=es . _build/html-es
```

## ReadTheDocs Integration

To host multi-language documentation on ReadTheDocs:

### Option 1: Separate Projects (Recommended)

1. Create main project: `pollywog` (English)
2. Create translation projects: `pollywog-pt-br`, `pollywog-es`, etc.
3. In ReadTheDocs settings:
   - Main project → Admin → Translations → Add `pollywog-pt-br`
   - Translation project → Admin → Advanced → Language = `pt_BR`

This creates a language switcher in the docs.

### Option 2: Single Project with Subprojects

Configure `.readthedocs.yml`:

```yaml
# .readthedocs.yml
version: 2

sphinx:
  configuration: docs/conf.py

formats:
  - pdf
  - epub

# Build multiple languages
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
  jobs:
    post_build:
      - sphinx-build -b html -D language=pt_BR docs docs/_build/html-pt_BR
```

## Translation Statistics

Track progress with `msgfmt`:

```bash
# Check translation completeness
msgfmt --statistics docs/locale/pt_BR/LC_MESSAGES/index.po

# Output example:
# 45 translated, 12 fuzzy, 8 untranslated messages.
```

## Resources

- **Sphinx i18n**: https://www.sphinx-doc.org/en/master/usage/advanced/intl.html
- **sphinx-intl**: https://sphinx-intl.readthedocs.io/
- **gettext**: https://www.gnu.org/software/gettext/manual/gettext.html
- **Poedit**: https://poedit.net/
- **ReadTheDocs i18n**: https://docs.readthedocs.io/en/stable/localization.html

## Questions?

If you have questions about translation, please:
1. Check existing issues: https://github.com/endarthur/pollywog/issues
2. Open a discussion: https://github.com/endarthur/pollywog/discussions
3. Ask in the Pull Request when submitting translations

Thank you for contributing translations! 🌍
