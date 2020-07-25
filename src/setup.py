from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "SliCer",
    version = "2.0",
    description = "A backward static slicing tool for C langage.",
    executables = [Executable("SliCer.py")],
)