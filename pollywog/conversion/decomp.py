# Refactor Plan: Intermediate Representation (IR) for CalcSet Decompilation
# =======================================================================
#
# Goal: Introduce an abstract, normalized IR for CalcSet, items, and expressions.
# All decompilation logic (grouping, template inference, code emission) will operate on the IR, not on pollywog's concrete classes.
#
# Pipeline:
# ---------
# 1. **IR Definition**
#    - Define IRCalcSet, IRItem, IRExpression, IRIf, IRIfRow, etc.
#    - These are simple dataclasses or classes, not tied to pollywog internals.
#
# 2. **Conversion Layer**
#    - Traverse a real CalcSet and convert all items/expressions to IR equivalents.
#    - Handles normalization and flattening as needed.
#
# 3. **Analysis/Processing**
#    - Grouping, template inference, and substitutions are performed on the IR.
#    - This makes logic much easier to test and reason about.
#
# 4. **Code Emission**
#    - Emit Python code from the IR, not from the original objects.
#    - The emitter is decoupled from pollywog's class structure.
#
# Benefits:
# - Clean separation of concerns
# - Easier to test and extend
# - Robust to changes in pollywog internals
#
# TODO: Define IR classes, implement conversion, then refactor grouping, template, and emission logic to use IR.

from dataclasses import dataclass, field
from typing import List, Any, Optional, Dict, Union
from pollywog.core import Item, CalcSet, If, IfRow


@dataclass
class IRExpression:
    children: List[Union[str, "IRIf"]]

    def emmit(self):
        if len(self.children) == 1 and isinstance(self.children[0], str):
            return self.children[0]
        else:
            parts = [
                child.emmit() if isinstance(child, IRIf) else "\"" + child + "\""
                for child in self.children
                if child is not None and child != ""
            ]
            return f"[{', '.join(parts)}]"
        
    @classmethod
    def from_expression(cls, expression: List[Any]) -> "IRExpression":
        ir_children = []
        for child in expression:
            if isinstance(child, If):
                ir_children.append(IRIf.from_if(child))
            else:
                ir_children.append(child)
        return cls(children=ir_children)

    def get_dependencies(self) -> set[str]:
        deps = set()
        for child in self.children:
            if isinstance(child, IRIf):
                deps.update(child.get_dependencies())
            elif isinstance(child, str):
                # Extract variable names from the string expression
                import re

                vars_in_expr = re.findall(r"\[([^\]]+)\]", child)
                deps.update(vars_in_expr)
        return deps

    # find all string constants in the expression, eiter set by single quotes, double quotes or numeric literals
    def get_constants(self) -> set[str]:
        consts = set()
        for child in self.children:
            if isinstance(child, IRIf):
                consts.update(child.get_constants())
            elif isinstance(child, str):
                import re

                # Find string literals
                str_consts = re.findall(r'"(.*?)"|\'(.*?)\'', child)
                for sc in str_consts:
                    const_value = sc[0] if sc[0] else sc[1]
                    consts.add(const_value)

                # Find numeric literals
                num_consts = re.findall(r'\b\d+(\.\d+)?\b', child)
                for nc in num_consts:
                    consts.add(nc)
        return consts
    
    def get_parameters(self) -> set[str]:
        return self.get_dependencies() | self.get_constants()

    def to_template(self, parameters) -> "IRExpression":
        template_children = []
        for child in self.children:
            if isinstance(child, IRIf):
                template_children.append(child.to_template(parameters))
            else:  # child is either an If or a string
                for i, par in enumerate(parameters):
                    if par in child:
                        child = child.replace(par, f"{{v{i}}}")
                template_children.append(child)
        return IRExpression(children=template_children)
    
    def partial_apply(self, parameters, values) -> "IRExpression":
        applied_children = []
        for child in self.children:
            if isinstance(child, IRIf):
                applied_children.append(child.partial_apply(parameters, values))
            else:  # child is either an If or a string
                for i, par in enumerate(parameters):
                    if par in child:
                        child = child.replace(f"{{v{i}}}", str(values[i]))
                applied_children.append(child)
        return IRExpression(children=applied_children)





@dataclass
class IRIfRow:
    condition: IRExpression
    result: IRExpression

    def emmit(self):
        return f"IfRow(condition={self.condition.emmit()}, result={self.result.emmit()})"


@dataclass
class IRIf:
    rows: List[IRIfRow]
    otherwise: IRExpression

    def emmit(self):
        return f"If(rows=[{', '.join(row.emmit() for row in self.rows)}], otherwise={self.otherwise.emmit()})"
    
    @classmethod
    def from_if(cls, if_obj: If) -> "IRIf":
        ir_rows = []
        for row in if_obj.rows:
            ir_condition = IRExpression.from_expression(row.condition)
            ir_result = IRExpression.from_expression(row.value)
            ir_rows.append(IRIfRow(condition=ir_condition, result=ir_result))
        ir_otherwise = IRExpression.from_expression(if_obj.otherwise) if if_obj.otherwise else IRExpression(children=[])
        return cls(rows=ir_rows, otherwise=ir_otherwise)
    
    def get_dependencies(self) -> set[str]:
        deps = set()
        for row in self.rows:
            deps.update(row.condition.get_dependencies())
            deps.update(row.result.get_dependencies())
        deps.update(self.otherwise.get_dependencies())
        return deps
    
    def get_constants(self) -> set[str]:
        consts = set()
        for row in self.rows:
            consts.update(row.condition.get_constants())
            consts.update(row.result.get_constants())
        consts.update(self.otherwise.get_constants())
        return consts
    
    def to_template(self, parameters) -> "IRIf":
        template_rows = []
        for row in self.rows:
            template_condition = row.condition.to_template(parameters)
            template_result = row.result.to_template(parameters)
            template_rows.append(IRIfRow(condition=template_condition, result=template_result))
        template_otherwise = self.otherwise.to_template(parameters)
        return IRIf(rows=template_rows, otherwise=template_otherwise)


@dataclass
class IRItem:
    name: str
    expression: IRExpression
    item: Item

    def emmit(self):
        return f"{self.item.__class__.__name__}(name={self.name}, expression={self.expression.emmit()})"

    @classmethod
    def from_item(cls, item: Item) -> "IRItem":
        ir_expression = IRExpression.from_expression(item.expression)
        return cls(name=item.name, expression=ir_expression, item=item)
    
    def get_dependencies(self) -> list[str]:
        pass


@dataclass
class IRLoop:
    var_names: List[str]
    value_lists: List[List[str]]
    body_item: IRItem

@dataclass
class IRCalcSet:
    items: List[Union[IRItem, IRLoop]]

    def emmit(self, calcset_name: str = "calcset"):
        items_code = [
            "from pollywog import CalcSet, Number, Variable, Category, Filter, If, IfRow",
            "",
            "items = []",
            "",
        ]
        for item in self.items:
            if not hasattr(item, "emmit_lines"):
                items_code.append(f"items.append({item.emmit()})")
            else:
                items_code.extend(item.emmit_lines())
        items_code.append("")
        items_code.append(f"{calcset_name} = CalcSet(items)")
        items_code.append(calcset_name)

        return "\n".join(items_code)
    
    @classmethod
    def from_calcset(cls, calcset: CalcSet) -> "IRCalcSet":
        ir_items = []
        for item in calcset.items:
            ir_items.append(IRItem.from_item(item))
        return cls(items=ir_items)