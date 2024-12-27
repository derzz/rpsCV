import cv2
import time

import mediapipe.python.solutions.hands as hands
import HandTrackingDynamic as htd

tip = [8, 12, 16, 20]
mid = [6, 10, 14, 18]
# Order of index, middle, ring, and pinky fingers
fingers = []
finger = []

HandsModule = hands.Hands()
def nameOfLandMark(frame1):
    list = []
    results = HandsModule.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks is not None:
        for handLandmarks in results.multi_hand_landmarks:
            for point in hands.HandLandmark:
                list.append(
                    str(point).replace("< ", "").replace("HandLandmark.", "").replace("_", " ").replace("[]", ""))
    return list


# posList requires a list of points such as ([0, 1, 2], [1, 1, 2]...)
def gestureDetector(posList):
    if len(posList) == 0:
        return
    for id in range(0, 4):




def main():
    ctime = 0
    ptime = 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = htd.HandTrackingDynamic()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        frame1 = cv2.resize(frame, (640, 480))
        frame = detector.findFingers(frame)
        lmsList = detector.findPosition(frame)
        if len(lmsList) != 0:
            print(lmsList[0])
            ctime = time.time()
            fps = 1 / (ctime - ptime)
            ptime = ctime

            cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            if len(lmsList[0]) != 0:
                for i in lmsList[0]:
                    # Used for debugging and determining points on the hand
                    cv2.putText(frame, str(i[0]), (i[1] + 10, i[2] + 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 3)

            gestureDetector(lmsList[0])
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == "__main__":
    main()
