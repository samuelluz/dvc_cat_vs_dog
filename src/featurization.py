from pydoc import ispath
import numpy as np
import os
import sys
import yaml

from tensorflow.keras import applications
from tensorflow.keras.preprocessing.image import ImageDataGenerator

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython featurization.py data-features-path\n")
    sys.exit(1)

params = yaml.safe_load(open("params.yaml"))["featurize"]
img_width = params["img_width"]
img_height = params["img_height"]
nb_validation_samples = params["nb_validation_samples"]
batch_size = params["batch_size"]


pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)
input_path = sys.argv[1]

train_data_dir = os.path.join(input_path, 'train')
validation_data_dir = os.path.join(input_path, 'validation')
output_train = os.path.join("features", "bottleneck_features_train.npy")
output_validation = os.path.join("features", "bottleneck_features_validation.npy")

cats_train_path = os.path.join(train_data_dir, 'cats')
nb_train_samples = 2 * len([name for name in os.listdir(cats_train_path)
                            if os.path.isfile(
                                os.path.join(cats_train_path, name))])

def save_bottlebeck_features():
    datagen = ImageDataGenerator(
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest')

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_train = model.predict_generator(
        generator, nb_train_samples // batch_size)
    np.save(open(output_train, 'wb'),
            bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_validation = model.predict_generator(
        generator, nb_validation_samples // batch_size)
    np.save(open(output_validation, 'wb'),
            bottleneck_features_validation)
            
if not os.path.exists("features/"):
    os.mkdir("features")

save_bottlebeck_features()