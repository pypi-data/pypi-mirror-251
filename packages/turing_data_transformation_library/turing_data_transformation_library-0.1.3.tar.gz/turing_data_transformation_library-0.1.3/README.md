# Data Transformation Library

## Overview
This Python library is designed to assist data scientists in performing essential data transformations,
particularly for machine learning models. It provides a suite of functions that simplify common operations 
in data processing and analysis.

## Features
The library currently offers three primary functions:

- Transpose: A function to transpose matrices (2D tensors), switching their axes.
- Time Series Windowing: A tool for creating windows in time series data, essential for time series
analysis and modeling.
- Cross-Correlation: An implementation of the cross-correlation function, commonly used in convolutional 
- neural networks.

### Transpose
![transpose.png](img%2Ftranspose.png)
- Function: transpose2d(input_matrix)
- Input: input_matrix - a list of lists of real numbers representing a 2D matrix.
- Output: Transposed matrix as a list of lists of real numbers.
- Implementation: Pure Python, using standard library.

### Time Series Windowing
![window.png](img%2Fwindow.png)
- Function: window1d(input_array, size, shift=1, stride=1)
- Inputs:
  - input_array: List or 1D Numpy array of real numbers.
  - size: Integer, size (length) of the window.
  - shift: Integer, shift (step size) between windows.
  - stride: Integer, stride (step size) within each window.
- Output: List of lists or 1D Numpy arrays of real numbers.
- Implementation: Python and Numpy.

### Cross-Correlation
![convolution.png](img%2Fconvolution.png)
- Function: convolution2d(input_matrix, kernel, stride=1)
- Inputs:
  - input_matrix: 2D Numpy array of real numbers.
  - kernel: 2D Numpy array of real numbers.
  - stride: Integer, stride value.
- Output: 2D Numpy array of real numbers.
- Implementation: Python and Numpy.

## Installation
The library is available on PyPI and can be installed using pip:
```
pip install turing_data_transformation_library
```

## Usage
After installation, the functions can be imported and used in Python scripts or Jupyter notebooks.

Example usage:
```
from turing_data_transformation_library.transpose import transpose2d
from turing_data_transformation_library.time_series_windowing import window1d
from turing_data_transformation_library.cross_correlation import convolution2d

# Example for transpose2d
matrix = [[1, 2], [3, 4]]
transpose2d(matrix)

# Example for window1d
input_array = [1, 2, 3, 4, 5]
size = 2
shift = 2
window1d(input_array, size, shift)

# Example for convolution2d
input_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
kernel = [[1, 0], [0, -1]]
stride = 2
convolution2d(input_matrix, kernel, stride)
```