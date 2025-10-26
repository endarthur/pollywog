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

Getting Started with JupyterLite
---------------------------------

The easiest way to try Pollywog is through JupyterLite—it runs Python directly in your web browser, no installation required.

**Try it now:** Visit `https://endarthur.github.io/pollyweb <https://endarthur.github.io/pollyweb>`_

.. note::
   **Important:** JupyterLite saves your work in your browser's memory. If you clear your browser cache, you'll lose your work! Always download your notebooks and .lfcalc files when you're done.

What You'll See in JupyterLite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you open JupyterLite, you'll see an interface similar to Jupyter Notebook. Here's what the main parts do:

- **File Browser (left side)**: Like Windows Explorer, shows your notebooks and files
- **Notebook (center)**: Where you write and run Python code
- **Code Cells**: Boxes where you type Python code
- **Run Button**: Click it to execute the code in a cell (or press Shift+Enter)

Creating Your First Notebook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Click the **+** button in the file browser
2. Select **Python (Pyodide)** under "Notebook"
3. You now have a blank notebook with one code cell
4. Try typing this and press Shift+Enter:

.. code-block:: python

   print("Hello, Pollywog!")

Congratulations! You just ran your first Python code.

Python Basics You Need to Know
-------------------------------

Don't worry—you don't need to become a Python expert. You just need to understand a few concepts.

Variables: Storing Values
~~~~~~~~~~~~~~~~~~~~~~~~~

In Leapfrog's calculator, you reference variables like ``[Au]`` or ``[Cu]``. In Python, you can create your own variables:

.. code-block:: python

   # In Python, we store values in variables like this:
   gold_price = 1800
   silver_price = 22
   
   # Now we can use these variables:
   total = gold_price + silver_price
   print(total)  # Shows: 1822

**Key points:**

- Variable names in Python don't need square brackets
- Use ``=`` to assign a value to a variable
- Lines starting with ``#`` are comments (notes to yourself)

Lists: Multiple Items
~~~~~~~~~~~~~~~~~~~~~

Sometimes you need to work with multiple items. In Python, we use lists:

.. code-block:: python

   # A list of metals we're interested in
   metals = ["Au", "Ag", "Cu"]
   
   # A list of domains
   domains = ["oxide", "transition", "sulfide"]
   
   # You can see what's in a list:
   print(metals)  # Shows: ['Au', 'Ag', 'Cu']

**Think of it this way:** A list is like a column in Excel—multiple values in one container.

Functions: Reusable Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Functions do things. You've already used one: ``print()``. Pollywog provides many helpful functions.

.. code-block:: python

   # This function adds numbers together
   total = sum([1, 2, 3, 4, 5])
   print(total)  # Shows: 15

You'll mostly be *using* functions that Pollywog provides, not creating your own.

Importing: Getting Tools
~~~~~~~~~~~~~~~~~~~~~~~~

Before you can use Pollywog, you need to import it (like opening a toolbox):

.. code-block:: python

   # Import the tools we need from Pollywog
   from pollywog.core import CalcSet, Number
   from pollywog.helpers import WeightedAverage

**Think of it this way:** Importing is like telling Python "I need these specific tools from the Pollywog toolbox."

From Leapfrog Calculator to Pollywog
------------------------------------

Let's translate what you know from Leapfrog's calculator to Pollywog code.

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

**What's happening here?**

1. ``Number(...)`` creates a numeric calculation
2. First parameter: the name (``"Au_clean"``)
3. Second parameter: the expression (``"clamp([Au], 0)"``)
4. ``comment_equation=`` adds a comment (optional but recommended)

.. note::
   Notice that expressions in Pollywog use the **exact same syntax** as Leapfrog's calculator! If you know how to write ``[Au] * 2`` in Leapfrog, you can use it in Pollywog.

Multiple Calculations
~~~~~~~~~~~~~~~~~~~~~

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

**Key concept:** ``CalcSet([...])`` is a container that holds multiple calculations. The square brackets ``[...]`` create a list of calculations.

Conditional Calculations (If/Else)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

- Use ``Category`` for text/categorical outputs (like "ore" or "waste")
- Use ``Number`` for numeric outputs (like ``1.5`` or ``0.88``)
- When you have an ``If`` statement, the expression must be in square brackets: ``expression=[If(...)]``
- Text values need quotes inside quotes: ``"'ore'"`` (outer quotes for Python, inner quotes for Leapfrog)

Practical Examples
------------------

