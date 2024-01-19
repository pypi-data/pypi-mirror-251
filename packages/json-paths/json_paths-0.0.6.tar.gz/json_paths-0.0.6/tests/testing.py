import json 
import sys 

sys.path.append('.')
from src.jsonpaths import JsonPaths

with open('/workspaces/jsonpaths/src/jsonpaths/workspacescan_results_20231023_144526043.json', 'r') as jfile:
    jfile = json.load(jfile)
j