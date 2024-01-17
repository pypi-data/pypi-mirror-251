class Package:
    options: list[str]
    name: str

    def get_import_directive(self):
        tmp = "\\usepackage"

        tmp += (
            f'[{", ".join(self.options)}]' + f"{{{self.name}}}"
            if self.options
            else f"{{{self.name}}}"
        )

        return tmp

    def __init__(self, name: str, options: list[str] = []):
        self.options = options
        self.name = name

    def __str__(self):
        return self.get_import_directive()
