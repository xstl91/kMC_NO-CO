KMC model for NO-CO reaction system
========================

Basic information
------------------------

Here we provide the kMC model for the NO-CO reaction system on Rh(100) and Rh(111).

The code is developed based on Python 2.7 and customized **KMCLib** package.

The following article concerning the construction and application of the model is under preparation:

> First-principles-based kinetic Monte Carlo simulation for the NO-CO reaction system on Rh(100) and Rh(111)

Contains
-------------------------

* `Interaction`: lateral-interaction parameters
* `Model_N2O`: codes for the kMC model concerning N<sub>2</sub>O-involved processes
* `run_N2O.py`: an executable script to do kMC simulation using `Model_N2O`
* `Model_NOCO`: codes for the kMC model concerning the whole NO-CO reaction system
* `run_NOCO.py`: an executable script to do kMC simulation using `Model_NOCO`
* `Analysis`: some executable scripts to analyze and visualize results from `run_NOCO.py`
* `README.md`: a brief introduction

Usage
-------------------------

`Model_N2O` and `Model_NOCO` are constructed as modules. Please add the path of the directory `.../kMC_NO-CO` to the environment variable `PYTHONPATH`.

To do the simulation, please copy the `run_N2O.py` or `run_NOCO.py` script to the data-collecting directory, and modify it to provide simulation settings as instructed by comments.

`run_N2O.py` should be run serially, but `run_NOCO.py` can be run parallelly.

If the customization of the model is needed, please modify the codes in the `Model_N2O` or `Model_NOCO` directory.