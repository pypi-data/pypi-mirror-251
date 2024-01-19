# DistroLab

## Introduction
DistroLab is a Python package for working with Gaussian and Binomial distributions. It provides functionality to calculate characteristics like mean, standard deviation, and to visualize the distributions.

## Installation
To install DistroLab, run the following command:

```commandline
pip install DistroLab
```


## Dependencies
- math
- matplotlib

## Usage
Here are some examples of how to use DistroLab:

### Working with Gaussian Distribution
```python
from distrolab import Gaussian

# Create a Gaussian distribution
gaussian = Gaussian(mu=10, sigma=2)

# Calculate mean and standard deviation
mean = gaussian.calculate_mean()
stdev = gaussian.calculate_stdev()

# Plot the histogram
gaussian.plot_histogram()

# Plot the probability density function
gaussian.plot_histogram_pdf()
```

### Working with Binomial Distribution
```python
from distrolab import Binomial

# Create a Binomial distribution
binomial = Binomial(prob=0.5, size=20)

# Calculate mean and standard deviation
mean = binomial.calculate_mean()
stdev = binomial.calculate_stdev()

# Plot the histogram
binomial.plot_data_histogram()

# Plot the probability density function
binomial.plot_distribution_pdf()
```


## License
This project is licensed under the [MIT License](license.txt)