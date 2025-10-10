"""Configuration models used by the LaTeX plugin."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .transformers import to_kebab_case


class CommonConfig(BaseModel):
    """Common configuration propagated to each book."""

    model_config = ConfigDict(extra="forbid")

    build_dir: Path | None = None
    save_html: bool = False
    mermaid_config: Path | None = None
    project_dir: Path | None = None


class CoverConfig(BaseModel):
    """Metadata used to render book covers."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(default="default", description="Cover template name")
    color: str | None = Field(default="black", description="Primary color")
    logo: str | None = Field(default=None, description="Logo path")


class BookConfig(CommonConfig):
    """Configuration for an individual book."""

    root: str | None = None
    title: str | None = None
    subtitle: str | None = None
    author: str | None = None
    year: int | None = None
    email: str | None = None
    folder: Path | None = None
    frontmatter: list[str] = Field(default_factory=list)
    backmatter: list[str] = Field(default_factory=list)
    base_level: int = -2
    copy_files: dict[str, str] = Field(default_factory=dict)
    index_is_foreword: bool = False
    drop_title_index: bool = False
    cover: CoverConfig = Field(default_factory=CoverConfig)

    @model_validator(mode="after")
    def set_folder(self) -> "BookConfig":
        """Populate the output folder from the book title when missing."""

        if self.folder is None and self.title:
            self.folder = to_kebab_case(self.title)
        return self


class LaTeXConfig(CommonConfig):
    """Configuration for LaTeX taken from ``mkdocs.yml``."""

    enabled: bool = True
    books: list[BookConfig] = Field(default_factory=lambda: [BookConfig()])
    clean_assets: bool = True

    @model_validator(mode="after")
    def propagate(self) -> "LaTeXConfig":
        """Propagate common values to nested book configurations."""

        to_propagate = ("build_dir", "mermaid_config", "save_html", "project_dir")
        for book in self.books:
            for key in to_propagate:
                if getattr(book, key) is None:
                    setattr(book, key, getattr(self, key))
        return self

    def add_extra(self, **extra_data: Any) -> None:
        """Allow consumers to attach additional attributes at runtime."""

        for key, value in extra_data.items():
            object.__setattr__(self, key, value)

