#!/usr/bin/python
import pandas as pd
import numpy as np
import matplotlib

from matplotlib import pyplot as plt

# Import modules from /batterym/ folder.
import sys
sys.path.append('../batterym')
import log


logs = log.get_battery('../logs/capacity_example')
df = pd.DataFrame(logs)

print df
