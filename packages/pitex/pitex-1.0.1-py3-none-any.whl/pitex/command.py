class Command:
    name: str
    args: list[str]
    optional_args: list[str]

    def __init__(
        self,
        name: str,
        optional_args: list[str] = [],
        *args: str,
    ):
        self.name = name
        self.args = list(args)
        self.optional_args = optional_args

    def __str__(self):
        return (
            "\\"
            + self.name
            + ("[" + ", ".join(self.optional_args) + "]" if self.optional_args else "")
            + (f"{{{', '.join(self.args)}}}" if self.args else "")
        )

    def __repr__(self):
        return str(self)
