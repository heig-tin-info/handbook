from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .transformers import to_kebab_case


class CommonConfig(BaseModel):
    """Common configuration for LaTeX, propagated to each book."""

    build_dir: Optional[Path] = None
    save_html: Optional[bool] = False
    mermaid_config: Optional[Path] = None
    project_dir: Optional[Path] = None  # Set internally

class CoverConfig(BaseModel):
    name: str = Field('default', description="Cover template name")
    color: Optional[str] = Field('black', description="Primary color")
    logo: Optional[str] = Field(None, description="Logo path")

class BookConfig(CommonConfig):
    """Configuration for a book."""

    root: Optional[str] = None  # Section title used as root
    title: str = None  # Book title
    subtitle: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    email: Optional[str] = None
    folder: Optional[Path] = None
    frontmatter: Optional[List[str]] = []
    backmatter: Optional[List[str]] = []
    base_level: Optional[int] = -2
    frontmatter: Optional[List[str]] = []
    backmatter: Optional[List[str]] = []
    copy_files: Optional[Dict[str, str]] = {}
    author: Optional[str] = None
    index_is_foreword: Optional[bool] = False
    drop_title_index: Optional[bool] = False
    cover: Optional[CoverConfig] = CoverConfig(name='default')

    @model_validator(mode="after")
    def set_folder_and_build_dir(self):
        """Set folder to title in kebab case if not provided"""
        if self.folder is None and self.title is not None:
            self.folder = to_kebab_case(self.title)

        return self


class LaTeXConfig(CommonConfig):
    """Configuration for LaTeX taken from the mkdocs.yml file."""

    enabled: Optional[bool] = True
    books: Optional[List[BookConfig]] = [BookConfig()]
    clean_assets: Optional[bool] = True

    @model_validator(mode="after")
    @classmethod
    def propagate(cls, data: Any) -> Any:
        for book in data.books:
            to_propagate = ["build_dir", "mermaid_config", "save_html", "project_dir"]
            for key in to_propagate:
                if getattr(book, key) is None:
                    setattr(book, key, getattr(data, key))
        return data

    model_config = ConfigDict(extra="forbid")

    def add_extra(self, **extra_data):
        """Allow to add extra data to the configuration object."""
        for key, value in extra_data.items():
            object.__setattr__(self, key, value)
            object.__setattr__(self, key, value)
            object.__setattr__(self, key, value)
            object.__setattr__(self, key, value)
