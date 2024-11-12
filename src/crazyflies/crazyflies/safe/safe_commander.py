import numpy as np
from numpy.typing import NDArray

from typing import List


class SafeCommander:
    """The SafeCommander provides functionality to convert target setpoints to safe ones.
    This is done by:
        1. clipping to max_step_distance.
        2. clipping at a bounding box.
        ...
    """

    def __init__(
        self,
        dt: float,
        max_step_distance_xy: float,
        max_step_distance_z: float,
        clipping_box: List[float] = None,
    ):
        """Initializes the SafeCommander. Lets the user set clipping distances. Bounding Box.

        Args:
            dt (float): The update rate at which safe_cmd_position is called afterwards
            max_step_distance_xy (float): Maximum xy_step the target is allowed be away from the position of the crazyflie in m/s
            max_step_distance_z (float): Maximum z_step the target is allowed to be away from the position of the crazyflie in m/s
            clipping_box (List[float]): 6 floats describing the bounding box no target is allowed to be outside of.
            The 6 values describe 2 opposite corners of the box.
        """
        self.dt = dt
        self.max_step_distance_xy = max_step_distance_xy
        self.max_step_distance_z = max_step_distance_z
        self.clipping_box = clipping_box
        if clipping_box is not None and len(clipping_box) == 6:
            self.clipping_box = np.array(
                [
                    min(clipping_box[0], clipping_box[3]),
                    min(clipping_box[1], clipping_box[4]),
                    min(clipping_box[2], clipping_box[5]),
                    max(clipping_box[0], clipping_box[3]),
                    max(clipping_box[1], clipping_box[4]),
                    max(clipping_box[2], clipping_box[5]),
                ]
            )

    def safe_cmd_position(
        self, position: List[float], target: List[float]
    ) -> List[float]:
        """Clips a target to be safe.

        Applies the clipping box as well as the max step distances

        Args:
            position (List[float]): The current position
            target (List[float]): The target as provided by the user

        Returns:
            List[float]: A safe target which can be sent to crazyflie controller as setpoint
        """
        np_position = np.array(position)
        np_target = np.array(target)

        np_target = self.__clip_step_distance(np_position, np_target)
        # np_target = self.__clip_box(np_target)

        return list(np_target)

    def __clip_box(self, target: NDArray[np.float_]) -> NDArray[np.float_]:
        """Clips the target to always stay inside of box

        Args:
            target (NDArray[np.float_]): The target to clop

        Returns:
            NDArray[np.float_]: The new clipped target
        """
        if self.clipping_box is not None:
            target = np.array(
                [
                    min(self.clipping_box[3], max(self.clipping_box[0], target[0])),
                    min(self.clipping_box[4], max(self.clipping_box[1], target[1])),
                    min(self.clipping_box[5], max(self.clipping_box[2], target[2])),
                ]
            )
        return target

    def __clip_step_distance(
        self, position: NDArray[np.float_], target: NDArray[np.float_]
    ) -> NDArray[np.float_]:
        """Clips the target with a maximum step distance.

        The step distances are set when initalizing the Commander

        Args:
            position (NDArray[np.float_]): The position we are at
            target (NDArray[np.float_]): The target we should go to

        Returns:
            NDArray[np.float_]: The new clipped target
        """
        max_step_distance_xy = self.dt * self.max_step_distance_xy
        max_step_distance_z = self.dt * self.max_step_distance_z

        delta = target - position
        d_xy = abs(np.linalg.norm(delta[:2]))

        if d_xy > max_step_distance_xy:
            direction_xy = delta[:2] / d_xy  # unit vector
            target[:2] = (
                position[:2] + direction_xy * max_step_distance_xy
            )  # add scaled v to pos

        if abs(delta[2]) > max_step_distance_z:
            direction_z = delta[2] / abs(delta[2])  # up or down
            target[2] = position[2] + direction_z * max_step_distance_z

        return target
