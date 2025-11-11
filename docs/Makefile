# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile gettext update-locale html-i18n

# Internationalization targets
gettext:
	@$(SPHINXBUILD) -M gettext "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/gettext."

# Update or create translation files for a specific language
# Usage: make update-locale LANG=pt_BR
update-locale:
	sphinx-intl update -p $(BUILDDIR)/gettext -l $(LANG)

# Build HTML documentation for a specific language
# Usage: make html-i18n LANG=pt_BR
html-i18n:
	@$(SPHINXBUILD) -b html -D language=$(LANG) "$(SOURCEDIR)" "$(BUILDDIR)/html-$(LANG)" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages for language $(LANG) are in $(BUILDDIR)/html-$(LANG)."

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
