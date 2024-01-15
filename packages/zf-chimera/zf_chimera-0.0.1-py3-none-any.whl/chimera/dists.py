from typing import List

import matplotlib.pyplot as plt
import numpy as np

line_plotted = False


def plot_line(slope: float, b: float):
    x = np.linspace(66, 100, 100)
    y = slope * x + b

    plt.plot(x, y)
    plt.show()


def first_dist(uniform_start, uniform_end) -> float:
    value = np.random.uniform(uniform_start, uniform_end)
    # logger.info(f"first: {value}")
    return value


def second_dist(slope, c, taper_start, taper_end) -> float:
    # Adjust the CDF to start at taper_start
    def cdf(x):
        return (slope / 2) * (x - taper_start) ** 2 + c * (x - taper_start)

    # Calculate the normalization constant based on the CDF at taper_end
    constant = 1 / (cdf(taper_end) - cdf(taper_start))
    c *= constant
    slope *= constant

    # Define the inverse CDF based on the normalized CDF
    def inverse_cdf(u):
        # Adjust for the normalization and offset
        return taper_start + (-c + np.sqrt(c ** 2 + 2 * slope * (u + cdf(taper_start)))) / slope

    value = inverse_cdf(np.random.uniform(0, 1))
    # logger.warning(f"second: {value}")
    return value


def age_dist() -> float:
    global line_plotted
    uniform_start = 1
    uniform_end = 65

    taper_start = 66
    taper_start_prob = 6
    taper_end = 100
    taper_end_prob = 0

    # Generate a random float between 0 and 1 to decide which distribution to sample from
    rand = np.random.rand()

    if rand <= 0.8:
        return first_dist(uniform_start, uniform_end)
    else:
        # Approximate slope of the line from the graph
        slope = (taper_end_prob - taper_start_prob) / (taper_end - taper_start)
        c = taper_start_prob - slope * taper_start
        # print(f"slope: {slope}")
        # print(f"c: {c}")

        # if not line_plotted:
        #     plot_line(slope, c)
        #     line_plotted = True

        # print(f"Calling second_dist with rand: {rand}, slope: {slope}, c: {c}, taper_end: {taper_end}")

        return second_dist(slope, c, taper_start, taper_end)


def test_second_dist():
    min_val, max_val = 1000, -100
    for i in range(10000):
        rand = np.random.uniform(0, 1)
        val = second_dist(rand, -0.17647058823529413, 17.647058823529413, 66, 100)
        min_val = min(min_val, val)
        max_val = max(max_val, val)

    print(f"min_val: {min_val}")
    print(f"max_val: {max_val}")
    return


def plot_age_dist_char():
    x = np.linspace(1, 100, 1000)
    y: List[float] = [age_dist() for _ in range(1000)]

    # Bucketize and plot
    buckets = range(1, 105, 5)  # Goes up to 105 to include the last bucket [100-104]
    hist, bins = np.histogram(y, bins=buckets)

    # Calculate the percentage of the total for each bin
    hist_percentage = (hist / float(hist.sum())) * 100

    # Calculate the center of each bin for plotting
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    # Plot the histogram as a bar chart
    plt.bar(bin_centers, hist_percentage, width=5, edgecolor='black')

    # Set the plot title and labels
    plt.title('Age Distribution (%)')
    plt.xlabel('Age (bucketed in 5-year intervals)')
    plt.ylabel('Percentage of Total Population')

    # Show the plot
    plt.show()


if __name__ == "__main__":
    age = age_dist()
    print(f"age: {age}")
