import copy
from pollywog.core import CalcSet, If, IfRow
import re


import math
import numpy as np


# Leapfrog-like math functions
def log(n, base=10):
    """
    Compute logarithm of n with the specified base.
    
    Args:
        n (float): The value to compute the logarithm of.
        base (float, optional): The logarithm base. Defaults to 10.
    
    Returns:
        float: The logarithm of n with the specified base.
    """
    return math.log(n, base)


def ln(n):
    """
    Compute natural logarithm (base e) of n.
    
    Args:
        n (float): The value to compute the natural logarithm of.
    
    Returns:
        float: The natural logarithm of n.
    """
    return math.log(n)


def exp(n):
    """
    Compute the exponential function e^n.
    
    Args:
        n (float): The exponent value.
    
    Returns:
        float: e raised to the power of n.
    """
    return math.exp(n)


def sqrt(n):
    """
    Compute the square root of n.
    
    Args:
        n (float): The value to compute the square root of.
    
    Returns:
        float: The square root of n.
    """
    return math.sqrt(n)


def abs_(n):
    """
    Compute the absolute value of n.
    
    Args:
        n (float): The value to compute the absolute value of.
    
    Returns:
        float: The absolute value of n.
    """
    import builtins
    return builtins.abs(n)


# Trigonometric functions
def sin(x):
    """
    Compute the sine of x (in radians).
    
    Args:
        x (float): Angle in radians.
    
    Returns:
        float: The sine of x.
    """
    return math.sin(x)


def cos(x):
    """
    Compute the cosine of x (in radians).
    
    Args:
        x (float): Angle in radians.
    
    Returns:
        float: The cosine of x.
    """
    return math.cos(x)


def tan(x):
    """
    Compute the tangent of x (in radians).
    
    Args:
        x (float): Angle in radians.
    
    Returns:
        float: The tangent of x.
    """
    return math.tan(x)


def asin(x):
    """
    Compute the arcsine (inverse sine) of x.
    
    Args:
        x (float): Value between -1 and 1.
    
    Returns:
        float: The arcsine of x in radians.
    """
    return math.asin(x)


def acos(x):
    """
    Compute the arccosine (inverse cosine) of x.
    
    Args:
        x (float): Value between -1 and 1.
    
    Returns:
        float: The arccosine of x in radians.
    """
    return math.acos(x)


def atan(x):
    """
    Compute the arctangent (inverse tangent) of x.
    
    Args:
        x (float): Any real number.
    
    Returns:
        float: The arctangent of x in radians.
    """
    return math.atan(x)


# Limits and rounding
def min_(*args):
    """
    Return the minimum value from the given arguments.
    
    Args:
        *args: Variable number of values to compare.
    
    Returns:
        The minimum value among the arguments.
    """
    import builtins
    return builtins.min(args)


def max_(*args):
    """
    Return the maximum value from the given arguments.
    
    Args:
        *args: Variable number of values to compare.
    
    Returns:
        The maximum value among the arguments.
    """
    import builtins
    return builtins.max(args)


def clamp(n, lower, upper=None):
    """
    Clamp a value between lower and upper bounds.
    
    If only lower is provided, returns max(n, lower).
    If both lower and upper are provided, returns a value between lower and upper.
    
    Args:
        n (float): The value to clamp.
        lower (float): The lower bound.
        upper (float, optional): The upper bound. If None, only lower bound is enforced.
    
    Returns:
        float: The clamped value.
    """
    if upper is not None:
        return max(lower, min(n, upper))
    return max(n, lower)


def round_(n, dp=None):
    """
    Round a number to a specified number of decimal places.
    
    Args:
        n (float): The number to round.
        dp (int, optional): Number of decimal places. If None, rounds to nearest integer.
    
    Returns:
        float: The rounded value.
    """
    if dp is not None:
        return round(n, dp)
    return round(n)


def roundsf(n, sf):
    """
    Round a number to a specified number of significant figures.
    
    Args:
        n (float): The number to round.
        sf (int): Number of significant figures.
    
    Returns:
        float: The number rounded to the specified significant figures.
    """
    if n == 0:
        return 0
    from math import log10, floor
    import builtins

    return builtins.round(n, -int(floor(log10(abs_(n)))) + (sf - 1))


def floor_(n):
    """
    Return the floor of n (largest integer less than or equal to n).
    
    Args:
        n (float): The value to floor.
    
    Returns:
        float: The floor of n.
    """
    return math.floor(n)


def ceiling(n):
    """
    Return the ceiling of n (smallest integer greater than or equal to n).
    
    Args:
        n (float): The value to ceiling.
    
    Returns:
        float: The ceiling of n.
    """
    return math.ceil(n)


