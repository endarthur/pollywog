Tutorial for Resource Geologists
=================================

Welcome! This tutorial is specifically designed for resource geologists who are comfortable with Leapfrog and its calculator but are new to programming with Python. If you've built calculations in Leapfrog using the calculator interface, you already have the conceptual foundation to use Pollywog—we'll just show you how to express those same ideas in Python code.

.. note::
   This tutorial assumes you already know how to use Leapfrog and its calculator. If you can create formulas in Leapfrog's calculator dialog (like ``[Au] * 2`` or ``if([Au] > 0.5, "ore", "waste")``), you're ready to learn Pollywog!

Why Learn Pollywog?
-------------------

You might be wondering: "I can already create calculations in Leapfrog—why learn Python?"

Here's why Pollywog is worth your time:

**Time Savings**
   - Creating 100 calculations manually in Leapfrog: **2-3 hours**
   - Creating the same 100 calculations with Pollywog: **5 minutes**
   - Once you learn the basics, you'll save hours on every project

**Consistency**
   - Manual work: Easy to make typos or miss a domain
   - Pollywog: If one calculation is right, all 100 are right

**Reusability**
   - Manual work: Start from scratch for each project
   - Pollywog: Reuse your scripts across multiple projects

**Documentation**
   - Manual work: Hard to explain what you did
   - Pollywog: Your Python code is the documentation

Quick Start: Your First Calculation in 5 Minutes
-------------------------------------------------

Let's get you winning immediately. We'll create a simple calculation, export it, and import it into Leapfrog. You can understand the details later—right now, let's just see it work!

Step 1: Open JupyterLite
~~~~~~~~~~~~~~~~~~~~~~~~~

Visit `https://endarthur.github.io/pollyweb <https://endarthur.github.io/pollyweb>`_

Click the **+** button and select **Python (Pyodide)** under "Notebook". You now have a blank notebook.

Step 2: Copy and Run This Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the first cell, copy this exactly:

.. code-block:: python

   from pollywog.core import CalcSet, Number

   my_first_calc = CalcSet([
       Number("Au_capped", "clamp([Au], 0, 50)")
   ])

   my_first_calc.to_lfcalc("my_first_pollywog.lfcalc")

Press **Shift+Enter** to run it.

Step 3: Download the File
~~~~~~~~~~~~~~~~~~~~~~~~~~

In the file browser on the left, you should see ``my_first_pollywog.lfcalc``. Right-click it and select **Download**.

Step 4: Import into Leapfrog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open your Leapfrog project
2. Navigate to your block model or drillhole data
3. Right-click on the "Evaluations" or "Numeric" section
4. Select "Import" → "From File"
5. Choose your ``my_first_pollywog.lfcalc`` file

You should now see a calculation called ``Au_capped`` in Leapfrog that caps gold values between 0 and 50!

🎉 **Congratulations!** You just automated your first Leapfrog calculation with code.

Now let's understand what you just did...

Getting Started with JupyterLite
---------------------------------

JupyterLite runs Python directly in your web browser—no installation required.

.. note::
   **Important:** JupyterLite saves your work in your browser's memory. If you clear your browser cache, you'll lose your work! Always download your notebooks and .lfcalc files when you're done.

The JupyterLite Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~

When you open JupyterLite, you'll see:

- **File Browser (left side)**: Like Windows Explorer, shows your notebooks and files
- **Notebook (center)**: Where you write and run Python code
- **Code Cells**: Boxes where you type Python code
- **Run Button**: Click it to execute the code in a cell (or press Shift+Enter)

Creating Cells
~~~~~~~~~~~~~~

Notebooks have two types of cells:

**Code Cells** (for Python)
   Type Python code here and run it with Shift+Enter

**Markdown Cells** (for notes)
   Document what your code does. To create one:

   1. Click on a cell
   2. Change the dropdown from "Code" to "Markdown"
   3. Type your notes (you can use headings, bullet points, bold text)
   4. Press Shift+Enter to render it

**Example markdown:**

.. code-block:: markdown

   # My Gold Grade Calculations

   This notebook creates calculations for:
   - Cleaning assay data
   - Domain-weighted composites
   - Recovery factors

   **Project:** Smith Mine 2024

For more on Jupyter and markdown, see the `Jupyter documentation <https://jupyter-notebook.readthedocs.io/en/stable/>`_.

Python Essentials for Geologists
---------------------------------

Good news: You don't need to become a Python expert! You need about 5 core concepts, and the rest you can Google when needed (just like you do with Excel formulas).

Let's learn just enough Python to be productive.

Importing: Getting Your Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you can use Pollywog, you need to import it (like opening a toolbox).

**Try this in a code cell:**

.. code-block:: python

   from pollywog.core import CalcSet, Number, Category
   from pollywog.helpers import WeightedAverage

Press Shift+Enter. If no error appears, you're ready!

.. note::
   Always put your imports at the top of your notebook. That way all your tools are loaded before you use them.

