# zolfa-nd2reader


### About

`zolfa-nd2reader` is a pure-Python package that reads images produced by NIS Elements 4.0+. It has only been definitively tested on NIS Elements 4.30.02 Build 1053. Support for older versions is being actively worked on.
The reader is written in the [pims](https://github.com/soft-matter/pims) framework, enabling easy access to multidimensional files, lazy slicing, and nice display in IPython.

This version is a fork of the project of published [here](https://github.com/Open-Science-Tools/nd2reader).

### Documentation

Documentation specific to this fork is not available yet.

The documentation of the origianl `nd2reader` project was available [here](http://www.lighthacking.nl/nd2reader/).

### Installation

The package is available on PyPi. Install it using:

```
pip install zolfa-nd2reader
```

If you don't already have the packages `numpy`, `pims` and `xmltodict`, they will be installed automatically running pip.
Python >= 3.10 are supported.


### ND2s

`nd2reader` follows the [pims](https://github.com/soft-matter/pims) framework. To open a file and show the first frame:

```python
from zolfa.nd2reader import ND2Reader
import matplotlib.pyplot as plt

with ND2Reader('my_directory/example.nd2') as images:
  plt.imshow(images[0])
```

After opening the file, all `pims` features are supported. Please refer to the [pims documentation](http://soft-matter.github.io/pims/).

### Contributing

If you'd like to help with the development of nd2reader or just have an idea for improvement, please see the [contributing](https://gitlab.pasteur.fr/zolfa/zolfa-nd2reader/-/blob/master/CONTRIBUTING.md) page
for more information.

### Bug Reports and Features

If this fails to work exactly as expected, please open an [issue](https://github.com/rbnvrw/nd2reader/issues).
If you get an unhandled exception, please paste the entire stack trace into the issue as well.

### Acknowledgments

First fork by Ruben Verweij.

PIMS modified version by Ruben Verweij.

Original version by Jim Rybarski. Support for the development of this package was partially provided by the [Finkelstein Laboratory](http://finkelsteinlab.org/).
