from scpy.primitives import Function, Predicate


def from_predicate_to_function(predicate: Predicate) -> Function:
    symbol = predicate.functor
    arguments = predicate.arguments
    return Function(symbol, arguments)


def from_function_to_predicate(function: Function) -> Predicate:
    functor = function.symbol or ""
    arguments = function.arguments
    return Predicate(functor, arguments)