def truncate(n):
    """
    Truncate n to an integer by removing the decimal part.
    
    Args:
        n (float): The value to truncate.
    
    Returns:
        int: The integer part of n.
    """
    return int(n)


# Text functions
def concat(*args):
    """
    Concatenate multiple values into a single string.
    
    Args:
        *args: Variable number of values to concatenate.
    
    Returns:
        str: The concatenated string.
    """
    return "".join(str(a) for a in args)


def startswith(t, prefix):
    """
    Check if text starts with the specified prefix.
    
    Args:
        t: The text to check (converted to string).
        prefix (str): The prefix to check for.
    
    Returns:
        bool: True if text starts with prefix, False otherwise.
    """
    return str(t).startswith(prefix)


def endswith(t, suffix):
    """
    Check if text ends with the specified suffix.
    
    Args:
        t: The text to check (converted to string).
        suffix (str): The suffix to check for.
    
    Returns:
        bool: True if text ends with suffix, False otherwise.
    """
    return str(t).endswith(suffix)


def contains(t, part):
    """
    Check if text contains the specified substring.
    
    Args:
        t: The text to check (converted to string).
        part (str): The substring to check for.
    
    Returns:
        bool: True if text contains part, False otherwise.
    """
    return part in str(t)


def like(t, pattern):
    """
    Check if text matches a regular expression pattern.
    
    Args:
        t: The text to check (converted to string).
        pattern (str): The regular expression pattern.
    
    Returns:
        bool: True if pattern matches anywhere in text, False otherwise.
    """
    import re

    return re.search(pattern, str(t)) is not None


def regexp(t, pattern):
    """
    Check if text matches a regular expression pattern (alias for like).
    
    Args:
        t: The text to check (converted to string).
        pattern (str): The regular expression pattern.
    
    Returns:
        bool: True if pattern matches anywhere in text, False otherwise.
    """
    import re

    return re.search(pattern, str(t)) is not None


def min(*args):
    """
    Wrapper for min_ to match Leapfrog function naming.
    
    Args:
        *args: Variable number of values to compare.
    
    Returns:
        The minimum value among the arguments.
    """
    return min_(*args)


def max(*args):
    """
    Wrapper for max_ to match Leapfrog function naming.
    
    Args:
        *args: Variable number of values to compare.
    
    Returns:
        The maximum value among the arguments.
    """
    return max_(*args)


def round(n, dp=None):
    """
    Wrapper for round_ to match Leapfrog function naming.
    
    Args:
        n (float): The number to round.
        dp (int, optional): Number of decimal places. If None, rounds to nearest integer.
    
    Returns:
        float: The rounded value.
    """
    return round_(n, dp)


def floor(n):
    """
    Wrapper for floor_ to match Leapfrog function naming.
    
    Args:
        n (float): The value to floor.
    
    Returns:
        float: The floor of n.
    """
    return floor_(n)


def abs(n):
    """
    Wrapper for abs_ to match Leapfrog function naming.
    
    Args:
        n (float): The value to compute the absolute value of.
    
    Returns:
        float: The absolute value of n.
    """
    return abs_(n)


def is_normal(n):
    """
    Check if a value is a normal (valid) number.
    
    Returns True for finite numbers (int, float), False for None, NaN, or infinity.
    Treats anything that isn't a normal number as NaN for run.py purposes.
    
    Args:
        n: The value to check.
    
    Returns:
        bool: True if n is a finite number, False otherwise.
    
    Example:
        >>> is_normal(5.0)
        True
        >>> is_normal(None)
        False
        >>> is_normal(float('nan'))
        False
        >>> is_normal(float('inf'))
        False
    """
    if n is None:
        return False
    try:
        import math
        # Check if it's a number and is finite (not NaN, not inf)
        return isinstance(n, (int, float)) and math.isfinite(n)
    except (TypeError, ValueError):
        return False


LEAPFROG_ENV = {
    "log": log,
    "ln": ln,
    "exp": exp,
    "sqrt": sqrt,
    "abs": abs,
    "pi": math.pi,
    "e": math.e,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "min": min_,
    "max": max_,
    "clamp": clamp,
    "round": round_,
    "roundsf": roundsf,
    "floor": floor_,
    "ceiling": ceiling,
    "truncate": truncate,
    "concat": concat,
    "startswith": startswith,
    "endswith": endswith,
    "contains": contains,
    "like": like,
    "regexp": regexp,
    "is_normal": is_normal,
}