Strings: Text in Quotes
~~~~~~~~~~~~~~~~~~~~~~~

In Python, text goes in quotes. You'll use this for calculation names and expressions.

**Try this:**

.. code-block:: python

   calculation_name = "Au_clean"
   expression = "clamp([Au], 0)"
   print(calculation_name)
   print(expression)

**You should see:**

::

   Au_clean
   clamp([Au], 0)

**Important:** Leapfrog expressions (like ``"clamp([Au], 0)"``) are just text strings to Python. The square brackets ``[Au]`` are part of the text, not Python syntax.

**Quote types:**

.. code-block:: python

   # Single quotes and double quotes both work
   name1 = "Au_clean"
   name2 = 'Au_clean'

   # Use one inside the other for nested quotes
   category_value = "'ore'"  # Double outside, single inside
   # This becomes the text: 'ore' (including the quotes!)

Variables: Storing Values
~~~~~~~~~~~~~~~~~~~~~~~~~

In Python, you store values in variables (different from Leapfrog's ``[Au]`` variables!).

**Try this:**

.. code-block:: python

   # Store values
   gold_price = 1800
   silver_price = 22

   # Use them
   total = gold_price + silver_price
   print(total)

**You should see:**

::

   1822

**Key points:**

- Variable names don't use square brackets (that's Leapfrog syntax)
- Use ``=`` to assign a value
- Lines starting with ``#`` are comments (notes to yourself)

Lists: Multiple Items
~~~~~~~~~~~~~~~~~~~~~

Sometimes you need multiple items. Use square brackets to make a list.

**Try this:**

.. code-block:: python

   # A list of metals
   metals = ["Au", "Ag", "Cu"]

   # A list of domains
   domains = ["oxide", "transition", "sulfide"]

   # See what's in a list
   print(metals)
   print(len(metals))  # How many items?
   print(metals[0])    # First item (counting starts at 0!)

**You should see:**

::

   ['Au', 'Ag', 'Cu']
   3
   Au

**Think of it like:** A column in Excel—multiple values in one container.

Functions: Doing Things
~~~~~~~~~~~~~~~~~~~~~~~

Functions perform actions. You call them with parentheses ``()``.

**Try this:**

.. code-block:: python

   # Built-in Python function
   numbers = [1, 2, 3, 4, 5]
   total = sum(numbers)
   print(total)

   # Pollywog function
   calc = Number("test", "[Au] * 2")
   print(calc.name)

**You should see:**

::

   15
   test

You'll mostly be *using* functions that Pollywog provides, not creating your own.

Comments: Documenting Your Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lines starting with ``#`` are comments—Python ignores them. Use them to explain your thinking.

**Try this:**

.. code-block:: python

   # This is a comment explaining what I'm doing
   price = 1850  # This is an inline comment

   # Comments help you remember why you did something
   # When you come back in 6 months, you'll thank yourself!

From Leapfrog Calculator to Pollywog
------------------------------------

Let's translate what you know from Leapfrog's calculator into Pollywog code.

Simple Calculation
~~~~~~~~~~~~~~~~~~

**In Leapfrog Calculator:**

- Name: ``Au_clean``
- Expression: ``clamp([Au], 0)``
- Comment: "Remove negative values"

**In Pollywog:**

.. code-block:: python

   from pollywog.core import Number

   Au_clean = Number(
       "Au_clean",
       "clamp([Au], 0)",
       comment_equation="Remove negative values"
   )

**What's happening:**

1. ``Number(...)`` creates a numeric calculation
2. First parameter: the name (``"Au_clean"``)
3. Second parameter: the expression (``"clamp([Au], 0)"``)
4. ``comment_equation=`` adds a comment (optional but recommended)

.. note::
   Notice that expressions in Pollywog use the **exact same syntax** as Leapfrog's calculator! If you know how to write ``[Au] * 2`` in Leapfrog, you can use it in Pollywog.

Multiple Calculations: The CalcSet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**In Leapfrog Calculator:**

You'd create each calculation one by one:

1. Au_clean: ``clamp([Au], 0)``
2. Au_log: ``log([Au_clean] + 1e-6)``
3. Au_scaled: ``[Au_log] * 0.95``

**In Pollywog:**

.. code-block:: python

   from pollywog.core import CalcSet, Number

   # Create all calculations at once
   preprocessing = CalcSet([
       Number("Au_clean", "clamp([Au], 0)",
              comment_equation="Remove negative values"),
       Number("Au_log", "log([Au_clean] + 1e-6)",
              comment_equation="Log transform"),
       Number("Au_scaled", "[Au_log] * 0.95",
              comment_equation="Apply 95% factor"),
   ])

   # Export to use in Leapfrog
   preprocessing.to_lfcalc("my_calculations.lfcalc")

**Key concept:** ``CalcSet([...])`` is a container holding multiple calculations. The square brackets ``[...]`` create a list of calculations.

Understanding Variable vs Number vs Category
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pollywog has three types of calculation items. Understanding when to use each is important.

