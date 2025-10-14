from .core import If, IfRow, Number, Category
from .utils import ensure_variables


def Sum(*variables, name=None, comment=None):
    """
    Create a Number representing the sum of the given variables.

    This helper function generates a calculation that adds multiple variables together.

    Args:
        *variables: Variable names (as strings) to sum, e.g. "Au", "Ag", 
            or a single list of variable names as strings.
        name (str, optional): Name for the output variable. 
            If None, defaults to "sum_<var1>_<var2>_...". Defaults to None.
        comment (str, optional): Optional comment for the calculation. 
            If None, generates a default comment. Defaults to None.

    Returns:
        Number: A pollywog Number representing the sum calculation.

    Raises:
        ValueError: If no variables are provided.

    Example:
        >>> from pollywog.helpers import Sum
        >>> Sum("Au", "Ag", name="total_precious")
        >>> Sum(["Au", "Ag", "Cu"], name="total_metals")
    """
    if not variables:
        raise ValueError("At least one variable must be provided.")
    if len(variables) == 1 and isinstance(variables[0], (list, tuple)):
        variables = variables[0]
    if name is None:
        name = "sum_" + "_".join(variables)
    expr = f"({' + '.join(f'[{v}]' for v in variables)})"
    return Number(
        name, [expr], comment_equation=comment or f"Sum of {', '.join(variables)}"
    )


def Product(*variables, name=None, comment=None):
    """
    Create a Number representing the product of the given variables.

    This helper function generates a calculation that multiplies multiple variables together.

    Args:
        *variables: Variable names (as strings) to multiply, e.g. "Au", "Ag", 
            or a single list of variable names as strings.
        name (str, optional): Name for the output variable. 
            If None, defaults to "prod_<var1>_<var2>_...". Defaults to None.
        comment (str, optional): Optional comment for the calculation. 
            If None, generates a default comment. Defaults to None.

    Returns:
        Number: A pollywog Number representing the product calculation.

    Raises:
        ValueError: If no variables are provided.

    Example:
        >>> from pollywog.helpers import Product
        >>> Product("grade", "tonnage", name="metal_content")
        >>> Product(["Au", "recovery", "price"], name="revenue")
    """
    if not variables:
        raise ValueError("At least one variable must be provided.")
    if len(variables) == 1 and isinstance(variables[0], (list, tuple)):
        variables = variables[0]
    if name is None:
        name = "prod_" + "_".join(variables)
    expr = f"({' * '.join(f'[{v}]' for v in variables)})"
    return Number(
        name, [expr], comment_equation=comment or f"Product of {', '.join(variables)}"
    )


def Normalize(variable, min_value, max_value, name=None, comment=None):
    """
    Create a Number that normalizes a variable to the range [0, 1].

    This helper function applies min-max normalization, mapping values from the 
    original range [min_value, max_value] to [0, 1].

    Args:
        variable (str): Variable name to normalize.
        min_value (float): Minimum value for normalization (maps to 0).
        max_value (float): Maximum value for normalization (maps to 1).
        name (str, optional): Name for the output variable. 
            If None, defaults to "norm_<variable>". Defaults to None.
        comment (str, optional): Optional comment for the calculation. 
            If None, generates a default comment. Defaults to None.

    Returns:
        Number: A pollywog Number representing the normalization calculation.

    Example:
        >>> from pollywog.helpers import Normalize
        >>> Normalize("Au", 0, 10, name="Au_normalized")
        >>> Normalize("porosity", 0.1, 0.3, name="porosity_norm")
    """
    if name is None:
        name = f"norm_{variable}"
    expr = f"([{variable}] - {min_value}) / ({max_value} - {min_value})"
    return Number(
        name,
        [expr],
        comment_equation=comment
        or f"Normalize {variable} to [0, 1] using min={min_value}, max={max_value}",
    )


def Average(*variables, name=None, comment=None):
    """
    Create a Number representing the arithmetic mean of the given variables.

    This helper function generates a calculation that computes the average
    (arithmetic mean) of multiple variables.

    Args:
        *variables: Variable names (as strings) to average, e.g. "Au", "Ag", 
            or a single list of variable names as strings.
        name (str, optional): Name for the output variable. 
            If None, defaults to "avg_<var1>_<var2>_...". Defaults to None.
        comment (str, optional): Optional comment for the calculation. 
            If None, generates a default comment. Defaults to None.

    Returns:
        Number: A pollywog Number representing the average calculation.

    Raises:
        ValueError: If no variables are provided.

    Example:
        >>> from pollywog.helpers import Average
        >>> Average("Au_est1", "Au_est2", "Au_est3", name="Au_avg")
        >>> Average(["density_dry", "density_wet"], name="density_mean")
    """
    if not variables:
        raise ValueError("At least one variable must be provided.")
    if len(variables) == 1 and isinstance(variables[0], list):
        variables = variables[0]
    if name is None:
        name = "avg_" + "_".join(variables)
    expr = f"({' + '.join(f'[{v}]' for v in variables)}) / {len(variables)}"
    return Number(
        name, [expr], comment_equation=comment or f"Average of {', '.join(variables)}"
    )


