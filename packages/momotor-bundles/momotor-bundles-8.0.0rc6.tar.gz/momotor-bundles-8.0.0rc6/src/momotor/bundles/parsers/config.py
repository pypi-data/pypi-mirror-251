from __future__ import annotations

from pathlib import Path

from xsdata.formats.dataclass.parsers.config import ParserConfig


class BundleParserConfig(ParserConfig):
    __slots__ = (
        "huge_tree",
        "process_xslt",
        "validation_schema_path",
    )

    def __init__(
        self,
        huge_tree: bool = True,
        process_xslt: bool = False,
        validation_schema_path: str | Path | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.huge_tree = huge_tree
        self.process_xslt = process_xslt
        self.validation_schema_path = validation_schema_path
