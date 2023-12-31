import numpy as np
from ultralytics import YOLO
from PIL import Image
#from pybboxes import BoundingBox


def get_iou(ground_truth, pred):
    # coordinates of the area of intersection.
    ix1 = np.maximum(ground_truth[0], pred[0])
    iy1 = np.maximum(ground_truth[1], pred[1])
    ix2 = np.minimum(ground_truth[2], pred[2])
    iy2 = np.minimum(ground_truth[3], pred[3])

    # Intersection height and width.
    i_height = np.maximum(iy2 - iy1 + 1, np.array(0.))
    i_width = np.maximum(ix2 - ix1 + 1, np.array(0.))

    area_of_intersection = i_height * i_width

    # Ground Truth dimensions.
    gt_height = ground_truth[3] - ground_truth[1] + 1
    gt_width = ground_truth[2] - ground_truth[0] + 1

    # Prediction dimensions.
    pd_height = pred[3] - pred[1] + 1
    pd_width = pred[2] - pred[0] + 1

    area_of_union = gt_height * gt_width + pd_height * pd_width - area_of_intersection

    iou = area_of_intersection / area_of_union

    return iou


def should_click(boxResults, fullGrid):
    shouldClick = []
    for gridBox in fullGrid:
        for items in boxResults:
            if get_iou(gridBox, items) > 0.04:
                print(get_iou(gridBox, items))
                shouldClick.append(gridBox)
    return shouldClick


def make_unique_should_click(should_click_array):
    unique_shouldClick = []
    for item in should_click_array:
        if item not in unique_shouldClick:
            unique_shouldClick.append(item)
    return unique_shouldClick


def boxClick(boxesTuple, fullGrid):
    clickArray = []
    for gridBox in fullGrid:
        if gridBox in boxesTuple:
            clickArray.append(True)
        else:
            clickArray.append(False)
    return clickArray


def get_click_array(classNbr):
    # Load YOLOv8n-seg, train it on COCO128-seg for 3 epochs and predict an image with it    
    model = YOLO('yolov8m-seg.pt')  # load a pretrained YOLOv8n segmentation model
    model.train(data='coco128-seg.yaml', epochs=3)  # train the model
    results = model('payload4.jpg')  # predict on an image
    result = results[0]

    img = Image.fromarray(result.plot()[:, :, ::-1])

    img.show()

    model = YOLO("yolov8m.pt")

    # results = model.predict("payload4.jpg")
    results = model.predict(source="payload.jpg", retina_masks=True, save=True, classes=[classNbr, classNbr])


    result = results[0]


    boxResults = []
    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        boxResults.append(cords)
        cords = [round(x) for x in cords]
        conf = round(box.conf[0].item(), 2)
        # print("Object type:", class_id)
        # print("Coordinates:", cords)
        # print("Probability:", conf)
        # print("---")

    img = Image.fromarray(result.plot()[:, :, ::-1])

    # img.show()

    width = img.size[0]
    height = img.size[1]
    # left, upper, right, lower
    C1R1 = [0, 0, width / 4, height / 4]
    C2R1 = [width / 4, 0, width / 4 * 2, height / 4]
    C3R1 = [width / 4 * 2, 0, width / 4 * 3, height / 4]
    C4R1 = [width / 4 * 3, 0, width, height / 4]
    C1R2 = [0, height / 4, width / 4, height / 4 * 2]
    C2R2 = [width / 4, height / 4, width / 4 * 2, height / 4 * 2]
    C3R2 = [width / 4 * 2, height / 4, width / 4 * 3, height / 4 * 2]
    C4R2 = [width / 4 * 3, height / 4, width, height / 4 * 2]
    C1R3 = [0, height / 4 * 2, width / 4, height / 4 * 3]
    C2R3 = [width / 4, height / 4 * 2, width / 4 * 2, height / 4 * 3]
    C3R3 = [width / 4 * 2, height / 4 * 2, width / 4 * 3, height / 4 * 3]
    C4R3 = [width / 4 * 3, height / 4 * 2, width, height / 4 * 3]
    C1R4 = [0, height / 4 * 3, width / 4, height]
    C2R4 = [width / 4, height / 4 * 3, width / 4 * 2, height]
    C3R4 = [width / 4 * 2, height / 4 * 3, width / 4 * 3, height]
    C4R4 = [width / 4 * 3, height / 4 * 3, width, height]

    fullGrid = [C1R1, C2R1, C3R1, C4R1,
                C1R2, C2R2, C3R2, C4R2,
                C1R3, C2R3, C3R3, C4R3,
                C1R4, C2R4, C3R4, C4R4]

    shouldClick = should_click(boxResults, fullGrid)
    unique = make_unique_should_click(shouldClick)
    boxesArray = boxClick(unique, fullGrid)
    print(boxesArray)
    return boxesArray


# get_click_array("img")