def WeightedAverage(variables, weights, name=None, comment=None):
    """
    Create a Number representing the weighted average of variables.

    This helper function computes a weighted average where each variable is 
    multiplied by its corresponding weight before averaging.

    Args:
        variables (list of str): Variable names to average, e.g. ["Au", "Ag", "Cu"].
        weights (list of float or str): Corresponding weights for each variable. 
            Can be constant values (e.g. [0.5, 0.3, 0.2]) or variable names 
            (e.g. ["weight_Au", "weight_Ag", "weight_Cu"]).
        name (str, optional): Name for the output variable. 
            If None, defaults to "wavg_<var1>_<var2>_...". Defaults to None.
        comment (str, optional): Optional comment for the calculation. 
            If None, generates a default comment. Defaults to None.

    Returns:
        Number: A pollywog Number representing the weighted average calculation.

    Raises:
        ValueError: If variables and weights are empty or have different lengths.

    Example:
        >>> from pollywog.helpers import WeightedAverage
        >>> WeightedAverage(["Au_oxide", "Au_sulfide"], [0.7, 0.3], name="Au_composite")
        >>> WeightedAverage(["est1", "est2"], ["weight1", "weight2"], name="weighted_est")
    """
    if not variables or not weights or len(variables) != len(weights):
        raise ValueError("variables and weights must be non-empty and of equal length.")
    if name is None:
        name = "wavg_" + "_".join(variables)
    weights = ensure_variables(weights)
    sum_weights = " + ".join(weights)
    weighted_terms = [f"[{v}] * {w}" for v, w in zip(variables, weights)]
    expr = f"({' + '.join(weighted_terms)}) / ({sum_weights})"
    return Number(
        name,
        [expr],
        comment_equation=comment
        or f"Weighted average of {', '.join(variables)} with weights {weights}",
    )


def Scale(variable, factor, name=None, comment=None):
    """
    Create a Number that multiplies a variable by a scaling factor.

    This helper function generates a simple multiplication calculation, useful
    for unit conversions or applying constant scaling factors.

    Args:
        variable (str): Variable name to scale.
        factor (float or str): Scaling factor. Can be a numeric constant 
            (e.g. 2.5) or another variable name (e.g. "scale_factor").
        name (str, optional): Name for the output variable. 
            If None, defaults to "scale_<variable>". Defaults to None.
        comment (str, optional): Optional comment for the calculation. 
            If None, generates a default comment. Defaults to None.

    Returns:
        Number: A pollywog Number representing the scaled variable.

    Example:
        >>> from pollywog.helpers import Scale
        >>> Scale("Au_ppm", 0.001, name="Au_percent")  # Convert ppm to percent
        >>> Scale("tonnes", 2204.62, name="pounds")  # Convert tonnes to pounds
        >>> Scale("grade", "dilution_factor", name="diluted_grade")
    """
    if name is None:
        name = f"scale_{variable}"
    factor_expr = f"[{factor}]" if isinstance(factor, str) else str(factor)
    expr = f"[{variable}] * {factor_expr}"
    return Number(
        name, [expr], comment_equation=comment or f"Scale {variable} by {factor}"
    )


def CategoryFromThresholds(variable, thresholds, categories, name=None, comment=None):
    """
    Create a Category that assigns labels based on value thresholds.

    This helper function generates conditional logic to classify a numeric variable
    into categories based on threshold boundaries.

    Args:
        variable (str): Variable to classify.
        thresholds (list of float): Threshold values in ascending order. 
            These define the boundaries between categories.
        categories (list of str): Category labels. Must have exactly one more 
            element than thresholds (one category for each range).
        name (str, optional): Name for the output category. 
            If None, defaults to "class_<variable>". Defaults to None.
        comment (str, optional): Optional comment for the calculation. 
            If None, generates a default comment. Defaults to None.

    Returns:
        Category: A pollywog Category with conditional logic for threshold-based classification.

    Raises:
        ValueError: If len(categories) != len(thresholds) + 1.

    Example:
        >>> from pollywog.helpers import CategoryFromThresholds
        >>> CategoryFromThresholds(
        ...     "Au", 
        ...     [0.5, 1.0, 2.0], 
        ...     ["Waste", "Low Grade", "Medium Grade", "High Grade"],
        ...     name="ore_class"
        ... )
        # This creates: 
        #   Au <= 0.5 -> "Waste"
        #   0.5 < Au <= 1.0 -> "Low Grade"
        #   1.0 < Au <= 2.0 -> "Medium Grade"
        #   Au > 2.0 -> "High Grade"
    """
    if len(categories) != len(thresholds) + 1:
        raise ValueError("categories must have one more element than thresholds")
    rows = []
    prev = None
    for i, threshold in enumerate(thresholds):
        if prev is None:
            cond = f"[{variable}] <= {threshold}"
        else:
            cond = f"([{variable}] > {prev}) and ([{variable}] <= {threshold})"
        rows.append(([cond], [categories[i]]))
        prev = threshold
    # Otherwise case
    otherwise = [categories[-1]]
    if_block = If([IfRow(cond, val) for cond, val in rows], otherwise=otherwise)
    if name is None:
        name = f"class_{variable}"
    return Category(
        name,
        [if_block],
        comment_equation=comment or f"Classify {variable} by thresholds {thresholds}",
    )
