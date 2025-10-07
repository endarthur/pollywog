from ..core import If, IfRow, Number, Category

try:
    import sklearn
except ImportError:
    raise ImportError(
        "scikit-learn is required for conversion. Please install it via 'pip install scikit-learn'."
    )



# Classification and Regression Trees

from sklearn import tree

def convert_tree(tree_model, feature_names, target_name, comment_equation=None):
    tree_ = tree_model.tree_
    feature_name = [
        feature_names[i] if i != tree._tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    def recurse(node):
        if tree_.feature[node] != tree._tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            left = recurse(tree_.children_left[node])
            right = recurse(tree_.children_right[node])
            return If(IfRow(f"[{name}] <= {threshold}", left), right)
        else:
            value = tree_.value[node][0][0]
            return f"{value}"

    if_rows = recurse(0)

    if comment_equation is None:
        comment_equation = f"Converted from {tree_model.__class__.__name__}"

    if isinstance(tree_model, tree.DecisionTreeRegressor):
        return Number(target_name, if_rows
                      , comment_equation=comment_equation)
    elif isinstance(tree_model, tree.DecisionTreeClassifier):
        return Category(target_name, if_rows
                        , comment_equation=comment_equation)
    else:
        raise ValueError("Unsupported tree model type")


# Linear Models
from sklearn import linear_model

def convert_linear_model(lm_model, feature_names, target_name):
    coefs = lm_model.coef_
    intercept = lm_model.intercept_

    terms = [f"{intercept:.6f}"] if intercept != 0 else []
    for coef, feature in zip(coefs, feature_names):
        if coef != 0:
            terms.append(f"{coef:.6f} * [{feature}]")

    equation = " + ".join(terms) if terms else "0"
    return Number(target_name, equation
                  , comment_equation=f"Converted from {lm_model.__class__.__name__}")