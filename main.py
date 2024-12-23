import os
import glob
import re
from number_plate.detection import number_plate_detection
from number_plate.utils import quickSort, binarySearch

def main():
    print("HELLO!!")
    print("Welcome to the Number Plate Detection System.\n")

    array = []

    dir_path = os.path.dirname(__file__)

    # Detecting number plates in Images
    for img_path in glob.glob(os.path.join(dir_path, "data/Images/*.jpeg")):
        img = cv2.imread(img_path)
        img_resized = cv2.resize(img, (600, 600))
        cv2.imshow("Image of car", img_resized)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

        number_plate = number_plate_detection(img)
        res2 = str("".join(re.split("[^a-zA-Z0-9]*", number_plate))).upper()
        print(res2)

        array.append(res2)

    # Sorting detected plates
    array = quickSort(array, 0, len(array) - 1)
    print("\n\nThe Vehicle numbers registered are:-")
    for plate in array:
        print(plate)
    print("\n\n")

    # Searching for a specific plate
    for img_path in glob.glob(os.path.join(dir_path, "data/search/*.jpeg")):
        img = cv2.imread(img_path)
        number_plate = number_plate_detection(img)
        res2 = str("".join(re.split("[^a-zA-Z0-9]*", number_plate)))
    
    print("The car number to search is:", res2)
    result = binarySearch(array, 0, len(array) - 1, res2)

    if result != -1:
        print("\n\nThe Vehicle is allowed to visit.")
    else:
        print("\n\nThe Vehicle is not allowed to visit.")

if __name__ == "__main__":
    main()