Let's work through real-world scenarios you face as a resource geologist.

Example 1: Cleaning Assay Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** You have gold assays and need to:

1. Remove negative values
2. Cap extreme values at 100 g/t
3. Create a log transform for kriging

**The Pollywog Way:**

.. code-block:: python

   from pollywog.core import CalcSet, Number
   
   # Create all cleaning steps
   cleaning = CalcSet([
       Number("Au_clean", "clamp([Au], 0)",
              comment_equation="Remove negative values"),
       Number("Au_capped", "clamp([Au_clean], 0, 100)",
              comment_equation="Cap at 100 g/t to reduce nugget effect"),
       Number("Au_log", "log([Au_capped] + 0.01)",
              comment_equation="Log transform for kriging"),
   ])
   
   # Export for Leapfrog
   cleaning.to_lfcalc("drillhole_cleaning.lfcalc")

After running this code, click the download button that appears below the cell to save ``drillhole_cleaning.lfcalc`` to your computer. Then import it into Leapfrog!

Example 2: Domain-Weighted Grades
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** You've estimated gold grades for three domains (oxide, transition, sulfide) and have domain proportions. Now you need to calculate the composite grade.

**In Leapfrog Calculator:**

You'd write something like:
``([Au_oxide] * [prop_oxide] + [Au_transition] * [prop_transition] + [Au_sulfide] * [prop_sulfide]) / ([prop_oxide] + [prop_transition] + [prop_sulfide])``

That's long and error-prone!

**The Pollywog Way:**

.. code-block:: python

   from pollywog.core import CalcSet
   from pollywog.helpers import WeightedAverage
   
   # Let Pollywog write the formula for you
   composite = CalcSet([
       WeightedAverage(
           variables=["Au_oxide", "Au_transition", "Au_sulfide"],
           weights=["prop_oxide", "prop_transition", "prop_sulfide"],
           name="Au_composite",
           comment="Domain-weighted gold grade"
       )
   ])
   
   composite.to_lfcalc("domain_composite.lfcalc")

**Much easier!** Pollywog handles the complex formula for you.

Example 3: Multiple Metals, Multiple Domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** You need domain-weighted composites for Au, Ag, Cu, Pb, and Zn across three domains.

**In Leapfrog Calculator:**

You'd create 5 calculations, each with a long formula. That's tedious and mistakes happen.

**The Pollywog Way:**

.. code-block:: python

   from pollywog.core import CalcSet
   from pollywog.helpers import WeightedAverage
   
   # Define your metals and domains
   metals = ["Au", "Ag", "Cu", "Pb", "Zn"]
   domains = ["oxide", "transition", "sulfide"]
   
   # Create composites for ALL metals at once
   composites = CalcSet([
       WeightedAverage(
           variables=[f"{metal}_{domain}" for domain in domains],
           weights=[f"prop_{domain}" for domain in domains],
           name=f"{metal}_composite",
           comment=f"Domain-weighted {metal} grade"
       )
       for metal in metals
   ])
   
   composites.to_lfcalc("all_metal_composites.lfcalc")

**What just happened?**

This creates 5 calculations (one for each metal), each with the proper domain weighting. The ``for metal in metals`` part repeats the calculation for each metal in your list.

**Think of it like this:** Instead of copy-pasting 5 times and changing "Au" to "Ag", "Cu", etc., Python does the repetition for you.

Example 4: Grade Classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Classify blocks by gold grade into waste, low grade, medium grade, and high grade.

**In Leapfrog Calculator:**

You'd write nested if statements—messy and hard to read.

**The Pollywog Way:**

.. code-block:: python

   from pollywog.core import CalcSet
   from pollywog.helpers import CategoryFromThresholds
   
   classification = CalcSet([
       CategoryFromThresholds(
           variable="Au_composite",
           thresholds=[0.3, 1.0, 3.0],
           categories=["waste", "low_grade", "medium_grade", "high_grade"],
           name="ore_class",
           comment="Material classification by Au grade"
       )
   ])
   
   classification.to_lfcalc("classification.lfcalc")

**How it works:**

- Au < 0.3: waste
- 0.3 ≤ Au < 1.0: low_grade  
- 1.0 ≤ Au < 3.0: medium_grade
- Au ≥ 3.0: high_grade

Example 5: Recovery and Economic Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Calculate recovered metal and net smelter return (NSR) for gold and copper.

