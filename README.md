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

## Prerequisites: Python development environment installation

Launched in 1991, Python has achieved enormous popularity in the scientific community in recent years. Python is an interpreted high-level general-purpose programming language with a many useful features. It's platform independent, simple, consistent and with a great code readability. Moreover, it has an extensive set of libraries that help to reduce development time.

Artificial Intelligence (AI) and Machine Learning (ML) projects differ from software projects in other areas due to differences in the technology stack and the skills needed to deal with them.

Python offers AI and ML programmers many features that help to develop and test complex algorithms. Even in Computer Vision (CV), there are solid software libraries that allow developers to focus on their research areas.

There are several different Python distributions, each one created with a different approach and for different audiences.

Robot@Home2 Toolbox is written in Python and works well with Anaconda which is a distribution of the Python and R programming languages for scientific computing. Of course, other distributions can be used to run the toolbox.

### Installation in Linux

To install Anaconda in Linux you must follow these steps.

Download the Anaconda installer

    $ cd ~/Downloads
    $ wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh

> replace `~/Downloads` with the path to the file you downloaded.


</div>

Install the distribution

    $ bash ~/Downloads/Anaconda3-2021.05-Linux-x86_64.sh

<div class="notes" id="orge09fe72">
<p>
include the <code>bash</code> command regardless of whether or not you are using Bash shell.
</p>

</div>

Review and agree the license agreement. Accept the default install location.

When the installer prompts *“Do you wish the installer to initialize Anaconda3 by running conda init?”*, we recommend *“yes”*.

Finally, for the installation to take effect

    $ source ~/.bashrc

For more detailed/updated installation information, go to [Anaconda installation page](https://docs.anaconda.com/anaconda/install/).

### Verifying your installation

Enter the command `python`. This command runs the Python shell. If Anaconda is installed and working, the version information it displays when it starts up will include `“Anaconda”`. To exit the Python shell, enter the `quit()` command.

    $ python
    Python 3.7.11 (default, Jul 27 2021, 14:32:16) 
    [GCC 7.5.0] :: Anaconda, Inc. on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> quit()

You can also display a list of installed packages and their versions running `conda list`

    $ conda list
    # packages in environment at /home/user/anaconda3:
    #
    # Name                    Version                   Build  Channel
    ...

### Making a virtual environment

A virtual environment is a Python environment such that the Python interpreter, libraries and scripts installed into it are isolated from those installed in other virtual environments

When a virtual environment is active, the installations tools install Python packages into the virtual environment without needing to be told to do so explicitly and without interfering in other virtual environments.

That's the reason why it's recommended to work with a virtual environment specifically for Robot@Home2. To do that with conda

    $ conda create --name rh python=3.9

<div class="notes" id="orga447755">
<p>
change <code>rh</code> to a name of your choice
</p>

</div>

<div class="notes" id="org431e2b5">
<p>
Robot@Home2 runs with python 3.7 or higher
</p>

</div>

once it has been created, it can already be activated

    $ conda activate rh

to deactivate run

    $ conda deactivate

### Literate programming with Jupyter

Literate programming is a programming paradigm introduced by Donald Knuth in which a computer program is given an explanation of its logic in a natural language, such as English, interspersed with snippets of macros and traditional source code. The approach is typically used in scientific computing and in data science routinely for reproducible research and open access purposes.

On the other hand, the [Jupyter](https://jupyter.org) *Notebook* is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text. Additionally *JupyterLab* is a web-based interactive development environment for Jupyter notebooks, code, and data.

Jupyter is an application of literate programming and Robot@Home2 includes Jupyter notebooks for introductions, easy learning, and technical explanations.

Installing Jupyter in Anaconda distribution is an easy task

    $ conda install -c conda-forge jupyterlab

<div class="notes" id="org2484622">
<p>
remember to previously activate your virtual environment with <code>conda activate</code>
command
</p>

</div>

<div class="notes" id="org6d9c1f5">
<p>
&gt; pip is a common Python package manager that is included in Anaconda and many
other distributions
</p>

</div>

## Time to install Robot@Home2

If you have followed previous sections you have the right working environment to
open [[https://github.com/goyoambrosio/RobotAtHome_API/blob/master/notebooks/10-Download-and-install.ipynb][this notebok]] with Jupyter to download and install both toolbox and dataset.

However, if jupyter notebook is not your choice right now you can try the
following instructions.

### Installing the toolbox

Robot@Home2 Toolbox can be installed through the Python package manager.

Confirm you are in the right virtual environment and install it

```
$ pip install robotathome
```

> pip is a common Python package manager that is included in Anaconda and many
> other distributions

and check it in Python

```
$ python
Python 3.7.11 (default, Jul 27 2021, 14:32:16) 
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import robotathome as rh
>>> print (rh.__version__)
0.4.9
```

### Downloading the dataset

Robot@Home resides in Zenodo site where all data versions can be downloaded.
Latest version ([v2.0.1](https://zenodo.org/record/4530453)) is composed of two
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

### Still trying the old version

This package still provides the Python API (dataset.py) that assists in loading,
parsing, and visualizing the annotations in the original Robot@Home (versions
[1.0.1](https://zenodo.org/record/3901564) and
[1.0.2](https://zenodo.org/record/4495821)). Please visit
http://mapir.isa.uma.es/ for more information on Robot@Home, including for the
data, paper, and tutorials. The exact format of the annotations is also
described on the [Robot@Home
website](http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html).

