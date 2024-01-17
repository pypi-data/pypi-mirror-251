import subprocess
from enum import Enum
from time import time
from pathlib import Path

import pitex.config
import pitex.package


class LatexDocument:
    name: str
    """The name of the document."""
    config: pitex.config.LatexConfig
    """The parameters of the latex document to be generated."""
    doc_text: str = "\\documentclass{article}"
    """The final document file text string."""
    content: str
    """The text between `\\begin{document}` and `\\end{document}`."""
    path: Path
    """The path to the file, by default `[name].tex`."""

    def __init__(
        self,
        name: str = "main",
        config: pitex.config.LatexConfig = pitex.config.LatexConfig(),
    ):
        self.name = name
        self.config = config
        self.content = ""
        self.path = Path(f"{name}.tex")

    def add_line(self, line: str = ""):
        self.doc_text += "\n" + line

    def add_package(self, name: str, options: list[str] = []):
        if self.config.packages:
            self.config.packages.append(pitex.package.Package(name))

    def generate_document(self) -> str:
        generated_document = LatexDocument(self.name, self.config)

        if not self.config.page_type:
            print("Page type not specified!")
            exit(1)
        else:
            generated_document.add_line(
                rf"\usepackage[{self.config.page_type.value}paper, total={{6in, 8in}}]{{geometry}}"
            )

        if not self.config.page_numbering:
            generated_document.add_line("\\pagenumbering{gobble}" + "\n")

        generated_document.add_line(
            rf'\usepackage{{{", ".join([package.name for package in filter(lambda package: not package.options, self.config.packages)])}}}'
        )

        for package in list(filter(lambda x: x.options, self.config.packages)):
            generated_document.add_line(package.get_import_directive())

        generated_document.add_line()

        generated_document.add_line("\\begin{document}")

        for line in self.content.splitlines():
            generated_document.add_line(line)

        generated_document.add_line("\\end{document}")

        return generated_document.doc_text

    def __str__(self):  # type: ignore
        return self.generate_document()

    def write(self):
        with open(self.path, "w") as file:
            file.write(str(self))
            file.close()

    def compile(self):
        self.write()

        print("Compiling...", end=" ")
        start = time()
        subprocess.run(["pdflatex", self.path], stdout=subprocess.DEVNULL)
        end = time()
        print("✅ in {:.2f} seconds.".format(end - start))

        self.clean()

    def clean(self):
        import os

        extensions_to_remove = [
            "aux",
            "log",
            "out",
            "fls",
            "fdb_latexmk",
            "synctex.gz",
            "toc",
            "gz",
            "bbl",
            "blg",
            "bcf",
            "run.xml",
        ]

        for extension in extensions_to_remove:
            if os.path.exists(f"{self.name}.{extension}"):
                os.remove(f"{self.name}.{extension}")

    def __str__(self):
        return self.generate_document()
