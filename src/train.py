# https://dvc.org/doc/use-cases/versioning-data-and-model-files/tutorial
import numpy as np
import sys
import os
import yaml

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, Flatten, Dense
from dvclive.keras import DvcLiveCallback
from tqdm.keras import TqdmCallback

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython train.py data-file-path\n")
    sys.exit(1)

pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)

top_model_weights_path = 'model.h5'
train_data_dir = os.path.join('data', 'train')
cats_train_path = os.path.join(train_data_dir, 'cats')
nb_train_samples = 2 * len([name for name in os.listdir(cats_train_path)
                            if os.path.isfile(
                                os.path.join(cats_train_path, name))])

train_data_path = os.path.join(sys.argv[1], 'bottleneck_features_train.npy')
validation_data_path = os.path.join(sys.argv[1], 'bottleneck_features_validation.npy')


params = yaml.safe_load(open("params.yaml"))["featurize"]
nb_validation_samples = params["nb_validation_samples"]
batch_size = params["batch_size"]
params = yaml.safe_load(open("params.yaml"))["train"]
epochs = params["epochs"]


def train_top_model():
    train_data = np.load(open(train_data_path, 'rb'))
    train_labels = np.array(
        [0] * (int(nb_train_samples / 2)) + [1] * (int(nb_train_samples / 2)))

    validation_data = np.load(open(validation_data_path, 'rb'))
    validation_labels = np.array(
        [0] * (int(nb_validation_samples / 2)) +
        [1] * (int(nb_validation_samples / 2)))

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels),
              verbose=0,
              callbacks=[TqdmCallback(), DvcLiveCallback(path="evaluation_train")])
    model.save(top_model_weights_path)

train_top_model()
