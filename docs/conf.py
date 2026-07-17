# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import shutil
import sys
from pathlib import Path

RELEASE_VERSION = "26.05"
DOCS_DIR = Path(__file__).parent.resolve()
ROOT_DIR = DOCS_DIR.parent

sys.path.append(str(DOCS_DIR / "_extension"))

project = "AMD Finance"
project_path = str(DOCS_DIR).replace("\\", "/")
author = "Advanced Micro Devices, Inc."
copyright = "Copyright (c) %Y Advanced Micro Devices, Inc. All rights reserved."
version = RELEASE_VERSION
release = RELEASE_VERSION
setting_all_article_info = True
all_article_info_os = ["linux"]
all_article_info_author = ""

extensions = [
    "rocm_docs",
    "rocm_docs_custom.icon",
]
external_toc_path = "./sphinx/_toc.yml"
external_projects_remote_repository = "rocm-finance"

html_theme = "rocm_docs_theme"
html_theme_options = {
    "flavor": "rocm-finance",
}
html_title = f"AMD Finance {RELEASE_VERSION} documentation"
html_context = {}
if os.environ.get("READTHEDOCS", "") == "True":
    html_context["READTHEDOCS"] = True

latex_engine = "xelatex"
latex_elements = {
    "fontpkg": r"""
\usepackage{tgtermes}
\usepackage{tgheros}
\renewcommand\ttdefault{txtt}
"""
}


def copy_rtd_file(src_path: Path, dest_path: Path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest_path)
    print(f"📁 Copied {src_path} → {dest_path}")


gh_release_path = ROOT_DIR / "RELEASE.md"
rtd_release_path = DOCS_DIR / "about" / "release-notes.md"
copy_rtd_file(gh_release_path, rtd_release_path)
