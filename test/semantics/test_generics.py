# -*- coding: utf-8 -*-

from typing import Callable, List
from pytest import raises
from discopy.python import Function

def test_parameterized_generics_in_function():
    def f(g: Callable[[int], int]) -> int:
        return g(42)

    # Function with Callable[[int], int] as domain
    # This ensures that discopy can handle parameterized generics in dom/cod
    # without crashing in assert_isinstance checks.
    func = Function(f, Callable[[int], int], int)

    # Should work with a valid callable
    assert func(lambda x: x) == 42

    # Should raise TypeError (not crash) with an invalid argument
    with raises(TypeError):
        func(1)

def test_list_generic_in_function():
    # Test with List[int]
    def sum_list(xs: List[int]) -> int:
        return sum(xs)

    func = Function(sum_list, List[int], int)

    # Valid input
    assert func([1, 2, 3]) == 6

    # Invalid input
    with raises(TypeError):
        func("not a list")
