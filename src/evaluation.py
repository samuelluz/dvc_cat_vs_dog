# https://dvc.org/doc/use-cases/versioning-data-and-model-files/tutorial
import json
import numpy as np
import sys
import os
import yaml
from dvclive import Live
from sklearn import metrics
from tensorflow.keras.models import load_model

live = Live("evaluation")

model_file = sys.argv[1]
model = load_model(model_file)