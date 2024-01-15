from itertools import islice

import pytest

from exact_cover_py import exact_covers

try:
    from . import problems
except (ModuleNotFoundError, ImportError):
    import problems
canonical = problems.canonical
canonical_s = problems.canonical_s
canonical_1 = problems.canonical_1


PARTIAL_TESTS = {
    "pentomino_chessboard_problem": 20,
    "pentomino_5_12_problem": 20,
}


def define_test(problem_name, problem):
    """
    for a given problem defined in problems.py
    say small_trimino_problem
    we define a derived function named like
    say test_small_trimino_problem
    """

    def test_solutions(problem):
        match problem:
            # check we get the first solutions in the same order
            # as in the solutions list
            case {
                "data": data,
                "solutions": solutions,
                "first_solutions": first_solutions,
            }:
                # this would be if the order of solutions could be trusted
                # canonical_solutions = canonical_s(solutions)
                # canonical_first_solutions = canonical_solutions[:first_solutions]
                # try:
                #     gen = exact_covers(data)
                #     computed_first_solutions = canonical_s(islice(gen, first_solutions))
                #     assert canonical_first_solutions == computed_first_solutions
                # except StopIteration:
                #     assert canonical_solutions == []
                canonical_solutions = canonical(solutions)
                gen = exact_covers(data)
                for _ in range(first_solutions):
                    canonical_computed_solution = canonical_1(next(gen))
                    assert canonical_computed_solution in canonical_solutions
            case {
                "data": data,
                "solutions": solutions,
            }:
                canonical_solutions = canonical(solutions)
                try:
                    canonical_computed = canonical(exact_covers(data))
                    assert canonical_computed == canonical_solutions
                except StopIteration:
                    assert solutions == []

    # problem = problems.__dict__[problem_name]()
    test_name = f"test_{problem_name}"
    if problem_name in PARTIAL_TESTS:
        problem["first_solutions"] = PARTIAL_TESTS[problem_name]
    # assign the global variable test_<problem_name>
    # to the newly defined function
    globals()[test_name] = lambda: test_solutions(problem)


for problem_name, problem_function in problems.ALL_PROBLEMS.items():
    problem = problem_function()
    define_test(problem_name, problem)
