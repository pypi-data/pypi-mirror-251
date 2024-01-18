from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Tuple
from typing import Union

import numpy as np
from scipy.signal import convolve
from scipy.signal import convolve2d

from ..state import SimulationState


class Dimension(ABC):
    """Abstract class for dimensions."""

    initial_conditions: SimulationState

    def __init__(self, initial_conditions: SimulationState) -> None:
        self.initial_conditions = initial_conditions

    @abstractmethod
    def create_grid(
        self, num_points: Union[int, Tuple[int, int]], base_value: float = 0.0
    ):
        init_state = np.zeros(num_points, dtype=float)
        init_state.fill(base_value)
        self.initial_conditions.set_state(init_state)

    @abstractmethod
    def convolution():
        pass


class OneDimSpatial(Dimension):
    """One dimensional spatial dimension.

    Args:
        initial_conditions (List[float]): Initial conditions for the simulation.
    """

    initial_conditions: List[float] = None

    def create_grid(self, num_points: int, base_value: float = 0.0):
        """Create a grid of num_points points with base_value(or 0).

        Args:
            num_points (int): Number of points.
            base_value (float): Base value for the grid. Defaults to 0.0.

        Returns:
            np.ndarray: Grid of num_points points with base_value. (1D)
        """
        super().create_grid(num_points, base_value)

    @staticmethod
    def convolution(
        state_matrix: np.ndarray,
        parametric_matrix: np.ndarray,
        mode="same",
    ):
        return convolve(
            state_matrix,
            parametric_matrix,
            mode=mode,
        )


class TwoDimSpatial(Dimension):
    """Two dimensional spatial dimension.

    Args:
        initial_conditions (List[List[float]]): Initial conditions for the simulation.
    """

    initial_conditions: List[List[float]] = None

    def create_grid(self, num_points: Tuple[int, int], base_value: float = 0.0):
        """Create a grid of i * j points with base_value.

        Args:
            num_points (Tuple[int, int]): Number of points in each dimension.
            base_value (float): Base value for the grid. Defaults to 0.0.

        Returns:
            np.ndarray: Grid of i * j points with base_value. (2D)
        """
        super().create_grid(num_points, base_value)

    @staticmethod
    def convolution(
        state_matrix: np.ndarray,
        parametric_matrix: np.ndarray,
        mode="same",
        boundary="wrap",
    ):
        return convolve2d(
            state_matrix,
            parametric_matrix,
            mode=mode,
            boundary=boundary,
            fillvalue=0,
        )
