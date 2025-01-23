import cv2
from fastapi import HTTPException
import HandTrackingDynamic as htd
from PIL import Image
import numpy as np
from keras import models
import random as rng


def resize():
    img = Image.open('parse.png')
    img = img.convert("RGB")
    img = img.resize((128, 128), Image.LANCZOS)
    print("finished resize and recoloration")
    return np.array(img) / 255.0


# Converts parse.png to a green background
def greenBg(val):
    color = (255, 255, 255)
    threshold = val
    img = cv2.imread('parse.png')
    padding = 1
    img = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    src_gray = cv2.blur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (3, 3))

    # Detect edges using Canny
    canny_output = cv2.Canny(src_gray, threshold, threshold * 2)

    # Find contours
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(contours)):
        hull = cv2.convexHull(contours[i])
        hull_list.append(hull)

    # Draw contours + hull results
    mask = np.zeros((canny_output.shape[0], canny_output.shape[1]), dtype=np.uint8)

    # Draw filled contours on the mask
    # TODO May need to reduce background noise
    for i in range(len(contours)):
        cv2.drawContours(mask, contours, i, 255, -1)

    # Use the mask to keep only the relevant parts of the image
    # TODO Mask is not working and not cropping out the part of the image
    result = cv2.bitwise_and(img, img, mask=mask)

    # Save the results
    cv2.imwrite('hull.png', result)






def analyze():
    print("running analyze")
    model = models.load_model('rpsModel.keras')
    detector = htd.HandTrackingDynamic()
    img = cv2.imread('handFrame.png')
    frame = detector.findFingers(img, draw=False)
    lmsList, bbox = detector.findPosition(frame, handDraw=False)
    # bbox should contain the bounding where the hand is
    # lmsList contains the coordinates for the hands
    if len(bbox) == 0:
        raise HTTPException(status_code=400, detail="No hand detected")
    xmin, ymin, xmax, ymax = bbox
    # TODO Take img here and mask it with a green background
    # Img should be in handFrame.png
    handFrame = img[max(0, ymin - 25):ymax + 25, max(0, xmin - 25):xmax + 25]
    cv2.imwrite('parse.png', handFrame)
    greenBg(75)
    prediction = model.predict(np.expand_dims(resize(), axis=0))
    PAPER, ROCK, SCISSORS = prediction[0][0], prediction[0][1], prediction[0][2]
    winning, prob = None, None
    print(prediction)

    if ROCK > PAPER and ROCK > SCISSORS:
        winning = "Rock"
        prob = ROCK
    elif PAPER > ROCK and PAPER > SCISSORS:
        winning = "Paper"
        prob = PAPER
    else:
        winning = "Scissors"
        prob = SCISSORS

    return {"rps": winning, "prob": round(prob.item(), 2), "rock": round(ROCK.item(), 2),
            "paper": round(PAPER.item(), 2),
            "scissors": round(SCISSORS.item(), 2)}


# running for test
if __name__ == "__main__":
    analyze()
