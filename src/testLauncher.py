import pytest
import os
os.chdir(os.getcwd())
if (os.path.basename(os.getcwd())=="SliCer"):
    args_str = "./src -rA -s -v --cache-clear"
else:
    args_str = "../src -rA -s -v --cache-clear"
pytest.main(args_str.split(" "))