# Robot@Home Dataset API #

The Robot-at-Home dataset (Robot@Home, paper here) is a collection of raw and
processed data from five domestic settings compiled by a mobile robot equipped
with 4 RGB-D cameras and a 2D laser scanner. Its main purpose is to serve as a
testbed for semantic mapping algorithms through the categorization of objects
and/or rooms.

This package provides the Python API that assists in loading, parsing, and
visualizing the annotations in Robot@Home. Please visit http://mapir.isa.uma.es/
for more information on Robot@Home, including for the data, paper, and
tutorials. The exact format of the annotations is also described on the
[Robot@Home website](http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html).

In addition to this API, please download the Robot @Home Dataset in order to run
the demos and use the API. It is available on the project website.

To install:

```
pip install robotathome
```

or

```
sudo pip install git+git://github.com/goyoambrosio/RoboAtHome_API.git#egg=RobotAtHome_API
```
