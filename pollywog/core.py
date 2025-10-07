import json
import zlib
import re
from pathlib import Path

from .utils import ensure_list, ensure_str_list, to_dict

HEADER = b"\x25\x6c\x66\x63\x61\x6c\x63\x2d\x31\x2e\x30\x0a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

ITEM_ORDER = {
    "variable": 0,
    "calculation": 1,
    "filter": 2,
}

# TODO: check if items need to be sorted into variables then calculations then filters and do so if needed
# TODO: actually just sorted preemptively when writing to file, will check later if this is an issue
class CalcSet:
    def __init__(self, items):
        """
        Initialize a CalcSet with a list of items.
        Args:
            items (list): List of calculation items (Variable, Number, Category, Filter, etc.)
        """
        self.items = items

    def to_dict(self, sort_items=True):
        """
        Convert the CalcSet to a dictionary representation.
        Args:
            sort_items (bool): Whether to sort items by type.
        Returns:
            dict: Dictionary representation of the calculation set.
        """
        items = to_dict(self.items)
        if sort_items:
            items.sort(key=lambda x: ITEM_ORDER.get(x.get("type"), 99))
        return {"type": "calculation-set", "items": items}

    @classmethod
    def from_dict(cls, data):
        """
        Create a CalcSet from a dictionary.
        Args:
            data (dict): Dictionary containing calculation set data.
        Returns:
            CalcSet: Instance of CalcSet.
        """
        if data["type"] != "calculation-set":
            raise ValueError(f"Expected type 'calculation-set', got {data['type']}")
        items = []
        for item in data["items"]:
            item_type = item["type"]
            if item_type in classes:
                items.append(classes[item_type].from_dict(item))
            elif item_type == "calculation":
                if item.get("calculation_type") == "number":
                    items.append(Number.from_dict(item))
                elif item.get("calculation_type") == "string":
                    items.append(Category.from_dict(item))
                else:
                    raise ValueError(f"Unknown calculation type: {item.get('calculation_type')}")
            else:
                raise ValueError(f"Unknown item type: {item_type}")
        return cls(items=items)

    def to_json(self, sort_items=True, indent=0):
        """
        Convert the CalcSet to a JSON string.
        Args:
            sort_items (bool): Whether to sort items by type.
            indent (int): Indentation level for JSON output.
        Returns:
            str: JSON string representation.
        """
        return json.dumps(self.to_dict(sort_items=sort_items), indent=indent)

    def to_lfcalc(self, filepath_or_buffer, sort_items=True):
        """
        Write the CalcSet to a Leapfrog .lfcalc file.
        Args:
            filepath_or_buffer (str, Path, or file-like): Output file path or buffer.
            sort_items (bool): Whether to sort items by type.
        """
        if isinstance(filepath_or_buffer, (str, Path)):
            with open(filepath_or_buffer, "wb") as f:
                self._write_to_file(f, sort_items=sort_items)
        else:
            self._write_to_file(filepath_or_buffer, sort_items=sort_items)

    def _write_to_file(self, file, sort_items):
        """
        Write the CalcSet to a file in Leapfrog format.
        Args:
            file (file-like): File object to write to.
            sort_items (bool): Whether to sort items by type.
        """
        compressed_data = zlib.compress(self.to_json(sort_items=sort_items).encode("utf-8"))
        file.write(HEADER)
        file.write(compressed_data)

    @staticmethod
    def read_lfcalc(filepath_or_buffer):
        """
        Read a Leapfrog .lfcalc file and return a CalcSet.
        Args:
            filepath_or_buffer (str, Path, or file-like): Input file path or buffer.
        Returns:
            CalcSet: Instance of CalcSet.
        """
        if isinstance(filepath_or_buffer, (str, Path)):
            with open(filepath_or_buffer, "rb") as f:
                return CalcSet._read_from_file(f)
        else:
            return CalcSet._read_from_file(filepath_or_buffer)

    @staticmethod
    def _read_from_file(file):
        """
        Read a CalcSet from a file object.
        Args:
            file (file-like): File object to read from.
        Returns:
            CalcSet: Instance of CalcSet.
        """
        file.seek(len(HEADER))
        compressed_data = file.read()
        json_data = zlib.decompress(compressed_data).decode("utf-8")
        data = json.loads(json_data)
        return CalcSet.from_dict(data)

    def __repr__(self):
        """
        Return a pretty-printed JSON string representation of the CalcSet.
        """
        return self.to_json(indent=2)

    def __add__(self, other):
        """
        Add two CalcSet objects together, combining their items.
        Args:
            other (CalcSet): Another CalcSet instance.
        Returns:
            CalcSet: New CalcSet with combined items.
        """
        if not isinstance(other, CalcSet):
            return NotImplemented
        return CalcSet(self.items + other.items)


