# confidence_calculator/calculator.py

import pandas as pd
import math
from scipy import stats  # 追加

def calculate_confidence(csv_path, confidence_level=0.95):
    """
    Calculate confidence interval for the mean from a CSV file.

    Parameters:
    - csv_path: str, path to the CSV file.
    - confidence_level: float, desired confidence level (default is 0.95).

    Returns:
    - confidence_interval: tuple, (lower_bound, upper_bound).
    """

    # Read CSV file
    data = pd.read_csv(csv_path)

    # Calculate mean and standard deviation
    mean = data.mean()
    std_dev = data.std()

    # Calculate sample size
    sample_size = len(data)

    # Calculate standard error
    std_error = std_dev / math.sqrt(sample_size)

    # Calculate margin of error
    margin_of_error = std_error * stats.t.ppf((1 + confidence_level) / 2, sample_size - 1)

    # Calculate confidence interval
    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error

    return lower_bound, mean, upper_bound
