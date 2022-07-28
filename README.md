# DVC - Get Started with cat_vs_dog
Building image classification models using little data.

## Get Started
```bash
git init
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
dvc init
git status
    # new file:   .dvc/.gitignore
    # new file:   .dvc/config
    # new file:   .dvcignore
    # new file:   .gitignore
git commit -m "Initialize DVC"
```
## Download data
**dvc get** can download any file or directory tracked in a DVC repository (and stored remotely). It's like wget, but for DVC or Git repos.

```bash
dvc get https://github.com/iterative/dataset-registry \
        tutorials/versioning/data.zip
unzip -q data.zip
rm -f data.zip
dvc add data
git add data.dvc .gitignore
```
## Storing and sharing

```bash
# pip install 'dvc[gdrive]'
# dvc remote add -d storage gdrive://...
dvc remote add -d myremote /tmp/dvcstore
dvc push
git add .dvc/config
dvc remote list
	# myremote        /tmp/dvcstore
git commit -m "Configure local remote"
```

# How can we use these artifacts outside of the project?
## List files and directories
```bash
dvc list https://github.com/iterative/dataset-registry get-started
```
## Download
```bash
dvc get https://github.com/iterative/dataset-registry use-cases/cats-dogs
```
## Import to yout project
```bash
dvc import https://github.com/iterative/dataset-registry \
             use-cases/cats-dogs -o data/cats-dogs
```
## Python API

It's also possible to integrate your data or models directly in source code with DVC's Python API. This lets you access the data contents directly from within an application at runtime. For example:
```python
import dvc.api

with dvc.api.open(
    'get-started/data.xml',
    repo='https://github.com/iterative/dataset-registry'
) as fd:
    # fd is a file descriptor which can be processed normally
```

## Pipeline

```bash
dvc stage add -n featurize -d src/featurization.py -d data \
    -p featurize.img_width,featurize.img_height \
    -p featurize.nb_validation_samples,featurize.batch_size \
    -o bottleneck_features_train.npy \
    -o bottleneck_features_validation.npy \
    python src/featurization.py data/
dvc dag
dvc repro
```
A dvc.yaml file is generated. It includes information about the command we want to run (python src/prepare.py data/data.xml), its dependencies, and outputs.

The command options used above mean the following:

- **-n** prepare specifies a name for the stage. If you open the dvc.yaml file you will see a section named prepare.

- **-p** prepare.seed,prepare.split defines special types of dependencies — parameters. We'll get to them later in the Metrics, Parameters, and Plots page, but the idea is that the stage can depend on field values from a parameters file (params.yaml by default):

- **-d** src/prepare.py and **-d** data/data.xml mean that the stage depends on these files to work. Notice that the source code itself is marked as a dependency. If any of these files change later, DVC will know that this stage needs to be reproduced.

- **-o** data/prepared specifies an output directory for this script, which writes two files in it. This is how the workspace should look like after the run:

The last line, python src/prepare.py data/data.xml is the command to run in this stage, and it's saved to dvc.yaml, as shown below.

By using dvc stage add multiple times, and specifying outputs of a stage as dependencies of another one, we can describe a sequence of commands which gets to a desired result. This is what we call a data pipeline or dependency graph.

```bash
dvc run -n train -d src/train.py -d features/ \
    -p train.epochs,featurize.nb_validation_samples,featurize.batch_size \
    -o model.h5 -M evaluation.json \
    python src/train.py features/
dvc dag
dvc metrics show
```

## Making changes

```bash
dvc get https://github.com/iterative/dataset-registry \
        tutorials/versioning/new-labels.zip
unzip -q new-labels.zip
rm -f new-labels.zip
dvc add data
git add data.dvc model.h5.dvc metrics.csv
git commit -m "Second model, trained with 2000 images"
git tag -a "v2.0" -m "model v2.0, 2000 images"
```

The whole point of creating this dvc.yaml file is the ability to easily reproduce a pipeline:
command can be used to compare this state with an actual state of the workspace.

```bash
dvc status 
dvc params diff
dvc metrics diff
dvc plots diff
```

## Switching between versions

```bash
git checkout v1.0
dvc checkout
```
On the other hand, if we want to keep the current code, but go back to the previous dataset version, we can target specific data, like this:

```bash
git checkout v1.0 data.dvc
dvc checkout data.dvc
```
https://dvc.org/doc/use-cases/versioning-data-and-model-files/tutorial
https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html