**Variable**
   - Visible in Leapfrog's calculator UI
   - **NOT available** outside the calculator (can't visualize in 3D, can't use in other Leapfrog tools)
   - Use for **intermediate steps** you need for calculations but won't visualize or export
   - Can hold numeric or categorical values

**Number**
   - Visible in Leapfrog's calculator UI
   - **Available everywhere** (can visualize, export, use in other tools)
   - Use for **final numeric outputs** you want to work with
   - Examples: composite grades, recoveries, NSR values

**Category**
   - Visible in Leapfrog's calculator UI
   - **Available everywhere** (can visualize, export, use in other tools)
   - Use for **final categorical outputs** like classifications
   - Examples: ore/waste, domain names, rock types

**Quick decision guide:**

.. code-block:: text

   "Will I need to visualize this in 3D or use it outside the calculator?"

   YES → Use Number (numeric) or Category (text)
   NO  → Use Variable (intermediate step)

**Example showing the difference:**

.. code-block:: python

   from pollywog.core import CalcSet, Variable, Number

   calcs = CalcSet([
       # Intermediate cleaning steps (won't visualize these)
       Variable("Au_clean", "clamp([Au], 0)"),
       Variable("Au_capped", "clamp([Au_clean], 0, 100)"),
       Variable("Au_log", "log([Au_capped] + 0.01)"),

       # Final result (this is what you'll visualize and export!)
       Number("Au_kriged", "[Au_log] * 0.95",
              comment_equation="Prepared for kriging")
   ])

In Leapfrog's calculator, you'll see all 4 items. But only ``Au_kriged`` is available for 3D visualization, exporting to CSV, or using in other Leapfrog tools. The Variables exist only within the calculator context.

**Why use Variables?**

.. code-block:: python

   # Without Variables: Your block model gets cluttered with 15 intermediate steps!
   # You'll see Au_step1, Au_step2, Au_step3... everywhere

   # With Variables: Clean interface
   # You only see the final results you actually care about
   # But you can still reference the intermediate steps in your calculations

Conditional Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~

**In Leapfrog Calculator:**

- Name: ``ore_class``
- Expression: ``if([Au] >= 0.5, "ore", "waste")``
- Type: Category

**In Pollywog:**

.. code-block:: python

   from pollywog.core import Category, If

   ore_class = Category(
       name="ore_class",
       expression=[
           If("[Au] >= 0.5", "'ore'", "'waste'")
       ]
   )

**Important notes:**

- Use ``Category`` for text outputs (like "ore" or "waste")
- Use ``Number`` for numeric outputs (like ``1.5`` or ``0.88``)
- The expression must be in square brackets: ``expression=[If(...)]``
- Text values need quotes inside quotes: ``"'ore'"`` (outer for Python, inner for Leapfrog)

Graduated Examples: Learning by Doing
--------------------------------------

Let's work through real-world examples, starting simple and building up. Each example builds on skills from the previous ones.

Level 1: Single Simple Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Remove negative gold values.

.. code-block:: python

   from pollywog.core import CalcSet, Number

   cleaning = CalcSet([
       Number("Au_clean", "clamp([Au], 0)",
              comment_equation="Remove negative values")
   ])

   cleaning.to_lfcalc("level1_cleaning.lfcalc")

✓ Download the file and import into Leapfrog to verify it works!

Level 2: Chain of Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Clean data through multiple steps.

.. code-block:: python

   from pollywog.core import CalcSet, Number

   processing = CalcSet([
       Number("Au_clean", "clamp([Au], 0)",
              comment_equation="Remove negative values"),
       Number("Au_capped", "clamp([Au_clean], 0, 100)",
              comment_equation="Cap at 100 g/t to reduce nugget effect"),
       Number("Au_log", "log([Au_capped] + 0.01)",
              comment_equation="Log transform for kriging"),
   ])

   processing.to_lfcalc("level2_chain.lfcalc")

**Notice:** ``Au_capped`` references ``[Au_clean]``, and ``Au_log`` references ``[Au_capped]``. Pollywog handles the dependency order automatically.

Level 3: Using Variables for Intermediate Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Same as Level 2, but keep Leapfrog interface clean.

.. code-block:: python

   from pollywog.core import CalcSet, Variable, Number

   processing_clean = CalcSet([
       # These are intermediate steps (won't export/visualize)
       Variable("Au_clean", "clamp([Au], 0)"),
       Variable("Au_capped", "clamp([Au_clean], 0, 100)"),

       # This is the final result (available everywhere in Leapfrog)
       Number("Au_kriged", "log([Au_capped] + 0.01) * 0.95",
              comment_equation="Cleaned and transformed for kriging"),
   ])

   processing_clean.to_lfcalc("level3_variables.lfcalc")

**Compare:** When you import this, you'll only see ``Au_kriged`` available for visualization. The cleaning steps exist in the calculator but don't clutter your block model interface.

