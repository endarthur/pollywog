"""
Script to generate diagrams for pollywog documentation.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set style
plt.style.use('default')

def create_workflow_diagram():
    """Create a high-level workflow diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Define boxes
    boxes = [
        {"x": 0.5, "y": 3, "width": 1.5, "height": 1, "text": "Python\nScript", "color": "#e3f2fd"},
        {"x": 2.5, "y": 3, "width": 1.5, "height": 1, "text": "pollywog\nCalcSet", "color": "#fff3e0"},
        {"x": 4.5, "y": 3, "width": 1.5, "height": 1, "text": ".lfcalc\nFile", "color": "#f3e5f5"},
        {"x": 6.5, "y": 3, "width": 1.5, "height": 1, "text": "Leapfrog", "color": "#e8f5e9"},
        {"x": 8.5, "y": 3, "width": 1.5, "height": 1, "text": "Results", "color": "#e0f2f1"},
    ]
    
    # Draw boxes
    for box in boxes:
        fancy_box = FancyBboxPatch(
            (box["x"], box["y"]), box["width"], box["height"],
            boxstyle="round,pad=0.1", 
            edgecolor='#333', facecolor=box["color"], 
            linewidth=2
        )
        ax.add_patch(fancy_box)
        ax.text(box["x"] + box["width"]/2, box["y"] + box["height"]/2, 
                box["text"], ha='center', va='center', fontsize=11, weight='bold')
    
    # Draw arrows
    arrows = [
        (2, 3.5, 2.5, 3.5),
        (4, 3.5, 4.5, 3.5),
        (6, 3.5, 6.5, 3.5),
        (8, 3.5, 8.5, 3.5),
    ]
    
    for x1, y1, x2, y2 in arrows:
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle='->', mutation_scale=20, 
            linewidth=2, color='#666'
        )
        ax.add_patch(arrow)
    
    # Add labels under arrows
    labels = [
        (2.25, 2.6, "build"),
        (4.25, 2.6, "export"),
        (6.25, 2.6, "import"),
        (8.25, 2.6, "run"),
    ]
    
    for x, y, text in labels:
        ax.text(x, y, text, ha='center', va='top', fontsize=9, style='italic', color='#666')
    
    plt.title("Pollywog Workflow", fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('/home/runner/work/pollywog/pollywog/docs/_static/workflow_diagram.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def create_estimation_workflow():
    """Create resource estimation workflow diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define boxes
    boxes = [
        {"x": 3, "y": 8.5, "width": 4, "height": 0.8, "text": "Raw Drillhole Data", "color": "#ffccbc"},
        {"x": 3, "y": 7, "width": 4, "height": 0.8, "text": "Preprocessing\n(clamp, transform)", "color": "#b3e5fc"},
        {"x": 3, "y": 5.5, "width": 4, "height": 0.8, "text": "Estimation in Leapfrog\n(kriging, IDW, etc.)", "color": "#c5e1a5"},
        {"x": 3, "y": 4, "width": 4, "height": 0.8, "text": "Postprocessing\n(back-transform, dilution)", "color": "#b3e5fc"},
        {"x": 3, "y": 2.5, "width": 4, "height": 0.8, "text": "Domain Weighting", "color": "#b3e5fc"},
        {"x": 3, "y": 1, "width": 4, "height": 0.8, "text": "Final Block Model", "color": "#a5d6a7"},
    ]
    
    # Draw boxes
    for box in boxes:
        fancy_box = FancyBboxPatch(
            (box["x"], box["y"]), box["width"], box["height"],
            boxstyle="round,pad=0.05", 
            edgecolor='#333', facecolor=box["color"], 
            linewidth=2
        )
        ax.add_patch(fancy_box)
        ax.text(box["x"] + box["width"]/2, box["y"] + box["height"]/2, 
                box["text"], ha='center', va='center', fontsize=10, weight='bold')
    
    # Draw arrows
    arrows = [
        (5, 8.5, 5, 7.8),
        (5, 7, 5, 6.3),
        (5, 5.5, 5, 4.8),
        (5, 4, 5, 3.3),
        (5, 2.5, 5, 1.8),
    ]
    
    for x1, y1, x2, y2 in arrows:
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle='->', mutation_scale=20, 
            linewidth=2, color='#666'
        )
        ax.add_patch(arrow)
    
    # Add side labels
    side_labels = [
        (1.5, 7.4, "pollywog", "#1976d2"),
        (1.5, 5.9, "Leapfrog", "#388e3c"),
        (1.5, 4.4, "pollywog", "#1976d2"),
        (1.5, 2.9, "pollywog", "#1976d2"),
    ]
    
    for x, y, text, color in side_labels:
        ax.text(x, y, text, ha='center', va='center', 
                fontsize=9, style='italic', color=color, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, linewidth=1.5))
    
    plt.title("Resource Estimation Workflow", fontsize=14, weight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('/home/runner/work/pollywog/pollywog/docs/_static/estimation_workflow.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def create_helper_decision_tree():
    """Create helper function decision tree."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Root question
    ax.text(6, 9, "What do you need to do?", ha='center', va='center', 
            fontsize=12, weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff9c4', edgecolor='#f57c00', linewidth=2))
    
    # Level 1 options
    level1 = [
        {"x": 2, "y": 7.5, "text": "Combine\nvalues", "color": "#e1f5fe"},
        {"x": 6, "y": 7.5, "text": "Transform\nvalues", "color": "#f3e5f5"},
        {"x": 10, "y": 7.5, "text": "Categorize", "color": "#fff3e0"},
    ]
    
    for box in level1:
        fancy_box = FancyBboxPatch(
            (box["x"]-0.7, box["y"]-0.3), 1.4, 0.6,
            boxstyle="round,pad=0.1", 
            edgecolor='#333', facecolor=box["color"], 
            linewidth=1.5
        )
        ax.add_patch(fancy_box)
        ax.text(box["x"], box["y"], box["text"], ha='center', va='center', 
                fontsize=9, weight='bold')
    
    # Arrows from root
    for box in level1:
        arrow = FancyArrowPatch(
            (6, 8.7), (box["x"], box["y"]+0.3),
            arrowstyle='->', mutation_scale=15, 
            linewidth=1.5, color='#666'
        )
        ax.add_patch(arrow)
    
    # Level 2 - Combine
    combine_helpers = [
        {"x": 0.8, "y": 6, "text": "Sum", "desc": "Add values"},
        {"x": 2, "y": 6, "text": "Product", "desc": "Multiply values"},
        {"x": 3.2, "y": 6, "text": "Average", "desc": "Mean of values"},
        {"x": 2, "y": 4.8, "text": "WeightedAverage", "desc": "Weighted mean"},
    ]
    
    # Level 2 - Transform
    transform_helpers = [
        {"x": 5, "y": 6, "text": "Scale", "desc": "Multiply by factor"},
        {"x": 7, "y": 6, "text": "Normalize", "desc": "Scale to sum=1"},
    ]
    
    # Level 2 - Categorize
    categorize_helpers = [
        {"x": 10, "y": 6, "text": "CategoryFromThresholds", "desc": "Threshold-based"},
    ]
    
    # Draw all helper boxes
    all_helpers = combine_helpers + transform_helpers + categorize_helpers
    for helper in all_helpers:
        fancy_box = FancyBboxPatch(
            (helper["x"]-0.6, helper["y"]-0.25), 1.2, 0.5,
            boxstyle="round,pad=0.05", 
            edgecolor='#2196f3', facecolor='#e3f2fd', 
            linewidth=1.5
        )
        ax.add_patch(fancy_box)
        ax.text(helper["x"], helper["y"], helper["text"], ha='center', va='center', 
                fontsize=8, weight='bold')
        ax.text(helper["x"], helper["y"]-0.5, helper["desc"], ha='center', va='top', 
                fontsize=7, style='italic', color='#666')
    
    # Connect level 1 to level 2
    connections = [
        (2, 7.2, 2, 6.25),
        (6, 7.2, 6, 6.25),
        (10, 7.2, 10, 6.25),
    ]
    
    for x1, y1, x2, y2 in connections:
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle='->', mutation_scale=12, 
            linewidth=1.2, color='#999'
        )
        ax.add_patch(arrow)
    
    # Add note
    ax.text(6, 0.5, "Note: For complex logic, use manual Number() or Category() expressions", 
            ha='center', va='center', fontsize=9, style='italic', color='#666',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffde7', edgecolor='#fbc02d'))
    
    plt.title("Helper Function Decision Tree", fontsize=14, weight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('/home/runner/work/pollywog/pollywog/docs/_static/helper_decision_tree.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


def create_architecture_diagram():
    """Create architecture/component diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Main components
    components = [
        {"x": 1, "y": 7, "width": 3, "height": 1.5, "text": "Core Classes\nCalcSet, Number,\nCategory, If, Filter", "color": "#e3f2fd"},
        {"x": 6, "y": 7, "width": 3, "height": 1.5, "text": "Helper Functions\nSum, Product,\nWeightedAverage", "color": "#fff3e0"},
        {"x": 1, "y": 4.5, "width": 3, "height": 1.5, "text": "I/O\nread_lfcalc()\nto_lfcalc()", "color": "#f3e5f5"},
        {"x": 6, "y": 4.5, "width": 3, "height": 1.5, "text": "ML Conversion\nscikit-learn\nintegration", "color": "#e8f5e9"},
        {"x": 3.5, "y": 2, "width": 3, "height": 1.5, "text": "Display & Query\nJupyter integration\nDataFrame-like queries", "color": "#fce4ec"},
    ]
    
    for comp in components:
        fancy_box = FancyBboxPatch(
            (comp["x"], comp["y"]), comp["width"], comp["height"],
            boxstyle="round,pad=0.1", 
            edgecolor='#333', facecolor=comp["color"], 
            linewidth=2
        )
        ax.add_patch(fancy_box)
        ax.text(comp["x"] + comp["width"]/2, comp["y"] + comp["height"]/2, 
                comp["text"], ha='center', va='center', fontsize=9, weight='bold')
    
    # User layer
    user_box = FancyBboxPatch(
        (3, 9), 4, 0.8,
        boxstyle="round,pad=0.1", 
        edgecolor='#1976d2', facecolor='#bbdefb', 
        linewidth=2.5
    )
    ax.add_patch(user_box)
    ax.text(5, 9.4, "Python User Script", ha='center', va='center', fontsize=11, weight='bold')
    
    # Leapfrog layer
    lf_box = FancyBboxPatch(
        (3, 0.2), 4, 0.8,
        boxstyle="round,pad=0.1", 
        edgecolor='#388e3c', facecolor='#c8e6c9', 
        linewidth=2.5
    )
    ax.add_patch(lf_box)
    ax.text(5, 0.6, "Leapfrog Software", ha='center', va='center', fontsize=11, weight='bold')
    
    # Arrows showing flow
    arrows = [
        (5, 9, 5, 8.5),
        (5, 3.5, 5, 1),
    ]
    
    for x1, y1, x2, y2 in arrows:
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle='<->', mutation_scale=20, 
            linewidth=2, color='#666'
        )
        ax.add_patch(arrow)
    
    plt.title("Pollywog Architecture", fontsize=14, weight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('/home/runner/work/pollywog/pollywog/docs/_static/architecture_diagram.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


if __name__ == "__main__":
    print("Generating workflow diagram...")
    create_workflow_diagram()
    print("✓ Generated workflow_diagram.png")
    
    print("Generating estimation workflow...")
    create_estimation_workflow()
    print("✓ Generated estimation_workflow.png")
    
    print("Generating helper decision tree...")
    create_helper_decision_tree()
    print("✓ Generated helper_decision_tree.png")
    
    print("Generating architecture diagram...")
    create_architecture_diagram()
    print("✓ Generated architecture_diagram.png")
    
    print("\nAll diagrams generated successfully!")
