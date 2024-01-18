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

        mse_left = [mse(cumsum_sq[i], cumsum[i], i + 1) for i in range(n - 1)]
        mse_right = [
            mse(cumsum_sq[-1] - cumsum_sq[i], cumsum[-1] - cumsum[i], n - i - 1)
            for i in range(n - 1)
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
        self, estimator: Estimator = Estimator.CUSUM, recursive: bool = True
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