Level 4: Weighted Average (One Metal)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Calculate domain-weighted gold grade.

.. code-block:: python

   from pollywog.core import CalcSet
   from pollywog.helpers import WeightedAverage

   composite = CalcSet([
       WeightedAverage(
           variables=["Au_oxide", "Au_transition", "Au_sulfide"],
           weights=["prop_oxide", "prop_transition", "prop_sulfide"],
           name="Au_composite",
           comment="Domain-weighted gold grade"
       )
   ])

   composite.to_lfcalc("level4_weighted.lfcalc")

**What ``WeightedAverage`` does:** It creates the formula ``([Au_oxide] * [prop_oxide] + [Au_transition] * [prop_transition] + [Au_sulfide] * [prop_sulfide]) / ([prop_oxide] + [prop_transition] + [prop_sulfide])`` for you. Much easier than typing that out!

Level 5: Multiple Weighted Averages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Create weighted composites for Au, Ag, and Cu.

**Version A: Write them all out** (recommended while learning)

.. code-block:: python

   from pollywog.core import CalcSet
   from pollywog.helpers import WeightedAverage

   composites = CalcSet([
       WeightedAverage(
           variables=["Au_oxide", "Au_transition", "Au_sulfide"],
           weights=["prop_oxide", "prop_transition", "prop_sulfide"],
           name="Au_composite",
           comment="Domain-weighted Au grade"
       ),
       WeightedAverage(
           variables=["Ag_oxide", "Ag_transition", "Ag_sulfide"],
           weights=["prop_oxide", "prop_transition", "prop_sulfide"],
           name="Ag_composite",
           comment="Domain-weighted Ag grade"
       ),
       WeightedAverage(
           variables=["Cu_oxide", "Cu_transition", "Cu_sulfide"],
           weights=["prop_oxide", "prop_transition", "prop_sulfide"],
           name="Cu_composite",
           comment="Domain-weighted Cu grade"
       ),
   ])

   composites.to_lfcalc("level5_three_metals.lfcalc")

This is clear and explicit. If you have 3-5 metals, this approach works great!

**Version B: Let Python do the repetition** (for when you have many metals)

If you have 10 metals, writing them all out gets tedious. Here's where Python shines:

.. code-block:: python

   from pollywog.core import CalcSet
   from pollywog.helpers import WeightedAverage

   metals = ["Au", "Ag", "Cu"]
   domains = ["oxide", "transition", "sulfide"]

   # This loop creates one WeightedAverage for each metal
   composites = CalcSet([
       WeightedAverage(
           variables=[f"{metal}_{domain}" for domain in domains],
           weights=[f"prop_{domain}" for domain in domains],
           name=f"{metal}_composite",
           comment=f"Domain-weighted {metal} grade"
       )
       for metal in metals
   ])

   composites.to_lfcalc("level5_automated.lfcalc")

.. note::
   Both versions create the same .lfcalc file! Use Version A until you're comfortable, then learn Version B when you're ready to scale up. We'll explain how the automation works in the "Common Patterns" section later.

Level 6: Classification with Thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Classify blocks by gold grade into waste, low grade, and high grade.

.. code-block:: python

   from pollywog.core import CalcSet
   from pollywog.helpers import CategoryFromThresholds

   classification = CalcSet([
       CategoryFromThresholds(
           variable="Au_composite",
           thresholds=[0.3, 1.0],
           categories=["waste", "low_grade", "high_grade"],
           name="ore_class",
           comment="Material classification by Au grade"
       )
   ])

   classification.to_lfcalc("level6_classification.lfcalc")

**How it works:**

- Au < 0.3: waste
- 0.3 ≤ Au < 1.0: low_grade
- Au ≥ 1.0: high_grade

.. note::
   You need **one more category than thresholds**. Here: 2 thresholds → 3 categories.

Level 7: Conditional Logic with If
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Apply different recovery rates depending on domain.

.. code-block:: python

   from pollywog.core import CalcSet, Number, If

   recovery = CalcSet([
       Number("Au_recovered", [
           If([
               ("[domain] = 'oxide'", "[Au_composite] * 0.92"),
               ("[domain] = 'transition'", "[Au_composite] * 0.85"),
               ("[domain] = 'sulfide'", "[Au_composite] * 0.78"),
           ], otherwise="[Au_composite] * 0.75")
       ], comment_equation="Domain-specific metallurgical recovery")
   ])

   recovery.to_lfcalc("level7_conditional.lfcalc")

**Notice:** The expression is wrapped in ``[If(...)]`` (a list containing one If structure).

Level 8: Complete Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Realistic workflow with composites, recovery, economics, and classification.

