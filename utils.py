import tensorflow as tf
import time
import numpy as np

# Dictionary that maps from joint names to keypoint indices.
KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

interpreter = tf.lite.Interpreter(model_path="lite-model_movenet_singlepose_thunder_tflite_float16_4.tflite")
interpreter.allocate_tensors()

def movenet(image_array):
    """Runs detection on an input image.
    Args:
      input_array: A [height, width, 3] numpy array represents the input image
        pixels.
    Returns:
      A [17, 2] float numpy array representing the predicted keypoint coordinates.
    """
    input_image = tf.convert_to_tensor(image_array)
    input_image = tf.expand_dims(input_image, axis=0)
    input_image = tf.image.resize_with_pad(input_image, 256, 256)
    # TF Lite format expects tensor type of uint8.
    input_image = tf.cast(input_image, dtype=tf.uint8)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
    # Invoke inference.
    interpreter.invoke()
    # Get the model prediction.
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    return keypoints_with_scores[0,0,:,:2]


def distance(point, end1, end2):
    return abs(np.cross(end2 - end1, point - end1) / np.linalg.norm(end2 - end1))

def slope(end1, end2):
    return abs((end2[0] - end1[0]) / (end2[1] - end1[1]))

def angle(end1, end2, end3):
    vec1 = (end1 - end2) / np.linalg.norm(end1 - end2)
    vec2 = (end3 - end2) / np.linalg.norm(end3 - end2)
    return np.degrees(np.arccos(np.dot(vec1, vec2)))


def test_warrior(keypoints):
    problems = []
    if slope(keypoints[9], keypoints[10]) > 0.1:  # slope of line between two wrists
        problems.append('Arms not parallel to ground')
    if distance(keypoints[5], keypoints[9], keypoints[10]) > 0.1 or distance(keypoints[6], keypoints[9], keypoints[10]) > 0.05:  # distance between shoulders and line from hand to hand
        problems.append('Arms too low')
    if distance(keypoints[7], keypoints[9], keypoints[10]) > 0.1 or distance(keypoints[8], keypoints[9], keypoints[10]) > 0.01:  # distance between elbows and line from hand to hand
        problems.append('Elbows are bent')
    if distance(keypoints[13], keypoints[11], keypoints[15]) > 0.1:  # distance between knee and line between hip and ankle
        problems.append('Left leg not straight')
    if angle(keypoints[12], keypoints[14], keypoints[16]) > 135:  # angle between line knee-hip and knee-ankle
        problems.append('Right leg not bent enough')
    print(problems)
    return problems

def test_tree(keypoints):
    problems = []
    if distance(keypoints[13], keypoints[11], keypoints[15]) > 0.1:  # distance between knee and line between hip and ankle
        problems.append('Left leg not straight')
    if angle(keypoints[12], keypoints[14], keypoints[16]) > 135:  # angle between line knee-hip and knee-ankle
        problems.append('Right foot not high enough')
    if distance(keypoints[7], keypoints[5], keypoints[9]) > 0.1:  # distance between elbow and line from shoulder to wrist
        problems.append('Left arm not straight')
    if distance(keypoints[8], keypoints[6], keypoints[10]) > 0.1:  # distance between elbow and line from shoulder to wrist
        problems.append('Right arm not straight')
    if keypoints[9][0] > keypoints[7][0] or keypoints[10][0] > keypoints[8][0]:  # wrist above or below elbow
        problems.append('Arms not in the air')
    print(problems)
    return problems

TESTS = {
    'warrior': test_warrior,
    'tree': test_tree
}

image_path = 'images/94885683_630091017837369_7513148106968545568_n.jpg'
#image_path = 'images/new_dir1_8_yoga_197.jpg'

#t0 = time.time()
#pts = movenet(image_path)
#test_warrior(pts)
#t1 = time.time()
#print(t1-t0)