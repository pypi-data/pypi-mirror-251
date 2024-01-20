from types import ModuleType
from typing import Any

import pytest

from symbolite import scalar
from symbolite.core.util import eval_content, substitute_content
from symbolite.impl import libstd


class SimpleVariable(scalar.Scalar):
    """Special type of Scalar that is evaluated to itself."""

    def __repr__(self):
        return self.name

    def eval(self, libsl: ModuleType | None = None):
        return self


class SimpleParameter(scalar.Scalar):
    """Special type of Scalar that is evaluated to itself."""

    def __repr__(self):
        return self.name

    def eval(self, libsl: ModuleType | None = None):
        return self


def is_dependency(x: Any) -> bool:
    return isinstance(x, (SimpleParameter, SimpleVariable))


def test_substitute_content():
    d = {SimpleParameter("x"): 1, SimpleParameter("y"): 2 * SimpleParameter("x")}

    assert substitute_content(d, is_dependency=is_dependency) == {
        SimpleParameter("x"): 1,
        SimpleParameter("y"): (2 * SimpleParameter("x")).subs(
            {SimpleParameter("x"): 1}
        ),
    }


def test_eval_content():
    d = {SimpleParameter("x"): 1}

    assert eval_content(d, libsl=libstd, is_dependency=is_dependency) == {
        SimpleParameter("x"): 1
    }

    d = {SimpleParameter("x"): 1, SimpleParameter("y"): 2 * SimpleParameter("x")}

    assert eval_content(d, libsl=libstd, is_dependency=is_dependency) == {
        SimpleParameter("x"): 1,
        SimpleParameter("y"): 2,
    }


def test_cyclic():
    d = {
        SimpleParameter("x"): 2 * SimpleParameter("x"),
    }

    with pytest.raises(ValueError):
        assert eval_content(d, libsl=libstd, is_dependency=is_dependency)

    d = {
        SimpleParameter("x"): 2 * SimpleParameter("y"),
        SimpleParameter("y"): 2 * SimpleParameter("x"),
    }

    with pytest.raises(ValueError):
        assert eval_content(d, libsl=libstd, is_dependency=is_dependency)
