# Robot@Home Dataset API 0.3.0 #

The Robot-at-Home dataset (Robot@Home, paper
[here](http://mapir.uma.es/papersrepo/2017/2017-raul-IJRR-Robot_at_home_dataset.pdf))
is a collection of raw and processed data from five domestic settings compiled
by a mobile robot equipped with 4 RGB-D cameras and a 2D laser scanner. Its main
purpose is to serve as a testbed for semantic mapping algorithms through the
categorization of objects and/or rooms.

This package provides the Python API that assists in loading, parsing, and
visualizing the annotations in Robot@Home. Please visit http://mapir.isa.uma.es/
for more information on Robot@Home, including for the data, paper, and
tutorials. The exact format of the annotations is also described on the
[Robot@Home website](http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html).

In addition to this API, please [download](https://zenodo.org/record/4495821)
the Robot@Home Dataset in order to run the demos and use the API (also, you'll
be able to download it using the API).

To install

```
pip install robotathome
```

or under conda environment

```
conda config --append channels gambrosio
conda install robotathome
```

Be careful with the opencv library because the pip installation is based on an
unofficial opencv-python package, while the conda installation is based on the
official opencv, usually at an earlier stage than the unofficial one.
