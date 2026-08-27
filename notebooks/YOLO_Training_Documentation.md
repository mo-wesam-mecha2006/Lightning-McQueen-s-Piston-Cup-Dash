# YOLO Hand Gesture Detection – Training Documentation

## 1. Model & Task

- **Model:** YOLO11n
- **Task:** Hand gesture detection for the racing game.
- **Classes:**
  - `0` → Open Palm
  - `1` → Peace Sign
- **Image size:** 640 × 640
- **GPU:** NVIDIA Tesla T4

### Control Mapping
- **Open Palm** → Steering
- **Peace Sign** → Boost

---

## 2. Initial Dataset

The initial dataset contained:

- **102** training images
- **27** validation images
- **102** training labels
- **27** validation labels

### Training Class Distribution

| Class | Count |
| :--- | :--- |
| **Open Palm** | 52 |
| **Peace Sign** | 51 |

The dataset was approximately balanced between the two classes.

---

## 3. Initial Training

### Configuration
- **Epochs:** 50
- **Image Size:** 640
- **Batch Size:** 16

The training completed successfully.

### Overall Results

| Metric | Score |
| :--- | :--- |
| **Precision** | 0.863 |
| **Recall** | 0.926 |
| **mAP50** | 0.920 |
| **mAP50-95** | 0.759 |

### Per-Class Performance

#### Open Palm
- **Precision:** 0.874
- **Recall:** 0.923
- **mAP50:** 0.940
- **mAP50-95:** 0.810

#### Peace Sign
- **Precision:** 0.852
- **Recall:** 0.929
- **mAP50:** 0.900
- **mAP50-95:** 0.708

> The initial training proved that the dataset, labels, YOLO configuration, and training pipeline were working correctly.

---

## 4. Validation & Testing

- **Validation Set Evaluation:** Tested on all 27 validation images with overall `mAP50: 0.920` and `Recall: 0.926`.
- **Real-World Webcam Test:**
  - **Open Palm** detection was generally stable.
  - **Peace Sign** was sometimes missed or incorrectly detected as *Open Palm*.

This indicated a gap between validation metrics and real-world webcam performance.

---

## 5. Experiment 2 – Augmentation

To improve Peace Sign detection, a second experiment was conducted with data augmentation.

### Configuration
- **Epochs:** 100
- **Patience:** 15
- **Image Size:** 640
- **Batch Size:** 16
- **Rotation:** ±15°
- **Horizontal Flip:** 0.5

*Early Stopping terminated training after 18 epochs (best result at epoch 3).*

### Results

| Metric | Score |
| :--- | :--- |
| **Precision** | 0.00335 |
| **Recall** | 0.964 |
| **mAP50** | 0.156 |
| **mAP50-95** | 0.0649 |

> **Conclusion:** Performance degraded significantly, so Experiment 2 was discarded.

---

## 6. Experiment 3 – 100 Epochs

A third experiment was run without heavy augmentation settings.

### Configuration
- **Epochs:** 100
- **Patience:** 20
- **Image Size:** 640
- **Batch Size:** 16

*Early Stopping stopped training at epoch 99. The best model was saved at epoch 79.*

### Overall Results

| Metric | Score |
| :--- | :--- |
| **Precision** | 0.977 |
| **Recall** | 0.809 |
| **mAP50** | 0.907 |
| **mAP50-95** | 0.762 |

### Peace Sign Specific Results

| Metric | Score |
| :--- | :--- |
| **Precision** | 0.955 |
| **Recall** | 0.643 |
| **mAP50** | 0.820 |
| **mAP50-95** | 0.633 |

> While precision improved, **Peace Sign recall** dropped lower than desired.

---

## 7. Current Conclusion

1. The YOLO training pipeline is robust and functioning properly.
2. The initial model remains the **strongest overall baseline** (`mAP50: 0.920`, `Recall: 0.926`).
3. **Core Challenge:** Peace Sign detection under live webcam conditions (misses and confusion with Open Palm).
4. **Root Cause:** The current training set is small (102 images), limiting real-world generalization.

---

## 8. New Data (P12 Set)

A new dataset batch **P12** was collected containing **50 additional images**.

### Next Steps:
- [ ] Bounding-box labeling
- [ ] Correct class assignment
- [ ] Integration into the primary YOLO dataset
- [ ] Retrain model and compare against baseline

---

## 9. Current Project Structure

```text
notebooks/
└── YOLO_Training.ipynb

models/
└── best.pt

src/
├── gesture_detection.py
└── camera_test.py
