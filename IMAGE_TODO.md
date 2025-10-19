# Image and Screenshot TODO

This document contains instructions for screenshots, diagrams, and images that should be added to the pollywog documentation to make it more visual and helpful.

## Diagrams and Images Needed

### Placeholders Added in Documentation

The following locations in the RST documentation files have commented placeholders where images should be added. After creating the images, simply uncomment the `.. image::` directive and ensure the filename matches:

1. **docs/index.rst** (lines ~32-44): Two diagram placeholders
   - `workflow_diagram.png` - Basic pollywog workflow (Python → CalcSet → .lfcalc → Leapfrog → Results)
   - `use_cases_diagram.png` - When to use pollywog / value proposition

2. **docs/getting_started.rst**:
   - Line ~196: `leapfrog_import_process.png` - Screenshot of importing .lfcalc into Leapfrog
   - Line ~320: `jupyter_display_example.png` - Interactive CalcSet display in Jupyter

3. **docs/tutorials.rst**:
   - Line ~128: `tutorial_visualization_example.png` - CalcSet visualization example
   - Line ~440: `query_example.png` - Query results showing filtered calculations

## Screenshots and Images to Create

### 1. Leapfrog Import Process
**File**: `docs/_static/leapfrog_import_process.png`

**Steps to capture**:
1. Open Leapfrog
2. Navigate to a block model or drillhole database
3. Right-click on "Evaluations" or "Numeric" section
4. Select "Import" → "From File"
5. Take a screenshot showing this menu and the file browser dialog
6. Highlight the steps with annotations

**Purpose**: Show users exactly how to import .lfcalc files into Leapfrog

---

### 2. Leapfrog Calculation Tree View
**File**: `docs/_static/leapfrog_calculation_tree.png`

**Steps to capture**:
1. After importing a .lfcalc file into Leapfrog
2. Show the calculation tree/hierarchy in the Leapfrog sidebar
3. Show several calculations expanded to show their formulas
4. Take a clean screenshot

**Purpose**: Show what the final result looks like in Leapfrog after importing

---

### 3. Jupyter Notebook Display Example
**File**: `docs/_static/jupyter_display_example.png`

**Steps to capture**:
1. Open a Jupyter notebook
2. Create a CalcSet with several calculations including If statements
3. Run `display_calcset(calcset)` or just display the calcset directly
4. Take a screenshot showing the interactive tree view
5. Make sure to show both collapsed and expanded calculations

**Purpose**: Demonstrate the interactive visualization capabilities

**Example code**:
```python
from pollywog.core import CalcSet, Number, If
from pollywog.helpers import WeightedAverage

calcset = CalcSet([
    Number(name="Au_clean", expression=["clamp([Au], 0)"]),
    WeightedAverage(
        variables=["Au_oxide", "Au_sulfide"],
        weights=["prop_oxide", "prop_sulfide"],
        name="Au_composite"
    ),
    Number(name="recovery", expression=[
        If([
            ("[domain] = 'oxide'", "0.92"),
            ("[domain] = 'sulfide'", "0.78"),
        ], otherwise=["0.85"])
    ]),
])

from pollywog.display import display_calcset
display_calcset(calcset)
```

---

### 4. JupyterLite Web Interface
**File**: `docs/_static/jupyterlite_interface.png`

**Steps to capture**:
1. Go to https://endarthur.github.io/pollyweb
2. Show the interface with a notebook open
3. Highlight the download button feature for .lfcalc files
4. Take a screenshot

**Purpose**: Show users the browser-based option for trying pollywog

---

### 5. Query Results Example
**File**: `docs/_static/query_example.png`

**Steps to capture**:
1. In a Jupyter notebook, create a large CalcSet with many items
2. Show the original calcset
3. Show a query operation: `calcset.query('name.startswith("Au")')`
4. Show the filtered results
5. Capture both in the same screenshot if possible

**Purpose**: Demonstrate the DataFrame-like query functionality

