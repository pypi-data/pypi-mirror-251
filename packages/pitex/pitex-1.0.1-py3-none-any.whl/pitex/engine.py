import subprocess


class LatexEngine:
    def __init__(self, texfile, engine="pdflatex", **kwargs):
        self.texfile = texfile
        self.engine = engine
        self.kwargs = kwargs

    def run(self):
        cmd = [self.engine, self.texfile]
        for k, v in self.kwargs.items():
            cmd.append(f"--{k}={v}")
        subprocess.run(cmd)