.. code-block:: python

   from pollywog.core import CalcSet, Variable, Number, Category, If
   from pollywog.helpers import WeightedAverage, CategoryFromThresholds

   # Complete resource model workflow
   block_model = CalcSet([
       # Domain-weighted composites
       WeightedAverage(
           variables=["Au_oxide", "Au_transition", "Au_sulfide"],
           weights=["prop_oxide", "prop_transition", "prop_sulfide"],
           name="Au_composite",
           comment="Domain-weighted Au grade"
       ),
       WeightedAverage(
           variables=["Cu_oxide", "Cu_transition", "Cu_sulfide"],
           weights=["prop_oxide", "prop_transition", "prop_sulfide"],
           name="Cu_composite",
           comment="Domain-weighted Cu grade"
       ),

       # Intermediate recovery calculations (Variables, not exported)
       Variable("Au_recovery_rate", [
           If([
               ("[domain] = 'oxide'", "0.92"),
               ("[domain] = 'transition'", "0.85"),
               ("[domain] = 'sulfide'", "0.78"),
           ], otherwise="0.75")
       ]),
       Variable("Cu_recovery_rate", [
           If([
               ("[domain] = 'oxide'", "0.88"),
               ("[domain] = 'transition'", "0.82"),
               ("[domain] = 'sulfide'", "0.85"),
           ], otherwise="0.80")
       ]),

       # Recovered metal (exported)
       Number("Au_recovered", "[Au_composite] * [Au_recovery_rate]",
              comment_equation="Domain-adjusted Au recovery"),
       Number("Cu_recovered", "[Cu_composite] * [Cu_recovery_rate]",
              comment_equation="Domain-adjusted Cu recovery"),

       # Economic values (exported)
       Number("Au_value", "[Au_recovered] * 1850 / 31.1035",
              comment_equation="Au value per tonne at $1850/oz"),
       Number("Cu_value", "[Cu_recovered] * 3.5 * 2204.62",
              comment_equation="Cu value per tonne at $3.50/lb"),
       Number("NSR", "[Au_value] + [Cu_value] - 150",
              comment_equation="Net smelter return minus processing costs"),

       # Material classification (exported)
       CategoryFromThresholds(
           variable="NSR",
           thresholds=[50, 150],
           categories=["waste", "low_grade", "high_grade"],
           name="material_type",
           comment="Block classification by NSR"
       ),
   ])

   block_model.to_lfcalc("level8_complete_workflow.lfcalc")

🎉 **Milestone!** If you've made it this far and successfully created this workflow, you're already more productive than doing it manually in Leapfrog. Everything from here is building on these foundations.

Reading and Modifying Existing Files
-------------------------------------

In real projects, you'll often need to read existing .lfcalc files, inspect them, modify them, or add new calculations.

Reading a .lfcalc File
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pollywog.core import CalcSet

   # Read an existing file
   existing = CalcSet.read_lfcalc("my_calculations.lfcalc")

   # How many calculations?
   print(f"This file has {len(existing.items)} calculations")

   # List all calculation names
   for item in existing.items:
       print(f"- {item.name}: {item.item_type}")

Inspecting Calculations
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pollywog.core import CalcSet

   model = CalcSet.read_lfcalc("resource_model.lfcalc")

   # Find all Au-related calculations
   for item in model.items:
       if "Au" in item.name:
           print(f"{item.name}: {item.expression}")

   # Or use the query method (like pandas)
   au_calcs = model.query('name.startswith("Au")')
   print(f"Found {len(au_calcs.items)} Au calculations")

Modifying Existing Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pollywog.core import CalcSet

   # Read file
   model = CalcSet.read_lfcalc("old_model.lfcalc")

   # Find and update a specific calculation
   for item in model.items:
       if item.name == "Au_recovered":
           # Update recovery rate from 88% to 90%
           item.expression = ["[Au_composite] * 0.90"]
           item.comment_equation = "Updated recovery per new test work"

   # Save as new file
   model.to_lfcalc("updated_model.lfcalc")

Adding New Calculations
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pollywog.core import CalcSet, Number

   # Read existing file
   model = CalcSet.read_lfcalc("resource_model.lfcalc")

   # Add new calculations
   model.items.append(
       Number("Au_value", "[Au_recovered] * 1900",
              comment_equation="Gold value at updated price $1900/oz")
   )

   model.items.append(
       Number("Cu_equiv", "[Cu] + ([Au] * 60)",
              comment_equation="Copper equivalent using 60:1 price ratio")
   )

   # Export updated file
   model.to_lfcalc("resource_model_v2.lfcalc")

Debugging and Testing Your Calculations
----------------------------------------

When things don't work as expected, here's how to find and fix issues.

Common Python Errors
~~~~~~~~~~~~~~~~~~~~

**"SyntaxError: invalid syntax"**

You have a typo or missing punctuation.

Common causes:

- Missing comma between items in a list
- Missing closing parenthesis or bracket
- Missing quote mark

**Fix:** Look at the line number in the error. Check for missing commas, brackets, or quotes.

Example:

.. code-block:: python

   # WRONG - missing comma
   CalcSet([
       Number("a", "x")
       Number("b", "y")
   ])

   # RIGHT
   CalcSet([
       Number("a", "x"),  # ← comma here!
       Number("b", "y")
   ])

