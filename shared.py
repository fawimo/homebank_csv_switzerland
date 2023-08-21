## Automatic file processing package
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import sys


## Statement processing package

import numpy as np
import pandas as pd
from pathlib import Path
import datetime
import glob
import os
import tabula

## General variables definition 
folder_path = "/home/fabien/Statements/"