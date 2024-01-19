import os
from os import path
from sys import platform
import dpml.mps_workaround

base_path = os.getenv("BASE_PATH")
cache_path = path.join(base_path, "models")
out_put = path.join(base_path, "output")
os.environ["TRANSFORMERS_CACHE"] = cache_path
os.environ["HF_HUB_CACHE"] = cache_path
os.environ["HF_HOME"] = cache_path
print("Base Path is: ", base_path)
print("Cache Path is: ", cache_path)
print("Output Path is: ", out_put)
is_mac = platform == "darwin"