.. code-block:: python

   from pollywog.core import CalcSet, Number
   
   economics = CalcSet([
       # Apply metallurgical recovery
       Number("Au_recovered", "[Au_composite] * 0.88",
              comment_equation="88% recovery"),
       Number("Cu_recovered", "[Cu_composite] * 0.82",
              comment_equation="82% recovery"),
       
       # Calculate NSR (simplified)
       Number("Au_value", "[Au_recovered] * 1800",
              comment_equation="Gold at $1800/oz"),
       Number("Cu_value", "[Cu_recovered] * 3.5",
              comment_equation="Copper at $3.50/lb"),
       Number("NSR_total", "[Au_value] + [Cu_value]",
              comment_equation="Total net smelter return"),
   ])
   
   economics.to_lfcalc("economics.lfcalc")

Step-by-Step Workflow in JupyterLite
-------------------------------------

Let's walk through a complete workflow from start to finish.

Step 1: Open JupyterLite
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Visit https://endarthur.github.io/pollyweb
2. Create a new Python notebook
3. Name it something like "My_First_Pollywog_Project"

Step 2: Import Pollywog
~~~~~~~~~~~~~~~~~~~~~~~~

In the first cell, type:

.. code-block:: python

   from pollywog.core import CalcSet, Number, Category
   from pollywog.helpers import WeightedAverage, CategoryFromThresholds

Press Shift+Enter to run the cell. If no error appears, you're ready to go!

Step 3: Create Your Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the next cell, create your calculations. Here's a complete example:

.. code-block:: python

   # Define the metals and domains for your project
   metals = ["Au", "Ag", "Cu"]
   domains = ["oxide", "transition", "sulfide"]
   
   # Create domain-weighted composites
   block_model = CalcSet([
       # Weighted averages for each metal
       *[WeightedAverage(
           variables=[f"{metal}_{domain}" for domain in domains],
           weights=[f"prop_{domain}" for domain in domains],
           name=f"{metal}_composite",
           comment=f"Domain-weighted {metal} grade"
       ) for metal in metals],
       
       # Apply dilution
       Number("Au_diluted", "[Au_composite] * 0.95",
              comment_equation="5% dilution"),
       
       # Apply recovery
       Number("Au_recovered", "[Au_diluted] * 0.88",
              comment_equation="88% metallurgical recovery"),
       
       # Classify blocks
       CategoryFromThresholds(
           variable="Au_recovered",
           thresholds=[0.3, 1.0],
           categories=["waste", "low_grade", "high_grade"],
           name="material_type",
           comment="Block classification"
       ),
   ])

Step 4: Export Your Calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the next cell:

.. code-block:: python

   # Export to .lfcalc file
   block_model.to_lfcalc("block_model_calculations.lfcalc")

When you run this cell, a download button appears below it. Click the button to save the file to your computer.

Step 5: Import into Leapfrog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open your Leapfrog project
2. Navigate to your block model
3. Right-click on the "Evaluations" or "Numeric" section
4. Select "Import" → "From File"
5. Choose your ``block_model_calculations.lfcalc`` file
6. Your calculations appear in Leapfrog!

Step 6: Verify in Leapfrog
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check a few blocks to make sure the calculations produce expected values. If something's wrong, you can fix it in Python and re-export—much faster than recreating everything in Leapfrog!

Understanding Common Patterns
------------------------------

As you use Pollywog, you'll see some patterns repeat. Here are the most common ones.

Pattern 1: The List Comprehension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You'll often see code like this:

.. code-block:: python

   [f"{metal}_composite" for metal in metals]

**What it does:** Creates a list of names by inserting each metal into the pattern.

**Example:**

.. code-block:: python

   metals = ["Au", "Ag", "Cu"]
   result = [f"{metal}_composite" for metal in metals]
   print(result)
   # Shows: ['Au_composite', 'Ag_composite', 'Cu_composite']

**Think of it as:** "For each metal in my list, create a name using this pattern"

The ``f"..."`` part is called an "f-string" and lets you insert variable values into text using ``{variable}``.

