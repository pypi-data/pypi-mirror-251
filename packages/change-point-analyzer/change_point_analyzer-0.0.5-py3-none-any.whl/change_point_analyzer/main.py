from enum import Enum, auto
from typing import List, Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt


def dimension_check(x: np.ndarray) -> np.ndarray:
    """Check if the input array is 1-dimensional."""
    if x.ndim == 1:
        return x.reshape(1, -1)
    elif x.ndim == 2:
        return x
    else:
        raise ValueError("Input array must be 1 or 2 dimensional.")


def compute_cusum(x: np.ndarray) -> np.ndarray:
    """Compute cumulative sum of array elements."""
    x = dimension_check(x)
    x_bar = np.mean(x, axis=1).reshape(-1, 1)
    normalized_x = x - x_bar
    return np.cumsum(normalized_x, axis=1)


def get_s_diff(x: np.ndarray) -> float:
    """Get the difference between the maximum and minimum of the cumulative sum."""
    x = dimension_check(x)
    return np.max(x, axis=1) - np.min(x, axis=1)


class Estimator(Enum):
    CUSUM = auto()
    MSE = auto()


class ChangePointAnalyzer:
    def __init__(
        self,
        data: np.array,
        bootstrap_samples: int = 1000,
        minimum_significance: float = 0.95,
    ):
        assert data.ndim == 1, "Input data must be 1-dimensional."
        assert len(data) >= 5
        self.data = data
        self.bootstrap_samples = bootstrap_samples
        self.minimum_significance = minimum_significance
        self.bootstrap(self.bootstrap_samples)
        self.series_cusum = compute_cusum(self.data)
        self.sample_cusum = compute_cusum(self.samples)
        self.s_diff_series = get_s_diff(self.series_cusum)
        self.s_diff_samples = get_s_diff(self.sample_cusum)

    def plot(self, changepoints: Optional[List[int]] = None):
        """Plot the cumulative sum with changepoints and plot original data with changepoints on different plots."""
        fig, ax = plt.subplots(nrows=2, ncols=1)
        ax[0].title.set_text("Time Series")
        ax[0].plot(self.data)
        ax[1].title.set_text("CUSUM")
        ax[1].plot(self.series_cusum.T)
        if changepoints:
            for changepoint in changepoints:
                ax[0].axvline(changepoint, color="red")
                ax[1].axvline(changepoint, color="red")
        plt.show()

    def bootstrap(self, n: int):
        """create n bootstrap samples of the data randomly ordered."""
        self.samples = np.random.choice(
            self.data, size=(n, len(self.data)), replace=True
        )

    def compute_changepoint_significance(self) -> np.float64:
        percentage_below_threshold = np.mean(self.s_diff_samples < self.s_diff_series)
        return percentage_below_threshold

    def compute_changepoint_s_diff(self) -> Tuple[Optional[int], Optional[float]]:
        """Compute the changepoint of the data."""
        significance = self.compute_changepoint_significance()
        if significance < self.minimum_significance:
            return (None, None)
        changepoint = self.series_cusum.argmax()
        return (changepoint, self.data[changepoint])

    def compute_changepoint_mse(self) -> [Tuple[Optional[int], Optional[float]]]:
        significance = self.compute_changepoint_significance()
        if significance < self.minimum_significance:
            return (None, None)
        n = len(self.data)
        cumsum = np.cumsum(self.data)
        cumsum_sq = np.cumsum(self.data**2)

        def mse(sum_sq, sum_, count):
            return (sum_sq - (sum_**2) / count) / count

        mse_left = [mse(cumsum_sq[i], cumsum[i], i + 1) for i in range(3, n - 3)]
        mse_right = [
            mse(cumsum_sq[-1] - cumsum_sq[i], cumsum[-1] - cumsum[i], n - i - 1)
            for i in range(3, n - 3)
        ]
        total_mse = np.array(mse_left) + np.array(mse_right)
        min_mse_index = np.argmin(total_mse)
        return min_mse_index + 1, total_mse[min_mse_index]

    def _changepoint_estimator(
        self, estimator: Estimator = Estimator.CUSUM
    ) -> callable:
        if estimator == Estimator.CUSUM:
            return self.compute_changepoint_s_diff
        else:
            return self.compute_changepoint_mse

    def detect_changepoints(
        self, estimator: Estimator = Estimator.MSE, recursive: bool = True
    ) -> List[Tuple[Optional[int], Optional[float]]]:
        changepoint_tuples = []

        def detect_recursive(data_slice, offset=0):
            # base case
            if len(data_slice) < 5:
                return

            analyzer = ChangePointAnalyzer(
                data_slice,
                bootstrap_samples=self.bootstrap_samples,
                minimum_significance=self.minimum_significance,
            )
            estimator_func = analyzer._changepoint_estimator(estimator)
            changepoint_idx, changepoint_value = estimator_func()

            if changepoint_idx is not None:
                adjusted_idx = changepoint_idx + offset
                changepoint_tuples.append((adjusted_idx, changepoint_value))
                # recursive case
                if recursive:
                    left_slice = data_slice[:changepoint_idx]
                    right_slice = data_slice[changepoint_idx + 1 :]
                    detect_recursive(left_slice, offset)
                    detect_recursive(right_slice, offset + changepoint_idx + 1)

        detect_recursive(self.data)

        return changepoint_tuples

if __name__ == "__main__":
    data = np.array([ 9.38709677,  7.75      ,  9.48387097,  8.06666667, 10.29032258,
       10.46666667, 11.06451613, 11.06451613, 10.93333333,  9.25806452,
       11.43333333, 11.19354839,  9.12903226,  6.72413793,  5.64516129,
       13.33333333, 10.5483871 ,  7.1       ,  7.64516129,  7.5483871 ,
        6.93333333,  7.96774194, 11.13333333,  9.06451613, 13.        ,
        8.85714286,  8.19354839,  9.66666667, 11.        , 11.33333333,
       11.4516129 , 11.87096774, 12.96666667, 10.83870968,  9.7       ,
       13.06451613, 11.25806452,  9.64285714, 11.09677419, 11.33333333,
       15.25806452, 13.8       , 17.03225806, 13.19354839, 16.66666667,
       14.58064516, 16.13333333, 16.74193548, 12.48387097, 12.53571429,
       12.93548387, 13.96666667, 15.16129032, 15.03333333, 15.87096774,
       14.87096774, 13.86666667, 13.64516129, 14.96666667, 15.80645161,
       14.6875    ])
    analyzer = ChangePointAnalyzer(data, bootstrap_samples=10_000, minimum_significance=0.85)
    changepoints = analyzer.detect_changepoints()
    print(changepoints)
    analyzer.plot([c[0] for c in changepoints])