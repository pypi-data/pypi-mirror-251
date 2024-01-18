import numpy as np


def contains_only_real_numbers(arr: np.ndarray) -> bool:
    """
    Check if the given array contains only real numbers.

    This function tests whether all elements in the given array `arr`
    are real numbers. Real numbers in this context are those that are either
    floating point numbers (dtype 'f') or integers (dtype 'i').

    Parameters:
    arr (np.ndarray): The array to be checked.

    Returns:
    bool: True if all elements are real numbers, False otherwise.
    """
    if arr.dtype.kind in ["f", "i"]:
        return True
    else:
        return False