def run_calcset(
    calcset, inputs=None, dataframe=None, assign_results=True, output_variables=False
):
    """
    Evaluate a CalcSet with external inputs or a pandas DataFrame.
    
    This function executes a calculation set using either a dictionary of input values
    or a pandas DataFrame. When using a DataFrame, calculations are applied row-by-row.
    
    Args:
        calcset (CalcSet): The calculation set to evaluate.
        inputs (dict, optional): Dictionary of input variable values for single evaluation.
        dataframe (pd.DataFrame, optional): DataFrame for row-by-row evaluation.
        assign_results (bool): Whether to assign results to output. Defaults to True.
        output_variables (bool): Whether to include variables in output. 
            Defaults to False (Leapfrog-like behavior: only calculations, categories, and filters).
    
    Returns:
        dict or pd.DataFrame: 
            - If inputs provided: Dictionary of calculation results.
            - If dataframe provided: DataFrame with calculated columns added.
    
    Note:
        pandas is only required when using DataFrame input/output.
    
    Example:
        >>> from pollywog.core import CalcSet, Number
        >>> cs = CalcSet([Number(name="doubled", children=["[x] * 2"])])
        >>> run_calcset(cs, inputs={"x": 5})
        {'doubled': 10}
    """

    # Helper to evaluate an expression or If object
    def eval_expr(expr, context):
        if isinstance(expr, str):
            if not expr.strip():
                return None

            # Replace [var] with context["var"] using regex
            def repl(m):
                var = m.group(1)
                return f"context[{repr(var)}]"

            expr_eval = re.sub(r"\[([^\]]+)\]", repl, expr)
            try:
                # Provide Leapfrog-like environment for eval
                return eval(expr_eval, {"context": context, **LEAPFROG_ENV}, context)
            except Exception:
                return None
        elif isinstance(expr, If):
            for row in expr.rows:
                cond = eval_expr(row.condition[0], context) if row.condition else True
                if cond:
                    return eval_expr(row.value[0], context)
            if expr.otherwise:
                return eval_expr(expr.otherwise[0], context)
            return None
        elif isinstance(expr, IfRow):
            # Should not be evaluated directly, only as part of If
            return None
        else:
            return expr

    # Dependency resolution
    sorted_items = calcset.topological_sort().items

    def run_single(context):
        results = {}
        for item in sorted_items:
            # If item is a Variable, assign its value from context or inputs directly
            if getattr(item, "item_type", None) == "variable":
                results[item.name] = context.get(item.name, None)
                continue
            child_results = []
            for child in item.children:
                child_results.append(eval_expr(child, {**context, **results}))
            results[item.name] = child_results[0] if child_results else None
        # Filter output according to output_variables flag
        item_type_map = {
            item.name: getattr(item, "item_type", None) for item in sorted_items
        }
        if not output_variables:
            return {
                k: v for k, v in results.items() if item_type_map.get(k) != "variable"
            }
        return results

    if dataframe is not None:
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for DataFrame input/output. Please install pandas or use dict inputs."
            )
        df = dataframe.copy()
        for idx, row in df.iterrows():
            context = dict(row)
            results = run_single(context)
            for k, v in results.items():
                df.at[idx, k] = v
        # Remove variable columns if output_variables is False
        if not output_variables:
            variable_names = [
                item.name
                for item in sorted_items
                if getattr(item, "item_type", None) == "variable"
            ]
            df = df.drop(columns=variable_names, errors="ignore")
        return df
    else:
        context = inputs if inputs is not None else {}
        return run_single(context)


# Pandas DataFrame extension accessor
try:
    import pandas as pd

    @pd.api.extensions.register_dataframe_accessor("pw")
    class PollywogAccessor:
        """
        Pandas DataFrame accessor for running pollywog calculations.
        
        This accessor provides a convenient way to run CalcSets on DataFrames
        using the .pw namespace.
        
        Example:
            >>> import pandas as pd
            >>> from pollywog.core import CalcSet, Number
            >>> df = pd.DataFrame({'x': [1, 2, 3]})
            >>> cs = CalcSet([Number(name="doubled", children=["[x] * 2"])])
            >>> result = df.pw.run(cs)
        """
        
        def __init__(self, pandas_obj):
            """
            Initialize the accessor with a DataFrame.
            
            Args:
                pandas_obj (pd.DataFrame): The DataFrame to operate on.
            """
            self._obj = pandas_obj

        def run(self, calcset, assign_results=True):
            """
            Run a CalcSet on this DataFrame, returning a copy with results assigned.
            
            Args:
                calcset (CalcSet): The calculation set to run.
                assign_results (bool): Whether to assign results to output. Defaults to True.
            
            Returns:
                pd.DataFrame: A copy of the DataFrame with calculated columns added.
            """
            return run_calcset(
                calcset, dataframe=self._obj, assign_results=assign_results
            )

except ImportError:
    pass
