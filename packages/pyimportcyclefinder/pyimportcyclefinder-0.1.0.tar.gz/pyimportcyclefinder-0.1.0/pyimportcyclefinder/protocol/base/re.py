import sys
from types import GenericAlias
from typing import Protocol, overload, AnyStr, Any, TypeVar, Mapping, Callable, Optional, runtime_checkable, Iterator
from typing_extensions import Self, Literal
try:
    from typing_extensions import Buffer
except ImportError as e:
    from typing_extensions.abc import Buffer


ReadableBuffer = Buffer
_T = TypeVar("_T")


@runtime_checkable
class BasePatternProtocol(Protocol[AnyStr]):
    @overload
    def search(
        self: "BasePatternProtocol[str]",
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> "Optional[BaseMatchProtocol[str]]": ...
    @overload
    def search(
        self: "BasePatternProtocol[bytes]",
        string: ReadableBuffer,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> "Optional[BaseMatchProtocol[bytes]]": ...
    @overload
    def match(
        self: "BasePatternProtocol[str]",
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> "Optional[BaseMatchProtocol[str]]": ...
    @overload
    def match(
        self: "BasePatternProtocol[bytes]",
        string: ReadableBuffer,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> "Optional[BaseMatchProtocol[bytes]]": ...
    @overload
    def fullmatch(
        self: "BasePatternProtocol[str]",
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> "Optional[BaseMatchProtocol[str]]": ...
    @overload
    def fullmatch(
        self: "BasePatternProtocol[bytes]",
        string: ReadableBuffer,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> "Optional[BaseMatchProtocol[bytes]]": ...
    @overload
    def split(
        self: "BasePatternProtocol[str]", string: str, maxsplit: int = ..., concurrent: bool | None = ..., timeout: float | None = ...
    ) -> list[str | Any]: ...
    @overload
    def split(
        self: "BasePatternProtocol[bytes]",
        string: ReadableBuffer,
        maxsplit: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> list[bytes | Any]: ...
    @overload
    def findall(
        self: "BasePatternProtocol[str]",
        string: str,
        pos: int = ...,
        endpos: int = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> list[Any]: ...
    @overload
    def findall(
        self: "BasePatternProtocol[bytes]",
        string: ReadableBuffer,
        pos: int = ...,
        endpos: int = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> list[Any]: ...
    @overload
    def finditer(
        self: "BasePatternProtocol[str]",
        string: str,
        pos: int = ...,
        endpos: int = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> "Iterator[BaseMatch[str]]": ...
    @overload
    def finditer(
        self: "BasePatternProtocol[bytes]",
        string: ReadableBuffer,
        pos: int = ...,
        endpos: int = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> "Iterator[BaseMatch[bytes]]": ...
    @overload
    def sub(
        self: "BasePatternProtocol[str]",
        repl: str | Callable[["BaseMatchProtocol[str]"], str],
        string: str,
        count: int = ...,
        flags: int = ...,
        pos: int | None = ...,
        endpos: int | None = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> str: ...
    @overload
    def sub(
        self: "BasePatternProtocol[bytes]",
        repl: ReadableBuffer | Callable[["BaseMatchProtocol[bytes]"], ReadableBuffer],
        string: ReadableBuffer,
        count: int = ...,
        flags: int = ...,
        pos: int | None = ...,
        endpos: int | None = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> bytes: ...
    @overload
    def subn(
        self: "BasePatternProtocol[str]",
        repl: str | Callable[["BaseMatchProtocol[str]"], str],
        string: str,
        count: int = ...,
        flags: int = ...,
        pos: int | None = ...,
        endpos: int | None = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> tuple[str, int]: ...
    @overload
    def subn(
        self: "BasePatternProtocol[bytes]",
        repl: ReadableBuffer | Callable[["BaseMatchProtocol[bytes]"], ReadableBuffer],
        string: ReadableBuffer,
        count: int = ...,
        flags: int = ...,
        pos: int | None = ...,
        endpos: int | None = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> tuple[bytes, int]: ...


@runtime_checkable
class BaseMatchProtocol(Protocol[AnyStr]):
    @overload
    def group(self, __group: Literal[0] = 0) -> AnyStr: ...
    @overload
    def group(self, __group: int | str = ...) -> AnyStr | Any: ...
    @overload
    def group(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[AnyStr | Any, ...]: ...
    @overload
    def groups(self, default: None = None) -> tuple[AnyStr | Any, ...]: ...
    @overload
    def groups(self, default: _T) -> tuple[AnyStr | _T, ...]: ...
    @overload
    def groupdict(self, default: None = None) -> dict[str, AnyStr | Any]: ...
    @overload
    def groupdict(self, default: _T) -> dict[str, AnyStr | _T]: ...
    @overload
    def span(self, __group: int | str = ...) -> tuple[int, int]: ...
    @overload
    def span(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[tuple[int, int], ...]: ...
    @overload
    def spans(self, __group: int | str = ...) -> list[tuple[int, int]]: ...
    @overload
    def spans(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[list[tuple[int, int]], ...]: ...
    @overload
    def start(self, __group: int | str = ...) -> int: ...
    @overload
    def start(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[int, ...]: ...
    @overload
    def starts(self, __group: int | str = ...) -> list[int]: ...
    @overload
    def starts(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[list[int], ...]: ...
    @overload
    def end(self, __group: int | str = ...) -> int: ...
    @overload
    def end(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[int, ...]: ...
    @overload
    def ends(self, __group: int | str = ...) -> list[int]: ...
    @overload
    def ends(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[list[int], ...]: ...
    def expand(self, template: AnyStr) -> AnyStr: ...
    def expandf(self, format: AnyStr) -> AnyStr: ...
    @overload
    def captures(self, __group: int | str = ...) -> list[AnyStr]: ...
    @overload
    def captures(self, __group1: int | str, __group2: int | str, *groups: int | str) -> tuple[list[AnyStr], ...]: ...
    def capturesdict(self) -> dict[str, list[AnyStr]]: ...
    def detach_string(self) -> None: ...
    def allcaptures(self) -> tuple[list[AnyStr]]: ...
    def allspans(self) -> tuple[list[tuple[int, int]]]: ...
    @overload
    def __getitem__(self, __key: Literal[0]) -> AnyStr: ...
    @overload
    def __getitem__(self, __key: int | str) -> AnyStr | Any: ...
    def __copy__(self) -> Self: ...
    def __deepcopy__(self) -> Self: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...


@runtime_checkable
class BaseScannerProtocol(Protocol[AnyStr]):
    def __iter__(self) -> Self: ...
    def __next__(self) -> BaseMatchProtocol[AnyStr]: ...
    def match(self) -> Optional[BaseMatchProtocol[AnyStr]]: ...
    def search(self) -> Optional[BaseMatchProtocol[AnyStr]]: ...