class Item:
    """
    Base class for items in a calculation set.
    Subclasses should define `item_type` and optionally `calculation_type`.
    """
    item_type = None
    calculation_type = None

    def __init__(self, name, children, comment_item="", comment_equation=""):
        """
        Initialize an Item.
        Args:
            name (str): Name of the item.
            children (list): List of child expressions/statements.
            comment_item (str): Comment for the item.
            comment_equation (str): Comment for the equation.
        """
        self.name = name
        self.children = children
        self.comment_item = comment_item
        self.comment_equation = comment_equation

    def to_dict(self):
        """
        Convert the Item to a dictionary representation.
        Returns:
            dict: Dictionary representation of the item.
        """
        if self.item_type is None:
            raise NotImplementedError("item_type must be defined in subclass")
        children = to_dict(self.children, guard_strings=True)
        item = {
            "type": self.item_type,
            "name": self.name,
            "equation": {
                "type": "equation",
                "comment": self.comment_equation,
                "statement": {
                    "type": "list",
                    "children": children,
                },
            },
            "comment": self.comment_item,
        }
        if self.calculation_type:
            item["calculation_type"] = self.calculation_type
        return item

    @classmethod
    def from_dict(cls, data):
        """
        Create an Item from a dictionary.
        Args:
            data (dict): Dictionary containing item data.
        Returns:
            Item: Instance of Item or subclass.
        """
        if cls.item_type is None:
            raise NotImplementedError("item_type must be defined in subclass")
        if data["type"] != cls.item_type:
            raise ValueError(f"Expected item type {cls.item_type}, got {data['type']}")
        children = []
        for child in ensure_list(data["equation"]["statement"]["children"]):
            children.append(dispatch_expression(child))
        return cls(
            name=data["name"],
            children=children,
            comment_item=data.get("comment", ""),
            comment_equation=data["equation"].get("comment", ""),
        )


class IfRow:
    def __init__(self, condition, value):
        """
        Initialize an IfRow.
        Args:
            condition (list): Condition expressions.
            value (list): Value expressions if condition is met.
        """
        self.condition = condition
        self.value = value

    def to_dict(self):
        """
        Convert the IfRow to a dictionary representation.
        Returns:
            dict: Dictionary representation of the IfRow.
        """
        return {
            "type": "if_row",
            "test": {"type": "list", "children": to_dict(self.condition)},
            "result": {"type": "list", "children": to_dict(self.value, guard_strings=True)},
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an IfRow from a dictionary.
        Args:
            data (dict): Dictionary containing IfRow data.
        Returns:
            IfRow: Instance of IfRow.
        """
        if data["type"] != "if_row":
            raise ValueError(f"Expected type 'if_row', got {data['type']}")
        # return cls(
        #     condition=data["test"]["children"],
        #     value=data["result"]["children"],
        # )
        condition = []
        for cond in ensure_list(data["test"]["children"]):
            condition.append(dispatch_expression(cond))
        value = []
        for val in ensure_str_list(data["result"]["children"]):
            value.append(dispatch_expression(val))
        return cls(condition=condition, value=value)


class If:
    def __init__(self, rows, otherwise):
        """
        Initialize an If expression.
        Args:
            rows (list): List of either IfRow objects, dicts, or (condition, value) tuples.
            otherwise (list): Expressions for the 'otherwise' case.
        """
        self.rows = rows
        self.otherwise = otherwise

    def to_dict(self):
        """
        Convert the If expression to a dictionary representation.
        Returns:
            dict: Dictionary representation of the If expression.
        """
        rows = []
        for row in ensure_list(self.rows):
            if isinstance(row, IfRow):
                rows.append(row.to_dict())
            elif isinstance(row, dict) and row.get("type") == "if_row":
                rows.append(row)
            elif isinstance(row, (tuple, list)) and len(row) == 2:
                condition, value = row
                rows.append(IfRow(condition, value).to_dict())
            else:
                raise ValueError(f"Invalid row format: {row}")
        return {
            "type": "if",
            "rows": rows,
            "otherwise": {"type": "list", "children": to_dict(self.otherwise, guard_strings=True)},
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an If expression from a dictionary.
        Args:
            data (dict): Dictionary containing If expression data.
        Returns:
            If: Instance of If.
        """
        if data["type"] != "if":
            raise ValueError(f"Expected type 'if', got {data['type']}")
        rows = [
            IfRow.from_dict(row) if isinstance(row, dict) else row
            for row in ensure_list(data["rows"])
        ]
        otherwise = []
        for val in ensure_str_list(data["otherwise"]["children"]):
            otherwise.append(dispatch_expression(val))
        return cls(rows=rows, otherwise=otherwise)


class Number(Item):
    """
    Represents a numeric calculation item.
    """
    item_type = "calculation"
    calculation_type = "number"


class Category(Item):
    """
    Represents a categorical calculation item.
    """
    item_type = "calculation"
    calculation_type = "string"


class Variable(Item):
    """
    Represents a variable item in a calculation set.
    """
    item_type = "variable"


class Filter(Item):
    """
    Represents a filter item in a calculation set.
    """
    item_type = "filter"


classes = {
    # "calculation": Item,
    "variable": Variable,
    "filter": Filter,
    "if": If,
    "if_row": IfRow,
}


expressions = {
    "if": If,
}


def dispatch_expression(data):
    """
    Dispatch an expression dictionary to the appropriate class constructor.
    Args:
        data (dict or any): Expression data.
    Returns:
        object: Instantiated expression object or the original data if not a dict.
    """
    if isinstance(data, dict) and "type" in data:
        expr_type = data["type"]
        if expr_type in expressions:
            return expressions[expr_type].from_dict(data)
        else:
            raise ValueError(f"Unknown expression type: {expr_type}")
    return data

