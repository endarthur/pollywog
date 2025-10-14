def ensure_list(x) -> list:
    """
    Ensure the input is a list. If not, wrap it in a list.
    
    This is a utility function for normalizing inputs that can be either
    a single value or a list of values.

    Args:
        x (Any): Input value or list.
    
    Returns:
        list: The input as a list. If x was already a list, returns it unchanged.
            If x was not a list, returns [x].
    
    Example:
        >>> ensure_list(5)
        [5]
        >>> ensure_list([1, 2, 3])
        [1, 2, 3]
    """
    if not isinstance(x, list):
        x = [x]
    return x


def ensure_str_list(x):
    """
    Ensure the input is a list with string guards at both ends.
    
    This function is used internally when serializing expressions to ensure
    proper formatting in Leapfrog calculation sets, which require string
    padding in certain contexts.

    Args:
        x (Any): Input value or list.
    
    Returns:
        list: List padded with empty strings at the beginning and/or end if
            the first or last elements are not strings.
    
    Example:
        >>> ensure_str_list([5, 10])
        ['', 5, 10, '']
        >>> ensure_str_list(['hello', 'world'])
        ['hello', 'world']
    """
    if not isinstance(x, list):
        x = [x]
    if isinstance(x, list):
        if not isinstance(x[0], str):
            x = [""] + x
        if not isinstance(x[-1], str):
            x = x + [""]
    return x


def to_dict(items, guard_strings=False):
    """
    Convert items to their dictionary representations for serialization.
    
    This function converts pollywog objects (Items, Expressions, etc.) to
    dictionaries for JSON serialization. Objects with a to_dict() method are
    converted, while other values are passed through unchanged.

    Args:
        items (list or Any): List of items or single item to convert.
        guard_strings (bool): If True, pad the output list with empty strings 
            at the beginning and/or end if the first or last elements are not strings.
            This is required by Leapfrog's .lfcalc format. Defaults to False.
    
    Returns:
        list: List of dictionaries or items, possibly padded with empty strings.
    
    Example:
        >>> from pollywog.core import Number
        >>> num = Number(name="test", children=["5"])
        >>> to_dict(num)
        [{'type': 'calculation', 'name': 'test', ...}]
    """
    out = [
        item.to_dict() if hasattr(item, "to_dict") else item
        for item in ensure_list(items)
    ]
    if guard_strings:
        if not isinstance(out[0], str):
            out = [""] + out
        if not isinstance(out[-1], str):
            out = out + [""]
    return out


def is_number(v):
    """
    Check if a value can be converted to a float (i.e., is numeric).
    
    This function attempts to convert the value to a float. If successful,
    the value is considered a number.

    Args:
        v (Any): Input value to check.
    
    Returns:
        bool: True if the value can be converted to a float, False otherwise.
    
    Example:
        >>> is_number(5)
        True
        >>> is_number("3.14")
        True
        >>> is_number("hello")
        False
    """
    try:
        float(v)
        return True
    except (ValueError, TypeError):
        return False


def ensure_brackets(var):
    """
    Ensure a variable name is wrapped in Leapfrog-style brackets [var].
    
    Variable references in Leapfrog expressions use bracket notation. This
    function ensures a variable name has the proper formatting.

    Args:
        var (str): Variable name, with or without brackets.
    
    Returns:
        str: Variable name wrapped in brackets, e.g., "[Au]".
    
    Example:
        >>> ensure_brackets("Au")
        '[Au]'
        >>> ensure_brackets("[Au]")
        '[Au]'
        >>> ensure_brackets("  grade  ")
        '[grade]'
    """
    var = var.strip()
    if not (var.startswith("[") and var.endswith("]")):
        var = f"[{var}]"
    return var


def ensure_variables(variables):
    """
    Format a list of values as Leapfrog variable references or constants.
    
    This function processes a list of values and formats them appropriately:
    - Numeric values are converted to strings (for use as constants)
    - Non-numeric strings are wrapped in brackets (for variable references)
    
    This is useful when building expressions that may contain a mix of
    variable references and numeric constants.

    Args:
        variables (Any): A single variable or a list of variables to process.
    
    Returns:
        list: A list of formatted strings, either bracketed variable references
            (e.g., "[Au]") or numeric constants (e.g., "0.5").
    
    Example:
        >>> ensure_variables(["Au", 0.5, "Ag"])
        ['[Au]', '0.5', '[Ag]']
        >>> ensure_variables("grade")
        ['[grade]']
    """

    return [
        f"{v}" if is_number(v) else ensure_brackets(v) for v in ensure_list(variables)
    ]
