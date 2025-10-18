"""
Script to generate diagrams for pollywog documentation.

This creates simple, focused diagrams that are actually helpful for understanding pollywog.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.patches as mpatches

# Set style for clean, professional diagrams
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

def create_workflow_diagram():
    """
    Create a simple, clear workflow diagram showing the basic pollywog flow.
    This is the most essential diagram - showing how pollywog fits into the workflow.
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 3))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 2.5)
    ax.axis('off')
    
    # Define steps with clear spacing
    steps = [
        {"x": 0, "text": "Write Python\nCode", "color": "#2196F3"},
        {"x": 2.5, "text": "Build\nCalcSet", "color": "#FF9800"},
        {"x": 5, "text": "Export\n.lfcalc", "color": "#9C27B0"},
        {"x": 7.5, "text": "Import to\nLeapfrog", "color": "#4CAF50"},
        {"x": 10, "text": "Run\nCalculations", "color": "#00BCD4"},
    ]
    
    # Draw boxes
    for step in steps:
        rect = FancyBboxPatch(
            (step["x"] - 0.6, 0.5), 1.2, 1.2,
            boxstyle="round,pad=0.1",
            edgecolor=step["color"],
            facecolor=step["color"],
            alpha=0.2,
            linewidth=2.5
        )
        ax.add_patch(rect)
        
        # Add text
        ax.text(step["x"], 1.1, step["text"], 
                ha='center', va='center', fontsize=10, weight='bold',
                color=step["color"])
    
    # Draw simple arrows between steps
    for i in range(len(steps) - 1):
        x1 = steps[i]["x"] + 0.65
        x2 = steps[i + 1]["x"] - 0.65
        y = 1.1
        
        # Simple arrow
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', lw=2.5, color='#555'))
    
    # Add title
    ax.text(5, 2.2, "Pollywog Workflow", 
            ha='center', va='center', fontsize=14, weight='bold')
    
    plt.tight_layout(pad=0.5)
    plt.savefig('/home/runner/work/pollywog/pollywog/docs/_static/workflow_diagram.png', 
                dpi=150, bbox_inches='tight', facecolor='white', pad_inches=0.3)
    plt.close()


def create_use_cases_diagram():
    """
    Create a diagram showing the key use cases for pollywog.
    This provides real value by showing WHEN and WHY to use pollywog.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Central pollywog box
    center_x, center_y = 6, 3.5
    pollywog = FancyBboxPatch(
        (center_x - 0.8, center_y - 0.5), 1.6, 1,
        boxstyle="round,pad=0.15",
        edgecolor='#FF9800',
        facecolor='#FF9800',
        alpha=0.2,
        linewidth=3
    )
    ax.add_patch(pollywog)
    ax.text(center_x, center_y, 'pollywog', ha='center', va='center',
            fontsize=14, weight='bold', color='#FF9800')
    
    # Use cases around it
    use_cases = [
        # Top row
        {"pos": (1.5, 6), "text": "Automate\nRepetitive\nCalculations", "color": "#2196F3"},
        {"pos": (6, 6), "text": "Version Control\nYour Workflow", "color": "#4CAF50"},
        {"pos": (10.5, 6), "text": "Deploy ML\nModels", "color": "#9C27B0"},
        # Bottom row
        {"pos": (1.5, 1), "text": "Multi-Domain\nEstimation", "color": "#00BCD4"},
        {"pos": (6, 1), "text": "Complex\nConditional Logic", "color": "#F44336"},
        {"pos": (10.5, 1), "text": "Query & Filter\nCalculations", "color": "#FF5722"},
    ]
    
    for uc in use_cases:
        # Draw box
        x, y = uc["pos"]
        box = FancyBboxPatch(
            (x - 1, y - 0.4), 2, 0.8,
            boxstyle="round,pad=0.08",
            edgecolor=uc["color"],
            facecolor='white',
            linewidth=2
        )
        ax.add_patch(box)
        ax.text(x, y, uc["text"], ha='center', va='center',
                fontsize=9, weight='bold', color=uc["color"])
        
        # Draw connection line to center
        # Calculate connection points
        dx = center_x - x
        dy = center_y - y
        length = (dx**2 + dy**2)**0.5
        
        # Start from edge of use case box towards center
        start_x = x + (dx / length) * 1.0
        start_y = y + (dy / length) * 0.5
        
        # End at edge of center box
        end_x = center_x - (dx / length) * 0.9
        end_y = center_y - (dy / length) * 0.6
        
        ax.plot([start_x, end_x], [start_y, end_y], 
                color=uc["color"], linewidth=1.5, alpha=0.5, linestyle='--')
    
    # Add title
    ax.text(6, 6.7, "When to Use Pollywog", ha='center', va='center',
            fontsize=14, weight='bold')
    
    plt.tight_layout(pad=0.5)
    plt.savefig('/home/runner/work/pollywog/pollywog/docs/_static/use_cases_diagram.png', 
                dpi=150, bbox_inches='tight', facecolor='white', pad_inches=0.3)
    plt.close()





if __name__ == "__main__":
    print("Generating simplified, focused diagrams...")
    print("\nGenerating workflow diagram...")
    create_workflow_diagram()
    print("✓ Generated workflow_diagram.png")
    
    print("\nGenerating use cases diagram...")
    create_use_cases_diagram()
    print("✓ Generated use_cases_diagram.png")
    
    print("\n✓ All diagrams generated successfully!")
    print("\nNote: Only 2 diagrams created - focused on providing real value:")
    print("  1. workflow_diagram.png - Shows HOW pollywog works")
    print("  2. use_cases_diagram.png - Shows WHEN to use pollywog")
