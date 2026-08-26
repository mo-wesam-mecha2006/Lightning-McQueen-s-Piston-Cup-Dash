"""
game_logic.py
Member 4 — Game Logic Developer

Manages obstacles, power-ups, collisions, score, lives, and the Boost system.
Includes Game Over logic and restart functionality.
"""

import random
import time
import cv2

from config import (
    OBSTACLE_WIDTH,
    OBSTACLE_HEIGHT,
    POWERUP_WIDTH,
    POWERUP_HEIGHT,
    INITIAL_LIVES,
    GAME_SPEED,
    SPAWN_INTERVAL,
    BOOST_DURATION,
    FRAME_HEIGHT,
    FRAME_WIDTH
)

class Obstacle:
    def __init__(self, lane, y=0, width=OBSTACLE_WIDTH, height=OBSTACLE_HEIGHT):
        self.lane = lane
        self.y = y
        self.width = width
        self.height = height
        self.active = True

    def move(self, speed):
        self.y += speed

    def get_bbox(self, lane_system):
        center_x = lane_system.lane_center_x(self.lane)
        half_w = self.width // 2
        half_h = self.height // 2
        return (center_x - half_w, self.y - half_h,
                center_x + half_w, self.y + half_h)


class PowerUp:
    def __init__(self, lane, y=0, width=POWERUP_WIDTH, height=POWERUP_HEIGHT):
        self.lane = lane
        self.y = y
        self.width = width
        self.height = height
        self.active = True

    def move(self, speed):
        self.y += speed

    def get_bbox(self, lane_system):
        center_x = lane_system.lane_center_x(self.lane)
        half_w = self.width // 2
        half_h = self.height // 2
        return (center_x - half_w, self.y - half_h,
                center_x + half_w, self.y + half_h)


class GameLogic:
    def __init__(self, lane_system, player, frame_height=FRAME_HEIGHT, frame_width=FRAME_WIDTH):
        self.lanes = lane_system
        self.player = player
        self.frame_height = frame_height
        self.frame_width = frame_width

        self.obstacles = []
        self.powerups = []
        self.nitro_points = 0
        self.score = 0

        # Game state
        self.game_over = False  # NEW: Track if game is over

        # Spawning settings
        self.spawn_timer = 0
        self.spawn_interval = SPAWN_INTERVAL
        self.speed = GAME_SPEED

        # Lives (will be reset in reset_game())
        self.lives = INITIAL_LIVES

    def reset_game(self):
        """Reset everything to start a new game."""
        self.obstacles.clear()
        self.powerups.clear()
        self.nitro_points = 0
        self.score = 0
        self.lives = INITIAL_LIVES
        self.game_over = False
        self.spawn_timer = 0
        print("Game Restarted")

    def spawn_item(self):
        if self.game_over:
            return  # Don't spawn if game is over
        lane = self.lanes.random_lane()
        if random.random() < 0.5:
            self.obstacles.append(Obstacle(lane, y=0))
        else:
            self.powerups.append(PowerUp(lane, y=0))

    def update(self):
        # If game is over, stop all updates (freeze the screen)
        if self.game_over:
            return

        # 1. Spawn
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_item()

        # 2. Move obstacles
        for obs in self.obstacles[:]:
            obs.move(self.speed)
            if obs.y > self.frame_height + 50:
                self.obstacles.remove(obs)

        # 3. Move powerups
        for p in self.powerups[:]:
            p.move(self.speed)
            if p.y > self.frame_height + 50:
                self.powerups.remove(p)

        # 4. Get player bbox
        player_bbox = self.player.get_bbox(self.frame_height)
        px1, py1, px2, py2 = player_bbox

        # 5. Collision with obstacles
        for obs in self.obstacles[:]:
            ox1, oy1, ox2, oy2 = obs.get_bbox(self.lanes)
            if (px1 < ox2 and px2 > ox1 and py1 < oy2 and py2 > oy1):
                if not self.player.boost_active:
                    self.lives -= 1
                    print(f" Collision lives left: {self.lives}")

                    # --- NEW: Check if game over ---
                    if self.lives <= 0:
                        self.game_over = True
                        print(" GAME OVER Press 'R' to restart.")
                # Remove obstacle
                self.obstacles.remove(obs)

        # 6. Collect nitro
        for p in self.powerups[:]:
            ox1, oy1, ox2, oy2 = p.get_bbox(self.lanes)
            if (px1 < ox2 and px2 > ox1 and py1 < oy2 and py2 > oy1):
                self.nitro_points += 1
                self.score += 10
                print(f" Nitro collected Total: {self.nitro_points}")
                self.powerups.remove(p)

    def trigger_boost(self):
        if self.game_over:
            print(" Game is over. Restart first!")
            return False
        if self.nitro_points > 0:
            self.nitro_points -= 1
            self.player.trigger_boost(duration=BOOST_DURATION)
            print(" Kachow Boost Activated!")
            return True
        else:
            print(" No nitro to boost!")
            return False

    def draw(self, frame):
        # Draw obstacles
        for obs in self.obstacles:
            x1, y1, x2, y2 = obs.get_bbox(self.lanes)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), -1)

        # Draw powerups
        for p in self.powerups:
            x1, y1, x2, y2 = p.get_bbox(self.lanes)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), -1)

        # HUD
        cv2.putText(frame, f"Lives: {self.lives}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Nitro: {self.nitro_points}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Score: {self.score}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # --- NEW: Game Over overlay ---
        if self.game_over:
            overlay = frame.copy()
            cv2.rectangle(overlay, (50, 150), (self.frame_width - 50, 250), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            cv2.putText(frame, "GAME OVER", (self.frame_width // 2 - 120, 200),
                        cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), 3)
            cv2.putText(frame, "Press 'R' to Restart", (self.frame_width // 2 - 130, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return frame