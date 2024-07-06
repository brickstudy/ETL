import os
import sys

root_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
src_path = os.path.abspath(os.path.join(root_path, "src"))
tests_path = os.path.abspath(os.path.join(root_path, "tests"))

if src_path not in sys.path:
    sys.path.append(src_path)

if tests_path not in sys.path:
    sys.path.append(tests_path)
