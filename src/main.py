import cv2
from ultralytics import YOLO

from lanes import LaneSystem
from player import Player
from game_logic import GameLogic
from config import (
    FRAME_WIDTH,
    FRAME_HEIGHT,
    NUM_LANES,
    SMOOTHING,
    PLAYER_Y_RATIO,
    PLAYER_SIZE
)


# ============================================================
# 1. LOAD YOLO MODEL
# ============================================================

model = YOLO("models/best.pt")


# ============================================================
# 2. CREATE GAME OBJECTS
# ============================================================

lane_system = LaneSystem(
    frame_width=FRAME_WIDTH,
    num_lanes=NUM_LANES
)

player = Player(
    lane_system,
    smoothing=SMOOTHING,
    y_ratio=PLAYER_Y_RATIO,
    size=PLAYER_SIZE
)

game = GameLogic(
    lane_system,
    player,
    FRAME_HEIGHT,
    FRAME_WIDTH
)


# ============================================================
# 3. OPEN CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()


# ============================================================
# 4. YOLO SETTINGS
# ============================================================

CONFIDENCE_THRESHOLD = 0.5


# ============================================================
# 5. GESTURE STATE
# ============================================================

previous_gesture = None


# ============================================================
# 6. MAIN GAME LOOP
# ============================================================

while True:

    # --------------------------------------------------------
    # Get frame from camera
    # --------------------------------------------------------

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break


    # --------------------------------------------------------
    # Resize frame to game resolution
    # --------------------------------------------------------

    frame = cv2.resize(
        frame,
        (FRAME_WIDTH, FRAME_HEIGHT)
    )


    # --------------------------------------------------------
    # Run YOLO
    # --------------------------------------------------------

    results = model(
        frame,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False
    )


    # --------------------------------------------------------
    # Current detected gesture
    # --------------------------------------------------------

    current_gesture = None

    # Store best detection for steering
    best_open_palm_confidence = 0.0
    best_open_palm_bbox = None

    # Store best Peace Sign confidence
    best_peace_confidence = 0.0


    # ========================================================
    # 7. PROCESS YOLO DETECTIONS
    # ========================================================

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            # ------------------------------------------------
            # Confidence
            # ------------------------------------------------

            confidence = float(box.conf[0])

            if confidence < CONFIDENCE_THRESHOLD:
                continue


            # ------------------------------------------------
            # Class ID
            # ------------------------------------------------

            class_id = int(box.cls[0])


            # ------------------------------------------------
            # Get class name from YOLO
            # ------------------------------------------------

            class_name = result.names[class_id]

            class_name = class_name.lower().replace(" ", "_")


            # ------------------------------------------------
            # Bounding box
            # ------------------------------------------------

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)


            # =================================================
            # OPEN PALM
            # =================================================

            if class_name in ["open_palm", "palm"]:

                if confidence > best_open_palm_confidence:

                    best_open_palm_confidence = confidence

                    best_open_palm_bbox = (
                        x1,
                        y1,
                        x2,
                        y2
                    )


            # =================================================
            # PEACE SIGN
            # =================================================

            elif class_name in ["peace_sign", "peace"]:

                if confidence > best_peace_confidence:

                    best_peace_confidence = confidence


            # ------------------------------------------------
            # Draw YOLO bounding box
            # ------------------------------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"{class_name} {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


    # ========================================================
    # 8. DECIDE WHICH GESTURE IS ACTIVE
    # ========================================================

    if best_peace_confidence > 0:

        current_gesture = "peace_sign"

    elif best_open_palm_bbox is not None:

        current_gesture = "open_palm"


    # ========================================================
    # 9. OPEN PALM → STEERING
    # ========================================================

    if current_gesture == "open_palm":

        x1, y1, x2, y2 = best_open_palm_bbox

        # Calculate center of hand bounding box
        hand_center_x = (x1 + x2) / 2

        # Send X position to Player
        player.update_from_hand_x(hand_center_x)


    # ========================================================
    # 10. PEACE SIGN → BOOST
    # ========================================================

    elif current_gesture == "peace_sign":

        # Only trigger when Peace Sign appears
        # and a boost is not already active.

        if previous_gesture != "peace_sign":

            if not player.boost_active:

                game.trigger_boost()


    # ========================================================
    # 11. REMEMBER CURRENT GESTURE
    # ========================================================

    previous_gesture = current_gesture


    # ========================================================
    # 12. UPDATE PLAYER BOOST
    # ========================================================

    player.update_boost_state()


    # ========================================================
    # 13. UPDATE GAME
    # ========================================================

    game.update()


    # ========================================================
    # 14. DRAW GAME
    # ========================================================

    lane_system.draw_lanes(frame)

    player.draw(frame)

    game.draw(frame)


    # ========================================================
    # 15. DISPLAY CURRENT GESTURE
    # ========================================================

    if current_gesture is not None:

        cv2.putText(
            frame,
            f"Gesture: {current_gesture}",
            (FRAME_WIDTH - 250, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

    else:

        cv2.putText(
            frame,
            "Gesture: None",
            (FRAME_WIDTH - 250, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


    # ========================================================
    # 16. DISPLAY GAME
    # ========================================================

    cv2.imshow(
        "Lightning McQueen - Piston Cup Dash",
        frame
    )


    # ========================================================
    # 17. KEYBOARD CONTROLS
    # ========================================================

    key = cv2.waitKey(1) & 0xFF


    # Quit
    if key == ord("q"):

        break


    # Restart
    elif key == ord("r") or key == ord("R"):

        game.reset_game()

        player.boost_active = False

        previous_gesture = None

        print("Game restarted.")


# ============================================================
# 18. CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()