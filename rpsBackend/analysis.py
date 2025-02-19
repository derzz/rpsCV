import cv2
from fastapi import HTTPException
import HandTrackingDynamic as htd
from PIL import Image
import numpy as np
from keras import models
import os

def findIfClose(cnt1, cnt2):
    row1, row2 = cnt1.shape[0], cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i] - cnt2[j])
            if abs(dist) < 5:
                return True
            elif i == row1 - 1 and j == row2 - 1:
                return False

def resize():
    img = Image.open('parse.png')
    img = img.convert("RGB")
    img = img.resize((128, 128), Image.LANCZOS)
    print("finished resize and recoloration")
    return np.array(img) / 255.0

def greenBgNew():
    img = cv2.imread('parse.png')
    im_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    skin_ycrcb_mint = np.array((0, 133, 77))
    skin_ycrcb_maxt = np.array((255, 173, 127))
    skin_ycrcb = cv2.inRange(im_ycrcb, skin_ycrcb_mint, skin_ycrcb_maxt)
    cv2.imwrite('bwImage.png', skin_ycrcb)  # Second image

    contours, _ = cv2.findContours(skin_ycrcb, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    '''
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        if area > 1000:
            cv2.drawContours(img, contours, i, (255, 0, 0), 3)
    
    '''
    # Create a mask with the same dimensions as the image
    mask = np.zeros_like(img)

    # Fill the contours on the mask
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Create a green background
    green_background = np.zeros_like(img)
    green_background[:] = (0, 255, 0)  # Green color

    # Combine the original image and the green background using the mask
    result = np.where(mask == (255, 255, 255), img, green_background)

    # Save the final result
    cv2.imwrite('parse.png', result)

# Converts parse.png to a green background by forming a mask of the image
def greenBg(val):
    # Load image
    img = cv2.imread('parse.png')

    src_gray = cv2.blur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (10, 10))

    # Detect edges using Canny
    threshold = val
    canny_output = cv2.Canny(src_gray, threshold, threshold * 2)

    # Dilate to close small gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.dilate(canny_output, kernel, iterations=8)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a blank mask
    mask = np.zeros_like(src_gray, dtype=np.uint8)

    # Filter and draw only large contours
    for contour in contours:
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

    # Apply morphological closing to fill gaps
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Apply flood fill to ensure interior gaps are filled
    h, w = mask.shape
    flood_fill_mask = mask.copy()
    cv2.floodFill(flood_fill_mask, None, (w//2, h//2), 255)

    # Combine original mask and flood-filled regions
    filled_mask = cv2.bitwise_or(mask, flood_fill_mask)

    # Save the mask
    cv2.imwrite('mask.png', filled_mask)

    # Create a green background
    green_background = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    green_background[:] = (0, 255, 0)  # Green color

    # Apply the mask to the original image
    result = cv2.bitwise_and(img, img, mask=filled_mask)

    # Combine result with the green background
    green_bg_result = np.where(filled_mask[:, :, None] == 255, result, green_background)

    # Save the final result
    cv2.imwrite('parse.png', green_bg_result)






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
    # Img should be in handFrame.png
    handFrame = img[max(0, ymin - 25):ymax + 25, max(0, xmin - 25):xmax + 25]
    cv2.imwrite('parse.png', handFrame)
    # greenBgNew()
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

    os.remove('./handFrame.png')
    os.remove('./parse.png')

    return {"rps": winning, "prob": round(prob.item(), 2), "rock": round(ROCK.item(), 2),
            "paper": round(PAPER.item(), 2),
            "scissors": round(SCISSORS.item(), 2)}


# running for test
if __name__ == "__main__":
    analyze()
