from distutils.core import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="tktermwidget",
    version="0.0.1",
    description="A terminal emulator for Tkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="littlewhitecloud",
    url="https://github.com/littlewhitecloud/TkTerminal",
    packages=["tkterm"],
)
