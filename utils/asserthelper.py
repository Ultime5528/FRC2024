def implies(condition1: bool, condition2: bool) -> bool:
    """
    implies(scondition1: bool, condition2: bool) -> bool

    Returns the result implication operator
         condition1 implies condition2
       or in mathematical notation
         condition1 => condition2
    """
    return (not condition1) or condition2