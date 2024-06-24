import json
import base64
import numpy as np
import cv2



class Shape:
    """
    creating labelme format shapes
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
        self.shape['label'] = label
    
    def add_points(self, points):
        self.shape['points'] = points
    

    
    def add_shape_type(self, shape_type):
        self.shape['shape_type'] = shape_type
    

    
    def get_shape(self):
        return self.shape




class Label:
    """
    creating labelme format labels
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
        self.label['shapes'].append(shapes.get_shape())
        return True
    
    def add_imagePath(self, imagePath):
        self.label['imagePath'] = imagePath
        return True
    
    def add_imageData(self, imageData):
        self.label['imageData'] = imageData
        return True
    
    def add_imageHeight(self, imageHeight):
        self.label['imageHeight'] = imageHeight
        return True
    
    def add_imageWidth(self, imageWidth):
        self.label['imageWidth'] = imageWidth
        return True
    
    def add_exposure(self, exposure):
        self.label['exposure'] = exposure
        return True
    
    def add_gain(self, gain):
        self.label['gain'] = gain
        return True

    def get_label(self):
        # print(self.label)
        return json.dumps(self.label)
    
    def setImage(self,image):
        self.add_imageHeight(image.shape[0])
        self.add_imageWidth(image.shape[1])
        self.add_imageData(self.image_to_base64(image))
        return True

    def image_to_base64(self,image):
        return base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
    
    def saveLabel(self, path):
        with open(path, 'w') as f:
            f.write(self.get_label())
        return True
    

# if __name__ == "__main__":
#     label = Label()
#     shape = Shape()
#     shape.add_label('test')
#     shape.add_points([[1,2],[3,4]])
#     shape.add_shape_type('rectangle')
#     label.add_shapes(shape)
#     label.add_imagePath('test.jpg')
#     label.setImage(cv2.imread('test.jpg'))
#     label.saveLabel('test.json')



    
