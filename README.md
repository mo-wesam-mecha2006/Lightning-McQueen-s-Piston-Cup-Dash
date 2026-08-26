# Kachow! Lightning McQueen's Piston Cup Dash

Real-time lane-dodging game controlled by hand gestures, detected with a
custom-trained YOLO model, built in OpenCV. (MIA Robotics — Electrical
Training 26/27, Task 9.2)

## How it works
McQueen's lane position is continuously tracked from the "steer" (open palm)
gesture — no clicking. Obstacles (tire debris / oil) and power-ups (nitro)
scroll down toward him; the "boost" (peace sign) gesture consumes nitro for
temporary invulnerability.

## Team & task division
| Member | Role | Responsibility |
|---|---|---|
| 1 | Dataset Lead | Collect & organize raw gesture images/video from all members |
| 2 | Annotation & Training Lead | Label data, train YOLO, export weights |
| 3 | Game Core Developer | Lane system, McQueen rendering, hand-x → lane mapping (`src/lanes.py`, `src/player.py`) |
| 4 | Game Logic Developer | Obstacles/power-ups, collision/pickup, Kachow Boost |
| 5 | Integration/Testing/Docs | Wire YOLO output into game loop, testing, repo/README, demo video |

## Repo structure
```
kachow-lane-dodge/
├── src/
│   ├── lanes.py        # LaneSystem — n-lane grid, x → lane mapping
│   ├── player.py        # Player (McQueen) — tracking, boost state, drawing
│   └── main_demo.py     # Mouse-controlled demo (stand-in until YOLO is wired in)
├── models/               # trained YOLO weights go here
├── data/                 # dataset (raw/annotated) goes here
├── assets/               # icons/images if any
├── requirements.txt
└── README.md
```

## Running the Member 3 demo (no camera needed yet)
```bash
pip install -r requirements.txt
cd src
python main_demo.py
```
Move the mouse left/right to steer, press `b` to trigger a boost, `+`/`-` to
change the number of lanes, `q` to quit.

## Integration point for YOLO (Member 5)
`Player.update_from_hand_x(x)` and `Player.trigger_boost()` are the only two
calls the YOLO integration loop needs — see the docstring at the top of
`src/main_demo.py`.

## Branching strategy
- `main` — always kept working/demo-able
- one feature branch per member, e.g. `dataset`, `training`, `game-core`,
  `game-logic`, `integration`
- open a PR into `main` when a part is working; small, frequent commits
  reflecting real milestones (not one giant final commit)

## Dataset — gesture photos/videos from the team
Everyone uploads their raw gesture samples (open palm + peace sign, varied
lighting/angles/backgrounds) here for Member 1 to collect and organize:

**Google Drive link:** _[paste link here]_

## Status / Challenges
_(fill in as we go — required for the README grading criteria)_
