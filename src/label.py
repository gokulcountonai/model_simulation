import json
import base64
import numpy as np
import cv2

class Shape:
    """
    Class for creating labelme format shapes.
    """

    def __init__(self):
        self.shape = {}
        self.shape['label'] = ''
        self.shape['points'] = []
        self.shape['group_id'] = None
        self.shape['description'] = ""
        self.shape['shape_type'] = 'rectangle'
        self.shape['flags'] = {}

    def add_label(self, label):
        """
        Add label to the shape.
        """
        self.shape['label'] = label

    def add_points(self, points):
        """
        Add points to the shape.
        """
        self.shape['points'] = points

    def add_shape_type(self, shape_type):
        """
        Add shape type to the shape.
        """
        self.shape['shape_type'] = shape_type

    def get_shape(self):
        """
        Get the shape dictionary.
        """
        return self.shape


class Label:
    """
    Class for creating labelme format labels.
    """

    def __init__(self):
        self.label = {}
        self.label['version'] = '4.5.6'
        self.label['flags'] = {}
        self.label['shapes'] = []
        self.label['imagePath'] = ''
        self.label['imageData'] = None
        self.label['imageHeight'] = 0
        self.label['imageWidth'] = 0
        self.label['exposure'] = 500
        self.label['gain'] = 20

    def add_shapes(self, shapes):
        """
        Add shapes to the label.
        """
        self.label['shapes'].append(shapes.get_shape())
        return True

    def add_imagePath(self, imagePath):
        """
        Add image path to the label.
        """
        self.label['imagePath'] = imagePath
        return True

    def add_imageData(self, imageData):
        """
        Add image data to the label.
        """
        self.label['imageData'] = imageData
        return True

    def add_imageHeight(self, imageHeight):
        """
        Add image height to the label.
        """
        self.label['imageHeight'] = imageHeight
        return True

    def add_imageWidth(self, imageWidth):
        """
        Add image width to the label.
        """
        self.label['imageWidth'] = imageWidth
        return True

    def add_exposure(self, exposure):
        """
        Add exposure to the label.
        """
        self.label['exposure'] = exposure
        return True

    def add_gain(self, gain):
        """
        Add gain to the label.
        """
        self.label['gain'] = gain
        return True

    def get_label(self):
        """
        Get the label as a JSON string.
        """
        return json.dumps(self.label)

    def setImage(self, image):
        """
        Set the image properties in the label.
        """
        self.add_imageHeight(image.shape[0])
        self.add_imageWidth(image.shape[1])
        self.add_imageData(self.image_to_base64(image))
        return True

    def image_to_base64(self, image):
        """
        Convert image to base64 encoded string.
        """
        return base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()

    def saveLabel(self, path):
        """
        Save the label to a file.
        """
        try:
            with open(path, 'w') as f:
                f.write(self.get_label())
            return True
        except Exception as e:
            print(f"Error saving label: {e}")
            return False
