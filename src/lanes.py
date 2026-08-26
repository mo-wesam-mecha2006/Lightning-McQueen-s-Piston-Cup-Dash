"""
lanes.py
Member 3 — Game Core Developer (Track & Player)

Divides the game frame into `num_lanes` equal vertical lanes and provides
helpers to convert between a raw x pixel coordinate (e.g. the center of the
YOLO "steer" bounding box) and a lane index.
"""

import cv2


class LaneSystem:
    def __init__(self, frame_width: int, num_lanes: int = 4):
        """
        frame_width: width of the camera / game frame in pixels
        num_lanes:   how many vertical lanes to divide the track into
                     (customizable difficulty — more lanes = harder to steer precisely)
        """
        self.frame_width = frame_width
        self.num_lanes = num_lanes
        self.lane_width = frame_width / num_lanes

    def set_num_lanes(self, num_lanes: int):
        """Change difficulty at runtime (e.g. from a settings menu)."""
        self.num_lanes = num_lanes
        self.lane_width = self.frame_width / num_lanes

    def x_to_lane(self, x: float) -> int:
        """Map a raw pixel x-coordinate to a lane index, clamped to valid range."""
        lane = int(x // self.lane_width)
        return max(0, min(self.num_lanes - 1, lane))

    def lane_center_x(self, lane_index: int) -> int:
        """Return the pixel x-coordinate of the center of a given lane."""
        lane_index = max(0, min(self.num_lanes - 1, lane_index))
        return int(lane_index * self.lane_width + self.lane_width / 2)

    def random_lane(self) -> int:
        """Used by Member 4 to spawn obstacles/power-ups in a random lane."""
        import random
        return random.randint(0, self.num_lanes - 1)

    def lane_boundaries(self):
        """Pixel x-coordinates of the vertical lines separating lanes (including edges)."""
        return [int(i * self.lane_width) for i in range(self.num_lanes + 1)]

    def draw_lanes(self, frame, color=(80, 80, 80), thickness=2):
        """Draw the lane divider lines onto a frame (for debugging / the game HUD)."""
        h = frame.shape[0]
        for x in self.lane_boundaries()[1:-1]:
            cv2.line(frame, (x, 0), (x, h), color, thickness)
        return frame
