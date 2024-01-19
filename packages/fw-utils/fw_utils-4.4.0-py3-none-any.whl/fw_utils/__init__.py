"""Flywheel utilities and common helpers."""
from datetime import datetime as builtin_datetime
from importlib.metadata import version
from json import JSONEncoder

try:
    from bson import ObjectId
except ImportError:  # pragma: no cover
    ObjectId = None  # type: ignore
try:
    from pydantic import BaseModel
except ImportError:  # pragma: no cover
    BaseModel = None  # type: ignore


__version__ = version(__name__)
__all__ = [
    "ZoneInfo",
    "format_datetime",
    "get_datetime",
    "get_tzinfo",
    "AttrDict",
    "attrify",
    "flatten_dotdict",
    "get_field",
    "inflate_dotdict",
    "AnyFile",
    "AnyPath",
    "BinFile",
    "TempDir",
    "TempFile",
    "fileglob",
    "open_any",
    "BaseFilter",
    "ExpressionFilter",
    "Filters",
    "IncludeExcludeFilter",
    "NumberFilter",
    "SetFilter",
    "SizeFilter",
    "StringFilter",
    "TimeFilter",
    "Template",
    "Timer",
    "format_query_string",
    "format_template",
    "format_url",
    "hrsize",
    "hrtime",
    "pluralize",
    "quantify",
    "report_progress",
    "Pattern",
    "parse_field_name",
    "parse_hrsize",
    "parse_hrtime",
    "parse_pattern",
    "parse_url",
    "Cached",
    "TempEnv",
    "assert_like",
]

from .datetime import ZoneInfo, format_datetime, get_datetime, get_tzinfo
from .dicts import AttrDict, attrify, flatten_dotdict, get_field, inflate_dotdict
from .files import AnyFile, AnyPath, BinFile, TempDir, TempFile, fileglob, open_any
from .filters import (
    BaseFilter,
    ExpressionFilter,
    Filters,
    IncludeExcludeFilter,
    NumberFilter,
    SetFilter,
    SizeFilter,
    StringFilter,
    TimeFilter,
)
from .formatters import (
    Template,
    Timer,
    format_query_string,
    format_template,
    format_url,
    hrsize,
    hrtime,
    pluralize,
    quantify,
    report_progress,
)
from .parsers import (
    Pattern,
    parse_field_name,
    parse_hrsize,
    parse_hrtime,
    parse_pattern,
    parse_url,
)
from .state import Cached, TempEnv
from .testing import assert_like


def fw_utils_json_encoder(self, obj):
    """Customizable encoder with datetime/objectid/pydantic support."""
    if hasattr(obj, "__json__"):
        return obj.__json__()
    if isinstance(obj, builtin_datetime):
        return format_datetime(obj)
    if ObjectId is not None and isinstance(obj, ObjectId):
        return str(obj)
    if BaseModel is not None and isinstance(obj, BaseModel):
        return getattr(obj, "model_dump", obj.dict)()
    return self.orig_default(obj)


# patch / extend the built-in python json encoder
setattr(JSONEncoder, "orig_default", JSONEncoder.default)
setattr(JSONEncoder, "default", fw_utils_json_encoder)