**"NameError: name 'CalcSet' is not defined"**

You forgot to import.

**Fix:** Add at the top of your notebook:

.. code-block:: python

   from pollywog.core import CalcSet, Number, Category, Variable

**"ValueError: ..."**

You passed the wrong type or number of values to a function.

**Fix:** Check the error message carefully—it usually tells you what's wrong. Common issues:

- Wrong number of categories vs thresholds (need N+1 categories for N thresholds)
- Empty lists where values are expected
- Mixing up parameter order

Common Leapfrog Issues
~~~~~~~~~~~~~~~~~~~~~~

**Your calculation imports but gives wrong results:**

**Checklist:**

1. **Variable names match exactly** (case-sensitive!): ``[Au]`` ≠ ``[au]``
2. **Square brackets around variables**: ``[Au] * 2`` not ``Au * 2``
3. **Quotes for category values**: ``"'ore'"`` not ``"ore"``
4. **Units are consistent**: g/t vs %, oz/ton vs g/t, $/oz vs $/lb
5. **Null/missing data handled**: Use ``coalesce([Au], 0)`` to replace nulls

**Your calculation doesn't appear where expected:**

- Check if you used ``Variable`` (calculator only) vs ``Number``/``Category`` (available everywhere)
- Variables won't show up for 3D visualization or export

Testing Strategies
~~~~~~~~~~~~~~~~~~

**Create a simple test case:**

.. code-block:: python

   # Known input and expected output
   test = CalcSet([
       Number("test_Au", "1.5"),
       Number("test_recovery", "0.88"),
       Number("test_result", "[test_Au] * [test_recovery]"),
       # Expected: test_result should be 1.32
   ])

   test.to_lfcalc("test_recovery.lfcalc")

Import to Leapfrog and verify ``test_result`` equals 1.32. If not, your formula has an issue.

**Test with edge cases:**

.. code-block:: python

   # Test boundary conditions
   edge_tests = CalcSet([
       Number("zero_test", "0"),
       Number("negative_test", "-5"),
       Number("large_test", "999999"),
       Number("result", "clamp([zero_test], 0, 100)"),  # Should be 0
   ])

**Verification workflow:**

1. Create calculation with Pollywog
2. Export to .lfcalc
3. Import to Leapfrog
4. Check a few blocks with known values
5. Export results to CSV
6. Spot-check in Excel
7. Compare against previous model (if updating)

Common Patterns Explained
--------------------------

As you use Pollywog, you'll see some patterns repeat. Here are the most common ones.

F-Strings: Text Templates
~~~~~~~~~~~~~~~~~~~~~~~~~

F-strings let you insert variable values into text. Very useful for creating many similar names.

.. code-block:: python

   metal = "Au"
   domain = "oxide"

   # Create a variable name by combining text and variables
   var_name = f"{metal}_{domain}"
   print(var_name)  # Shows: Au_oxide

   # The f before the quotes makes it an "f-string"
   # Anything in {curly braces} gets replaced with the variable value

**Practical use:**

.. code-block:: python

   metal = "Au"
   domains = ["oxide", "transition", "sulfide"]

   # Create variable names for all domains
   variables = [f"{metal}_{domain}" for domain in domains]
   print(variables)
   # Shows: ['Au_oxide', 'Au_transition', 'Au_sulfide']

List Comprehensions: Automation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List comprehensions create lists by repeating a pattern. This is Python's way of doing "for each item, do this."

**Basic pattern:**

.. code-block:: python

   metals = ["Au", "Ag", "Cu"]

   # Create composite names for each metal
   composite_names = [f"{metal}_composite" for metal in metals]
   print(composite_names)
   # Shows: ['Au_composite', 'Ag_composite', 'Cu_composite']

**Think of it as:** "For each metal in my list, create a name using this pattern."

**In Pollywog:**

.. code-block:: python

   from pollywog.core import CalcSet
   from pollywog.helpers import WeightedAverage

   metals = ["Au", "Ag", "Cu", "Pb", "Zn"]
   domains = ["oxide", "transition", "sulfide"]

   # Create one WeightedAverage for each metal
   composites = CalcSet([
       WeightedAverage(
           variables=[f"{metal}_{domain}" for domain in domains],
           weights=[f"prop_{domain}" for domain in domains],
           name=f"{metal}_composite",
           comment=f"Domain-weighted {metal} grade"
       )
       for metal in metals  # ← This repeats the whole WeightedAverage for each metal
   ])

This creates 5 weighted averages (one for each metal) automatically!

