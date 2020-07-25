import pytest
import os
os.chdir(os.getcwd())
args_str = "-rA -s -v --cache-clear"
pytest.main(args_str.split(" "))