"""
main_demo.py
Member 3 — Game Core Developer (Track & Player)

Standalone demo of the lane + player system, controlled with the mouse
instead of a real hand gesture. This lets us test/tune lane snapping and
boost visuals before Member 5 wires up the real YOLO hand-tracking feed.

--------------------------------------------------------------------------
Integration contract for Member 5 (replaces the mouse callback below):

    lane_system = LaneSystem(frame_width=640, num_lanes=4)
    player = Player(lane_system)

    # each frame, once YOLO gives the "steer" (open palm) bounding box (x1,y1,x2,y2):
    hand_center_x = (x1 + x2) / 2
    player.update_from_hand_x(hand_center_x)
    player.update_boost_state()

    # when the "boost" (peace sign) gesture is detected AND nitro is available
    # (nitro/points bookkeeping lives in Member 4's obstacle/power-up module):
    player.trigger_boost()
--------------------------------------------------------------------------
"""

import cv2
import numpy as np

from lanes import LaneSystem
from player import Player

WIDTH, HEIGHT = 640, 480
NUM_LANES = 4

mouse_x = WIDTH // 2


def on_mouse(event, x, y, flags, param):
    global mouse_x
    mouse_x = x


def main():
    lane_system = LaneSystem(frame_width=WIDTH, num_lanes=NUM_LANES)
    player = Player(lane_system)

    cv2.namedWindow("Kachow! Lane Demo")
    cv2.setMouseCallback("Kachow! Lane Demo", on_mouse)

    print("Move the mouse left/right to steer McQueen between lanes.")
    print("Press 'b' to trigger a boost. Press '+/-' to change lane count. Press 'q' to quit.")

    while True:
        frame = np.full((HEIGHT, WIDTH, 3), 30, dtype=np.uint8)

        lane_system.draw_lanes(frame)

        # --- stand-in for Member 5's real YOLO hand x-coordinate ---
        player.update_from_hand_x(mouse_x)
        player.update_boost_state()
        player.draw(frame)

        cv2.putText(frame, f"Lane: {player.current_lane}/{lane_system.num_lanes - 1}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Kachow! Lane Demo", frame)
        key = cv2.waitKey(16) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            player.trigger_boost()
        elif key == ord('+') and lane_system.num_lanes < 8:
            lane_system.set_num_lanes(lane_system.num_lanes + 1)
        elif key == ord('-') and lane_system.num_lanes > 2:
            lane_system.set_num_lanes(lane_system.num_lanes - 1)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