The Unpacking Operator (*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``*`` unpacks a list, putting each item directly where you use it.

**Why you need it:**

.. code-block:: python

   # Create multiple calculations with a loop
   extra_calcs = [Number(f"calc_{i}", f"[Au] * {i}") for i in range(3)]

   # WRONG - creates a nested list
   CalcSet([extra_calcs, Number("final", "[Au]")])
   # Result: [[calc_0, calc_1, calc_2], final]  ← nested, won't work!

   # RIGHT - unpacks the list
   CalcSet([*extra_calcs, Number("final", "[Au]")])
   # Result: [calc_0, calc_1, calc_2, final]  ← flat list, correct!

**Think of it as:** "Unpack this list and put each item directly here."

Named Parameters
~~~~~~~~~~~~~~~~

Functions in Pollywog often use named parameters for clarity.

.. code-block:: python

   # You can use positional parameters (shorter)
   Number("Au_clean", "clamp([Au], 0)")

   # Or named parameters (clearer)
   Number(
       name="Au_clean",
       expression="clamp([Au], 0)",
       comment_equation="Remove negative values"
   )

   # Both work! Use whichever feels clearer to you

**Benefits of named parameters:**

- Makes code more readable
- Can put parameters in any order
- Can skip optional parameters
- Easy to see what each value means

Common Mistakes and How to Fix Them
------------------------------------

Everyone makes mistakes when learning. Here are the most common ones.

Mistake 1: Forgetting Square Brackets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   Number("result", "Au * 2")

**Problem:** In Leapfrog expressions, variable references need square brackets.

**Fix:**

.. code-block:: python

   Number("result", "[Au] * 2")

Mistake 2: Quote Confusion in Categories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   Category("type", [If("[Au] > 0.5", "ore", "waste")])

**Problem:** Category values need to be quoted in the Leapfrog expression.

**Fix:**

.. code-block:: python

   Category("type", [If("[Au] > 0.5", "'ore'", "'waste'")])

**Remember:** Use ``"'text'"`` (double quotes outside, single quotes inside) for category values.

Mistake 3: Forgetting to Import
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   calcset = CalcSet([...])
   # Error: NameError: name 'CalcSet' is not defined

**Problem:** You need to import before you can use Pollywog classes.

**Fix:**

.. code-block:: python

   from pollywog.core import CalcSet, Number

   calcset = CalcSet([...])

Mistake 4: Missing Commas in Lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   CalcSet([
       Number("a", "[x] * 2")
       Number("b", "[y] * 2")
   ])

**Problem:** Python lists need commas between items.

**Fix:**

.. code-block:: python

   CalcSet([
       Number("a", "[x] * 2"),  # ← comma here
       Number("b", "[y] * 2")   # ← comma optional on last item
   ])

Mistake 5: Using Number for Categories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   Number("type", [If("[Au] > 0.5", "'ore'", "'waste'")])

**Problem:** Numbers can't hold text values.

**Fix:**

.. code-block:: python

   Category("type", [If("[Au] > 0.5", "'ore'", "'waste'")])

**Rule:** Use ``Number`` for numeric results, ``Category`` for text results.

Mistake 6: Wrong Number of Categories vs Thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   CategoryFromThresholds(
       variable="Au",
       thresholds=[0.3, 1.0],
       categories=["waste", "ore"]  # Only 2 categories!
   )

**Problem:** Need one more category than thresholds.

**Fix:**

.. code-block:: python

   CategoryFromThresholds(
       variable="Au",
       thresholds=[0.3, 1.0],
       categories=["waste", "low_grade", "high_grade"]  # 3 categories for 2 thresholds
   )

Mistake 7: Variable vs Number Confusion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   # Want to visualize this in 3D, but used Variable
   Variable("Au_composite", "...")

**Problem:** Variables aren't available outside the calculator.

**Fix:**

.. code-block:: python

   # Use Number if you need to visualize, export, or use in other tools
   Number("Au_composite", "...")

Best Practices
--------------

Commenting Your Work
~~~~~~~~~~~~~~~~~~~~

Add comments to document your logic—your future self will thank you!

.. code-block:: python

   # BAD: States the obvious
   Number("Au_recovered", "[Au] * 0.88",
          comment_equation="Multiply Au by 0.88")

   # GOOD: Explains the why and includes context
   Number("Au_recovered", "[Au] * 0.88",
          comment_equation="Metallurgical recovery per June 2024 test work")

   # BETTER: Includes source document
   Number("Au_recovered", "[Au] * 0.88",
          comment_equation="88% recovery per Met Lab Report ML-2024-06")

Use Variables for Intermediate Steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Keep your Leapfrog interface clean by using Variables for calculations you won't visualize.

.. code-block:: python

   # GOOD: Only final result is a Number
   CalcSet([
       Variable("Au_clean", "clamp([Au], 0)"),
       Variable("Au_capped", "clamp([Au_clean], 0, 100)"),
       Number("Au_final", "[Au_capped] * 0.95")
   ])

Organize with Markdown Cells
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use markdown cells in your notebooks to explain what each section does:

.. code-block:: markdown

   ## Data Cleaning

   Remove negative values and cap extreme outliers.

   ## Domain Composites

   Calculate weighted averages for each metal across three domains.

   ## Economic Calculations

   Apply recovery rates and metal prices to calculate NSR.

Test Before Scaling Up
~~~~~~~~~~~~~~~~~~~~~~~

When creating many calculations with loops:

1. Test with 1-2 items first
2. Verify in Leapfrog
3. Then scale up to full list

.. code-block:: python

   # Test with just Au first
   metals = ["Au"]
   # ... create calculations ...
   # ... verify in Leapfrog ...

   # Once working, scale up
   metals = ["Au", "Ag", "Cu", "Pb", "Zn", "Mo", "As", "Fe", "S"]

Version Your Files
~~~~~~~~~~~~~~~~~~

Keep track of changes by using version numbers or dates in filenames:

.. code-block:: python

   model.to_lfcalc("resource_model_v1.lfcalc")
   # Later...
   model.to_lfcalc("resource_model_v2_updated_recovery.lfcalc")
   # Or with dates...
   model.to_lfcalc("resource_model_2024-01-15.lfcalc")

When to Use Pollywog vs Manual
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Pollywog when:**

- Creating >10 similar calculations
- Need to update many calculations at once
- Want version control for workflows
- Reusing patterns across projects
- Automating repetitive work

**Use Leapfrog's Calculator when:**

- One-off custom calculation
- Experimental/exploratory work
- Very simple single calculation
- Still learning the pattern

**The sweet spot:** Use both! Prototype in Leapfrog's calculator, then convert to Pollywog when you need to scale or reuse.

Downloading Files from JupyterLite
-----------------------------------

You have two options to download your .lfcalc files:

Option 1: Enable Autodownload Magic (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the top of your notebook, run:

.. code-block:: python

   %load_ext pollywog.magics
   %pollywog autodownload on

Now when you run ``to_lfcalc()``, a download button appears below the cell. Click it to save the file.

Option 2: Manual Download
~~~~~~~~~~~~~~~~~~~~~~~~~~

In JupyterLite's file browser (left side), right-click on your ``.lfcalc`` file and select "Download".

Tips for Success
-----------------

1. **Start small:** Begin with 2-3 calculations and get comfortable before tackling complex workflows

2. **Test frequently:** Export and test in Leapfrog often to catch issues early

3. **Use comments:** Add ``comment_equation`` to document your logic

4. **Copy examples:** There's no shame in copying working code and modifying it—that's how everyone learns!

5. **Build a library:** Save your successful scripts for reuse on future projects

6. **Use markdown cells:** Document what each section of your notebook does

7. **Keep it readable:** If a formula gets too complex, break it into Variables

8. **Ask for help:** If you're stuck, check the documentation or ask Python-savvy colleagues

Saving and Organizing Your Work
--------------------------------

In JupyterLite
~~~~~~~~~~~~~~

**Remember:** JupyterLite stores everything in browser memory!

**Best practices:**

1. Download your notebooks regularly (File → Download)
2. Download .lfcalc files immediately after creating them
3. Keep backups on your computer or network drive
4. Consider one notebook per project or workflow stage
5. Clear browser cache carefully (you'll lose unsaved work!)

On Your Computer
~~~~~~~~~~~~~~~~

If you install Python and Pollywog locally (see :doc:`getting_started`), you can:

- Save notebooks and scripts directly to your file system
- Use version control (Git) to track changes
- Integrate with your company's data management systems
- Better performance for large calculation sets

Next Steps
----------

Now that you understand the basics:

Practice Projects
~~~~~~~~~~~~~~~~~

1. Recreate a simple calculation set from one of your Leapfrog projects
2. Build domain-weighted composites for your most common metals
3. Create a classification system for your typical ore types
4. Add economic calculations (recovery, metal prices, NSR)

Learn More
~~~~~~~~~~

- :doc:`getting_started` - Installing Pollywog on your computer
- :doc:`tutorials` - More detailed workflow examples
- :doc:`expression_syntax` - Complete guide to Leapfrog expression syntax
- :doc:`helpers_guide` - All available helper functions
- :doc:`workflow_patterns` - Common patterns for different scenarios

Advanced Topics (For Later)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Converting Excel formulas to Pollywog
- Building calculation templates for your company
- Integrating machine learning models
- Automating complete workflows

Getting Help
------------

If you get stuck:

1. **Check the examples:** The ``examples/`` folder in the GitHub repository has working notebooks
2. **Read the documentation:** https://pollywog.readthedocs.io
3. **Search for similar issues:** https://github.com/endarthur/pollywog/issues
4. **Ask questions:** Open a new issue on GitHub

The Pollywog community is friendly and helpful. Don't be afraid to ask questions!

Final Thoughts
--------------

Learning Python and Pollywog might feel challenging at first, but remember:

- You already understand the concepts (you use Leapfrog's calculator!)
- You're just learning a new way to express the same ideas
- The time investment pays off quickly—often after just one project
- Every resource geologist who learns this says: "I wish I'd learned it sooner"

Start with simple examples, build confidence, and gradually tackle more complex workflows. Before you know it, you'll be automating calculations that used to take hours.

**You've got this!** 🪨✨
