import cv2
import numpy as np
from PIL import Image
import pytesseract

def number_plate_detection(img):
    def clean2_plate(plate):
        gray_img = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_img, 110, 255, cv2.THRESH_BINARY)
        num_contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if num_contours:
            contour_area = [cv2.contourArea(c) for c in num_contours]
            max_cntr_index = np.argmax(contour_area)
            max_cnt = num_contours[max_cntr_index]
            x, y, w, h = cv2.boundingRect(max_cnt)
            if not ratioCheck(cv2.contourArea(max_cnt), w, h):
                return plate, None
            final_img = thresh[y:y+h, x:x+w]
            return final_img, [x, y, w, h]
        else:
            return plate, None

    def ratioCheck(area, width, height):
        ratio = float(width) / float(height)
        if ratio < 1:
            ratio = 1 / ratio
        return 1063.62 <= area <= 73862.5 and 3 <= ratio <= 6

    def isMaxWhite(plate):
        return np.mean(plate) >= 115

    def ratio_and_rotation(rect):
        (x, y), (width, height), rect_angle = rect
        angle = -rect_angle if width > height else 90 + rect_angle
        if angle > 15:
            return False
        return height != 0 and width != 0 and ratioCheck(height * width, width, height)

    img_blur = cv2.GaussianBlur(img, (5, 5), 0)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_sobel = cv2.Sobel(img_gray, cv2.CV_8U, 1, 0, ksize=3)
    _, img_thresh = cv2.threshold(img_sobel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
    morph_img_threshold = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel=element)
    num_contours, _ = cv2.findContours(morph_img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in num_contours:
        min_rect = cv2.minAreaRect(cnt)
        if ratio_and_rotation(min_rect):
            x, y, w, h = cv2.boundingRect(cnt)
            plate_img = img[y:y+h, x:x+w]
            if isMaxWhite(plate_img):
                clean_plate, rect = clean2_plate(plate_img)
                if rect:
                    x1, y1, w1, h1 = rect
                    x, y, w, h = x + x1, y + y1, w1, h1
                    plate_im = Image.fromarray(clean_plate)
                    return pytesseract.image_to_string(plate_im, lang='eng')
    return None
