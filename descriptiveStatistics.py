import statistics
import numpy as np
import scipy.stats as stats

def getDescriptiveStatistics(array, name):
    print(name)
    # Mean
    print("Mean", statistics.mean(array))
    # Standard Error
    print("Standard Error", stats.sem(array))
    # Median
    print("Median", statistics.median(array))
    # Mode
    print("Mode", statistics.mode(array))
    # Standard Deviation
    print("Standard Deviation", np.std(array))
    # Sample Variance
    print("Sample Variance", statistics.variance(array))
    # Kurtosis
    print("Kurtosis", stats.kurtosis(array))
    # Skewness
    print("Skewness", stats.skew(array))
    # Range
    print("Range", np.ptp(array))
    # Minimum
    print("Minimum", np.amin(array))
    # Maximum
    print("Maximum", np.amax(array))
    # Sum
    print("Sum", sum(array))
    # Count
    print("Count", len(array))