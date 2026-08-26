"""
player.py
Member 3 — Game Core Developer (Track & Player)

McQueen's on-screen representation. Continuously tracks the "steer" gesture's
x-position and smoothly snaps to the nearest lane, instead of teleporting.
Boost state (set by Member 4's Kachow Boost logic) is only read here for
rendering — this module doesn't own the nitro/points logic.
"""

import time
import cv2


class Player:
    def __init__(self, lane_system, start_lane: int = None,
                 y_ratio: float = 0.85, size: int = 60, smoothing: float = 0.25):
        """
        lane_system: a LaneSystem instance (see lanes.py)
        start_lane:  lane McQueen starts in (defaults to the middle lane)
        y_ratio:     vertical position as a fraction of frame height (near bottom)
        size:        width/height of McQueen's icon in pixels
        smoothing:   0..1, how quickly McQueen glides to the target lane
                     (1 = instant snap, lower = smoother glide)
        """
        self.lanes = lane_system
        self.current_lane = start_lane if start_lane is not None else lane_system.num_lanes // 2
        self.y_ratio = y_ratio
        self.size = size
        self.smoothing = smoothing
        self.x = float(self.lanes.lane_center_x(self.current_lane))
        self.target_x = self.x

        # Boost is triggered externally (Member 4's logic); this class just
        # tracks the state for drawing feedback (glow/trail).
        self.boost_active = False
        self.boost_end_time = 0.0

    def update_from_hand_x(self, hand_x: float):
        """Call every frame with the center-x of the YOLO 'steer' (open palm) bbox."""
        self.current_lane = self.lanes.x_to_lane(hand_x)
        self.target_x = self.lanes.lane_center_x(self.current_lane)
        # smooth interpolation toward the target lane's center
        self.x += (self.target_x - self.x) * self.smoothing

    def trigger_boost(self, duration: float = 1.5):
        """Called by Member 4's Kachow Boost logic when nitro is consumed."""
        self.boost_active = True
        self.boost_end_time = time.time() + duration

    def update_boost_state(self) -> bool:
        """Call once per frame to expire the boost window automatically."""
        if self.boost_active and time.time() >= self.boost_end_time:
            self.boost_active = False
        return self.boost_active

    def get_bbox(self, frame_height: int):
        """Returns (x1, y1, x2, y2) — used by Member 4 for collision checks."""
        y = int(frame_height * self.y_ratio)
        half = self.size // 2
        x = int(self.x)
        return (x - half, y - half, x + half, y + half)

    def draw(self, frame):
        h = frame.shape[0]
        x1, y1, x2, y2 = self.get_bbox(h)
        color = (0, 215, 255) if self.boost_active else (0, 0, 255)  # gold glow on boost
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        if self.boost_active:
            cv2.circle(frame, (int(self.x), (y1 + y2) // 2), self.size, (0, 200, 255), 2)
        return frame
