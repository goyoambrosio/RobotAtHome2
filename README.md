# Robot@Home2 Dataset Toolbox #

[![PyPI](https://img.shields.io/pypi/v/robotathome)](https://pypi.org/project/robotathome/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4530453.svg)](https://doi.org/10.5281/zenodo.4530453)

The Robot-at-Home dataset (Robot@Home, paper
[here](http://mapir.uma.es/papersrepo/2017/2017-raul-IJRR-Robot_at_home_dataset.pdf))
is a collection of raw and processed data from five domestic settings compiled
by a mobile robot equipped with 4 RGB-D cameras and a 2D laser scanner. Its main
purpose is to serve as a testbed for semantic mapping algorithms through the
categorization of objects and/or rooms.

Nevertheless, the Robot@Home dataset has been updated to **Robot@Home2**. This
update is made up of a relational database file in SQLite format with all the
original data and a size of only 2,2 GB. The image and scene files have been
reorganized and now takes only 25,9 GB.

The database, named `rh.db`, is a relational sql database accessible with the
SQLite engine that usually accompanies the python environment and is popularly
used in the development of current applications in both fixed (linux and
windows) and mobile environments. (android).

The data files have been organized into two main groups. On the one hand, the
files with RGBD data (RGB images and depth images) and on the other the 3D
scenes in point cloud files.

The intensity (RGB) and depth (D) image files have a standard *png* format so
they can be opened directly. In addition, the files are linked to the data in
the database through tables that relate them. Moreover, the database contains
tables that relate the files of the new version with those of the old version.
  
In the case of 3D scene files, these are plain text files that store the
coordinates and colors of the points that make up the 3D cloud. These files can
be easily visualized with current software for the visualization of point
clouds like [MeshLab](https://www.meshlab.net/).

You no longer need to waste time diving the obscure data formats (despite an API
-**dataset.py**- for that is provided). Instead, you can simply surf the dataset
through SQL queries or the new toolbox.

The toolbox (**toolbox.py**) has been coded for various purposes. The first one
consists of encapsulating frequent queries as functions and integrating the
results with a data analysis library such as Pandas. Pandas library is widely
used in data science and machine learning disciplines in the Python framework.
The second one is the integration of the data set with the GluonCV library to
apply deep learning algorithms in artificial vision.

## Installing the toolbox

To can install the Robot@Home2 Toolbox through the Python package manager.

It's recommended to install it under a python environment.

If you are using conda you can create an environment:

```
$ conda create --name rh python=3.9
```

Change **rh** for your chosen environment name.

Then activate it

```
$ conda activate rh
```

Now you can install Robot@Home2 Toolbox

```
$ pip install robotathome
```

and check it out in python

```
>>> import robotathome as rh
>>> print (rh.__version__)
0.4.9
```

## Downloading the dataset

Robot@Home resides in Zenodo site where all data versions can be downloaded.
Last version ([v2.0.1](https://zenodo.org/record/4530453)) is composed of two
files: `Robot@Home2_db.tgz` and `Robot@Home2_files.tgz`. The first one contains the
database, and the second one contains the bunch of RGBD images and 3D scenes

You can choose to download it on your own or through the new brand toolbox.

In case you are considering Linux

```
$ wget https://zenodo.org/record/4530453/files/Robot@Home2_db.tgz
$ wget https://zenodo.org/record/4530453/files/Robot@Home2_files.tgz
```

check the files integrity

```{bash}
$ md5sum Robot@Home2_db.tgz 
c2a3536b6b98b907c56eda3a78300cbe  Robot@Home2_db.tgz

$ md5sum Robot@Home2_files.tgz 
c55465536738ec3470c75e1671bab5f2  Robot@Home2_files.tgz
```

and to finish unzip files

```
$ pv /home/user/Downloads/Robot@Home2_db.tgz | tar -J -xf - -C /home/user/WORKSPACE/
$ pv /home/user/Downloads/Robot@Home2_files.tgz | tar -xzf - -C /home/user/WORKSPACE/files
```

or even better, now you can do the same programmatically using the toolbox

```{python}
import robotathome as rh

# Download files
rh.download('https://zenodo.org/record/4530453/files/Robot@Home2_db.tgz', '~/Downloads')
rh.download('https://zenodo.org/record/4530453/files/Robot@Home2_files.tgz', '~/Downloads')

# Compute md5 checksums
md5_checksum_db = rh.get_md5('~/Downloads/Robot@Home2_db.tgz')
md5_checksum_files = rh.get_md5('~/Downloads/Robot@Home2_files.tgz')

# Check the files integrity and download
if md5_checksum_db == 'c2a3536b6b98b907c56eda3a78300cbe':
    rh.uncompress('~/Downloads/Robot@Home2_db.tgz', '~/WORKSPACE')
else:
    print('Integrity of Robot@Home2_db.tgz is compromised, please download again')
    
if md5_checksum_files == 'c55465536738ec3470c75e1671bab5f2':
    rh.uncompress('~/Downloads/Robot@Home2_files.tgz', '~/WORKSPACE/files')
else:
    print('Integrity of Robot@Home2_files.tgz is compromised, please download again')
```

## Still trying the old version

This package still provides the Python API (dataset.py) that assists in loading,
parsing, and visualizing the annotations in the original Robot@Home (versions
[1.0.1](https://zenodo.org/record/3901564) and
[1.0.2](https://zenodo.org/record/4495821)). Please visit
http://mapir.isa.uma.es/ for more information on Robot@Home, including for the
data, paper, and tutorials. The exact format of the annotations is also
described on the [Robot@Home
website](http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html).