Pattern 2: The Unpacking Operator (*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You'll sometimes see code like this:

.. code-block:: python

   CalcSet([
       *[WeightedAverage(...) for metal in metals],
       Number("extra_calc", "..."),
   ])

The ``*`` unpacks a list. **Why use it?**

.. code-block:: python

   # Without *:
   my_list = [calc1, calc2, calc3]
   CalcSet([my_list, calc4])
   # Result: [[calc1, calc2, calc3], calc4]  ← nested list, wrong!
   
   # With *:
   my_list = [calc1, calc2, calc3]
   CalcSet([*my_list, calc4])
   # Result: [calc1, calc2, calc3, calc4]  ← flat list, correct!

**Think of it as:** "Unpack this list and put each item directly here"

Pattern 3: Named Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Functions in Pollywog often use named parameters:

.. code-block:: python

   Number(
       name="Au_clean",
       expression="clamp([Au], 0)",
       comment_equation="Remove negatives"
   )

**Why use names?**

- Makes code more readable
- You can put parameters in any order
- You can skip optional parameters

You can also use positional parameters for common cases:

.. code-block:: python

   # Positional (shorter):
   Number("Au_clean", "clamp([Au], 0)")
   
   # Named (clearer):
   Number(name="Au_clean", expression="clamp([Au], 0)")

Both are correct—use whichever feels clearer to you.

Common Mistakes and How to Fix Them
------------------------------------

Everyone makes mistakes when learning. Here are the most common ones and how to fix them.

Mistake 1: Forgetting Square Brackets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   Number("result", "Au * 2")

**Problem:** In Leapfrog expressions, variable references need square brackets.

**Fix:**

.. code-block:: python

   Number("result", "[Au] * 2")

Mistake 2: Quote Confusion
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   Category("type", [If("[Au] > 0.5", "ore", "waste")])

**Problem:** Category values (like "ore") need to be quoted in the Leapfrog expression, which means quotes inside quotes.

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

Mistake 4: Missing Commas
~~~~~~~~~~~~~~~~~~~~~~~~~

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

Mistake 5: Wrong Calculation Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: python

   Number("type", [If("[Au] > 0.5", "'ore'", "'waste'")])

**Problem:** Numbers can't hold text values like "ore" or "waste".

**Fix:**

.. code-block:: python

   Category("type", [If("[Au] > 0.5", "'ore'", "'waste'")])

**Rule:** Use ``Number`` for numeric results, ``Category`` for text results.

Tips for Success
-----------------

1. **Start small:** Begin with 2-3 calculations and get comfortable before tackling complex workflows
2. **Test frequently:** Export and test in Leapfrog often to catch issues early
3. **Use comments:** Add ``comment_equation`` to document your logic—your future self will thank you
4. **Copy examples:** There's no shame in copying working code and modifying it
5. **Build a library:** Save your successful scripts for reuse on future projects
6. **Ask for help:** If you're stuck, don't hesitate to ask Python-savvy colleagues or check the documentation

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

On Your Computer
~~~~~~~~~~~~~~~~

If you install Python and Pollywog locally (see :doc:`getting_started`), you can:

- Save notebooks and scripts directly to your file system
- Use version control (Git) to track changes
- Integrate with your company's data management systems

Next Steps
----------

Now that you understand the basics:

**Practice Projects:**

1. Recreate a simple calculation set from one of your Leapfrog projects
2. Build a domain-weighted composite for your most common metals
3. Create a classification system for your typical ore types

**Learn More:**

- :doc:`getting_started` - Installing Pollywog on your computer
- :doc:`tutorials` - More detailed workflow examples
- :doc:`expression_syntax` - Complete guide to Leapfrog expression syntax
- :doc:`helpers_guide` - All available helper functions
- :doc:`workflow_patterns` - Common patterns for different scenarios

**Advanced Topics** (for later):

- Converting Excel formulas to Pollywog
- Building calculation templates for your company
- Integrating machine learning models (yes, really!)
- Automating entire estimation workflows

Getting Help
------------

If you get stuck:

1. **Check the examples:** The ``examples/`` folder in the GitHub repository has working notebooks
2. **Read the documentation:** https://pollywog.readthedocs.io
3. **Search for similar issues:** https://github.com/endarthur/pollywog/issues
4. **Ask questions:** Open a new issue on GitHub with your question

Remember: Everyone starts somewhere, and the Pollywog community is friendly and helpful. Don't be afraid to ask questions!

Final Thoughts
--------------

Learning Python and Pollywog might feel challenging at first, but remember:

- You already understand the concepts (you use Leapfrog's calculator!)
- You're just learning a new way to express the same ideas
- The time investment pays off quickly—often after just one project
- Every resource geologist who learns this says: "I wish I'd learned it sooner"

You've got this! Start with simple examples, build confidence, and gradually tackle more complex workflows. Before you know it, you'll be automating calculations that used to take hours.

Happy modeling! 🪨✨