**Example code**:
```python
from pollywog.core import CalcSet, Number

# Create many calculations
calcset = CalcSet([
    Number(name="Au_clean", expression=["clamp([Au], 0)"]),
    Number(name="Au_log", expression=["log([Au_clean] + 0.01)"]),
    Number(name="Ag_clean", expression=["clamp([Ag], 0)"]),
    Number(name="Ag_log", expression=["log([Ag_clean] + 0.01)"]),
    Number(name="Cu_clean", expression=["clamp([Cu], 0)"]),
    Number(name="Cu_log", expression=["log([Cu_clean] + 0.01)"]),
])

print("Original calcset:")
display(calcset)

print("\nFiltered for Au only:")
au_only = calcset.query('name.startswith("Au")')
display(au_only)
```

---

### 6. Before/After Comparison
**File**: `docs/_static/manual_vs_pollywog.png`

**Steps to capture**:
Create a side-by-side comparison showing:

**Left side**: Screenshot of manually creating calculations in Leapfrog UI
- Show the tedious point-and-click interface
- Show formula entry boxes

**Right side**: Show the equivalent Python code in pollywog
- Clean, readable code
- Version controllable
- Automatable

**Purpose**: Highlight the value proposition of pollywog

---

### 7. Complex Calculation Example
**File**: `docs/_static/complex_calculation_tree.png`

**Steps to capture**:
1. Create a complex multi-domain resource model with conditional logic
2. Display it in Jupyter showing the full calculation tree
3. Show dependencies between calculations
4. Capture the full structure

**Purpose**: Demonstrate pollywog's ability to handle complex workflows

---

### 8. Git Integration Example
**File**: `docs/_static/git_version_control.png`

**Steps to capture**:
1. Show a Git repository with pollywog Python scripts
2. Show commit history for calculation scripts
3. Show diffs between versions
4. Demonstrate version control benefits

**Purpose**: Highlight the version control advantage over manual Leapfrog files

---

### 9. Error Handling Example
**File**: `docs/_static/error_handling.png`

**Steps to capture**:
1. Show code with clamp functions to handle edge cases
2. Show conditional logic to avoid division by zero
3. Show epsilon additions for log transforms
4. Annotate the defensive programming patterns

**Purpose**: Teach best practices for robust calculations

---

### 10. Real-World Workflow
**File**: `docs/_static/real_world_workflow.png`

**Steps to capture**:
A flowchart or diagram showing a real mining project workflow:
1. Drillhole data → Python preprocessing script
2. Preprocessed data → Leapfrog estimation
3. Block model → Python postprocessing script
4. Final model → Economic evaluation
5. Results → Reporting/visualization

**Purpose**: Show how pollywog fits into a real mining workflow

---

## Optional Animated GIFs

If you want to create animated demonstrations:

### 1. End-to-End Workflow GIF
**File**: `docs/_static/end_to_end_demo.gif`

Show the complete process:
1. Writing Python code in Jupyter
2. Exporting .lfcalc file
3. Importing into Leapfrog
4. Running calculations
5. Viewing results

---

### 2. Interactive Query GIF
**File**: `docs/_static/interactive_query.gif`

Show:
1. Starting with a large calcset
2. Typing and running different queries
3. Results updating in real-time
4. Filtering by different criteria

---

## Image Creation Tools

For creating diagrams and flowcharts, consider using:
- **Draw.io** (https://app.diagrams.net/) - Free, web-based
- **Excalidraw** (https://excalidraw.com/) - Simple sketching tool
- **Microsoft Visio** - Professional diagramming
- **Lucidchart** - Collaborative diagramming
- **PlantUML** - Text-based diagram generation

For screenshots:
- **Windows**: Snipping Tool or Snip & Sketch
- **macOS**: Cmd+Shift+4 for region capture
- **Linux**: gnome-screenshot or similar
- **Annotation**: Use tools like Greenshot, ShareX, or Skitch to add arrows and labels

## Notes

- All images should be saved as PNG format for best quality
- Recommended resolution: At least 1920x1080 for screenshots
- Use consistent styling (fonts, colors, annotations)
- Add red arrows or boxes to highlight important areas
- Keep file sizes reasonable (compress if needed)
- Use descriptive alt text when adding to documentation
- Consider creating both light and dark mode versions if relevant

## Priority Order

1. **HIGH**: Jupyter Notebook Display Example (#3) - Shows core functionality
2. **HIGH**: Leapfrog Import Process (#1) - Essential for users
3. **MEDIUM**: Query Results Example (#5) - Demonstrates advanced feature
4. **MEDIUM**: Before/After Comparison (#6) - Shows value proposition
5. **LOW**: Everything else - Nice to have for completeness
