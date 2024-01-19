# RE-WRITER/WRITER: LauNT # EMAIL: ttruongllau@gmail.com 

import numpy as np


def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)

    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2

    return y


def post_processing_output(output, img_shape, 
                           model_shape, 
                           conf_threshold=0.5, iou_threshold=0.1):
    # Post-processing model output

    predictions = np.squeeze(output[0]).T
    scores = np.max(predictions[:, 4:], axis=1)
    predictions = predictions[scores > conf_threshold, :]
    scores = scores[scores > conf_threshold]

    if len(scores) == 0:
        return [], [], []

    # get the class with the highest confidence
    class_ids = np.argmax(predictions[:, 4:], axis=1)

    # get bounding boxes for each object
    boxes = extract_boxes(predictions, img_shape, model_shape)
    indices = nms(boxes, scores, iou_threshold)

    return boxes[indices], scores[indices], class_ids[indices]


def extract_boxes(predictions, img_shape, model_shape):
    # Extract boxes from predictions

    boxes = predictions[:, :4]

    # scale boxes to original image dimensions
    boxes = rescale_boxes(boxes, img_shape, model_shape)
    boxes = xywh2xyxy(boxes)

    return boxes


def rescale_boxes(boxes, img_shape, model_shape):
    # Rescale boxes to original image dimensions

    model_w, model_h = model_shape
    img_w, img_h = img_shape
    
    input_shape = np.array([model_w, model_h, model_w, model_h])
    boxes = np.divide(boxes, input_shape, dtype=np.float32)
    boxes *= np.array([img_w, img_h, img_w, img_h])

    return boxes


def compute_iou(box, boxes):
    # Compute xmin, ymin, xmax, ymax for both boxes

    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])

    # compute intersection area
    intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    # compute union area
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union_area = box_area + boxes_area - intersection_area

    # compute IoU
    iou = intersection_area / union_area

    return iou


def nms(boxes, scores, iou_threshold):
    # Non-maximum Suppression

    sorted_indices = np.argsort(scores)[::-1]
    keep_boxes = []

    while sorted_indices.size > 0:
        # pick the last box
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # remove boxes with IoU over the threshold
        keep_indices = np.where(ious < iou_threshold)[0]
        sorted_indices = sorted_indices[keep_indices + 1]

    return keep_boxes