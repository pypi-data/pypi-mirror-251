import sys
from typing import _GenericAlias  # type: ignore[attr-defined]
from typing import TYPE_CHECKING, Any, Generic, TypeVar, Union

from sympy import Symbol
from typing_extensions import ParamSpec

from classiq.interface.generator.functions.classical_type import (
    ClassicalArray,
    ClassicalList,
    ClassicalType,
    Struct,
)

from classiq import StructDeclaration
from classiq.qmod.model_state_container import ModelStateContainer

_T = TypeVar("_T")

if TYPE_CHECKING:

    class QParam(Generic[_T], Symbol):  # expose to mypy all operators
        pass

else:

    class QParam(Generic[_T]):
        pass


class QParamScalar(QParam, Symbol):
    pass


class QParamList(QParam):
    def __init__(
        self,
        expr_str: str,
        list_type: Union[ClassicalList, ClassicalArray],
        *,
        qmodule: ModelStateContainer,
    ) -> None:
        self._qmodule = qmodule
        self._expr_str = expr_str
        self._list_type = list_type

    def __str__(self) -> str:
        return self._expr_str

    def __getitem__(self, key: Any) -> QParam:
        return create_param(
            f"{self._expr_str}[{str(key)}]",
            self._list_type.element_type,
            qmodule=self._qmodule,
        )

    def __len__(self) -> int:
        raise ValueError(
            "len(<expr>) is not supported for QMod lists - use <expr>.len() instead"
        )

    def len(self) -> "QParamScalar":
        return QParamScalar(name=f"len({self._expr_str})")


class QParamStruct(QParam):
    def __init__(
        self, expr_str: str, struct_type: Struct, *, qmodule: ModelStateContainer
    ) -> None:
        self._qmodule = qmodule
        self._expr_str = expr_str
        self._struct_type = struct_type

    def __str__(self) -> str:
        return self._expr_str

    def __getattr__(self, field_name: str) -> QParam:
        struct_decl = StructDeclaration.BUILTIN_STRUCT_DECLARATIONS.get(
            self._struct_type.name
        )
        if struct_decl is None:
            struct_decl = self._qmodule.type_decls.get(self._struct_type.name)
        assert struct_decl is not None
        field_type = struct_decl.variables.get(field_name)
        if field_type is None:
            raise ValueError(
                f"Struct {self._struct_type.name!r} doesn't have field {field_name!r}"
            )

        return create_param(
            f"get_field({self._expr_str},{field_name!r})",
            field_type,
            qmodule=self._qmodule,
        )


_P = ParamSpec("_P")


class ArrayBase(Generic[_P]):
    # Support comma-separated generic args in older Python versions
    if sys.version_info[0:2] < (3, 10):

        def __class_getitem__(cls, args) -> _GenericAlias:
            return _GenericAlias(cls, args)


class Array(ArrayBase[_P]):
    pass


def create_param(
    expr_str: str, ctype: ClassicalType, qmodule: ModelStateContainer
) -> QParam:
    if isinstance(ctype, ClassicalList) or isinstance(ctype, ClassicalArray):
        return QParamList(expr_str, ctype, qmodule=qmodule)
    elif isinstance(ctype, Struct):
        return QParamStruct(expr_str, ctype, qmodule=qmodule)
    else:
        return QParamScalar(expr_str)
