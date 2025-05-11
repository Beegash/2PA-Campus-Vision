import cv2
import numpy as np
import time
from ultralytics import YOLO
from norfair import Detection, Tracker, draw_points
from datetime import datetime
from collections import deque
import matplotlib.pyplot as plt

model = YOLO("yolov8n.pt")
tracker = Tracker(distance_function="euclidean", distance_threshold=40)

person_times = {}
person_bag_map = {}
unattended_bags = {}
doluluk_log = deque(maxlen=100)
heatmap = np.zeros((10, 10))

# Parametreler
OTURMA_THRESHOLD = 180
DIST_THRESHOLD = 80
BAG_MATCH_THRESHOLD = 100
UNATTENDED_THRESHOLD = 30  # frame sayısı
TOTAL_CHAIRS_ESTIMATED = 10

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    boxes = results[0].boxes.data
    names = model.names

    chairs, persons_xy, bags = [], [], []

    for box in boxes:
        x1, y1, x2, y2, conf, cls = box
        cls_name = names[int(cls.item())]
        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

        if cls_name == "chair":
            chairs.append(((int(x1), int(y1), int(x2), int(y2)), (cx, cy)))
        elif cls_name == "person":
            persons_xy.append((cx, cy))
        elif cls_name in ["backpack", "handbag"]:
            bags.append((cx, cy))

    # Sahipsiz çanta analizi
    for bag in bags:
        owned = False
        for person in persons_xy:
            if np.linalg.norm(np.array(person) - np.array(bag)) < BAG_MATCH_THRESHOLD:
                owned = True
                break
        if not owned:
            if bag in unattended_bags:
                unattended_bags[bag] += 1
            else:
                unattended_bags[bag] = 1

            if unattended_bags[bag] > UNATTENDED_THRESHOLD:
                cv2.putText(frame, "SAHIPSIZ CANTA!", (bag[0] + 10, bag[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.circle(frame, bag, 12, (0, 0, 255), 3)
        else:
            if bag in unattended_bags:
                del unattended_bags[bag]

    # Sandalye durumu
    occupied_count = 0
    for chair_box, chair_center in chairs:
        state = "Bos"
        color = (128, 128, 128)
        for person in persons_xy:
            if np.linalg.norm(np.array(chair_center) - np.array(person)) < DIST_THRESHOLD:
                state = "Oturuluyor"
                color = (0, 255, 0)
                occupied_count += 1
                break
        else:
            for bag in bags:
                if np.linalg.norm(np.array(chair_center) - np.array(bag)) < DIST_THRESHOLD:
                    state = "Canta Var"
                    color = (0, 165, 255)
                    break

        x1, y1, x2, y2 = chair_box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, state, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Norfair takibi
    def yolo_to_norfair(results):
        detections = []
        for box in results[0].boxes.data:
            x1, y1, x2, y2, conf, cls = box
            if names[int(cls.item())] != "person":
                continue
            cx, cy = float((x1 + x2) / 2), float((y1 + y2) / 2)
            detections.append(Detection(points=np.array([[cx, cy]])))
        return detections

    tracked_objects = tracker.update(detections=yolo_to_norfair(results))
    current_time = time.time()

    for obj in tracked_objects:
        ID = obj.id
        x, y = obj.estimate[0]

        if ID not in person_times:
            person_times[ID] = current_time

        sure = current_time - person_times[ID]
        cv2.putText(frame, f"ID:{ID} - {int(sure)}s", (int(x), int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        # Bag eşleştirme
        closest_bag = None
        min_dist = float("inf")
        for bag in bags:
            dist = np.linalg.norm(np.array([x, y]) - np.array(bag))
            if dist < min_dist and dist < BAG_MATCH_THRESHOLD:
                closest_bag = bag
                min_dist = dist
        if closest_bag:
            person_bag_map[ID] = closest_bag

        if ID in person_bag_map:
            bx, by = person_bag_map[ID]
            cv2.circle(frame, (int(bx), int(by)), 10, (255, 0, 255), -1)
            cv2.putText(frame, f"ID:{ID} Bag", (int(bx), int(by) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

    frame = draw_points(frame, tracked_objects)

    # Doluluk, yoğunluk, ısı
    doluluk_orani = occupied_count / TOTAL_CHAIRS_ESTIMATED
    toplam_kisi = len(persons_xy)
    yogunluk_orani = toplam_kisi / TOTAL_CHAIRS_ESTIMATED
    doluluk_log.append((datetime.now(), doluluk_orani))

    cv2.putText(frame, f"Doluluk: %{int(doluluk_orani * 100)}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.putText(frame, f"Yogunluk: %{int(yogunluk_orani * 100)}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 200, 0), 2)

    for _ in tracked_objects:
        gx, gy = np.random.randint(0, 10), np.random.randint(0, 10)
        heatmap[gy][gx] += 1

    cv2.imshow("CampusVision - Akilli Sistem", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# Grafikler
zamanlar = [dt.strftime("%H:%M:%S") for dt, _ in doluluk_log]
oranlar = [oran for _, oran in doluluk_log]

fig, axes = plt.subplots(2, 1, figsize=(10, 10))
axes[0].plot(zamanlar, oranlar, marker="o")
axes[0].set_title("Zaman Bazli Doluluk Orani")
axes[0].set_ylabel("Doluluk")
axes[0].grid(True)

im = axes[1].imshow(heatmap, cmap='hot', interpolation='nearest')
axes[1].set_title("Alan Isı Haritasi")
plt.colorbar(im, ax=axes[1])
plt.tight_layout()
plt.show()

# Final mesaj
if yogunluk_orani > 1.0:
    print(" Ortam çok yoğun! Oturulacak yer kalmamış olabilir.")
elif yogunluk_orani < 0.5:
    print(" Ortam sakin. Oturmak için uygun.")
else:
    print(" Orta yoğunlukta. Oturmak için kısmen uygun.")