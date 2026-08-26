"""
main_demo.py
by member4
"""

import cv2
import numpy as np

from lanes import LaneSystem
from player import Player
from game_logic import GameLogic
from config import FRAME_WIDTH, FRAME_HEIGHT, NUM_LANES, SMOOTHING, PLAYER_Y_RATIO

mouse_x = FRAME_WIDTH // 2

def on_mouse(event, x, y, flags, param):
    global mouse_x
    mouse_x = x

def main():
    lane_system = LaneSystem(frame_width=FRAME_WIDTH, num_lanes=NUM_LANES)
    player = Player(lane_system, smoothing=SMOOTHING, y_ratio=PLAYER_Y_RATIO)
    game = GameLogic(lane_system, player, FRAME_HEIGHT, FRAME_WIDTH)

    cv2.namedWindow("Kachow Piston Cup Dash (Demo)")
    cv2.setMouseCallback("Kachow Piston Cup Dash (Demo)", on_mouse)

    print("Move mouse left/right to steer.")
    print("  Press 'b' for Boost. Press '+/-' for lanes. Press 'q' to quit.")

    while True:
        frame = np.full((FRAME_HEIGHT, FRAME_WIDTH, 3), 30, dtype=np.uint8)

        lane_system.draw_lanes(frame)
        player.update_from_hand_x(mouse_x)
        player.update_boost_state()
        game.update()

        player.draw(frame)
        game.draw(frame)

        cv2.putText(frame, f"Lane: {player.current_lane}/{lane_system.num_lanes - 1}",
                    (FRAME_WIDTH - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        boost_status = "ON" if player.boost_active else "OFF"
        cv2.putText(frame, f"Boost: {boost_status}", (FRAME_WIDTH - 200, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Kachow Piston Cup Dash (Demo)", frame)
        key = cv2.waitKey(16) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('b'):
            game.trigger_boost()
        elif key == ord('+') and lane_system.num_lanes < 8:
            lane_system.set_num_lanes(lane_system.num_lanes + 1)
        elif key == ord('-') and lane_system.num_lanes > 2:
            lane_system.set_num_lanes(lane_system.num_lanes - 1)
        elif key == ord('r') or key == ord('R'):
            game.reset_game()
            player.boost_active = False  # Reset boost state too
            print(" Press 'R' to restart...")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()