import cv2
import time
import queue
import threading
from src.label import Label, Shape

class StoreImage:
    """
    Class to store and process images.
    """

    def __init__(self):
        """
        Initialize the StoreImage class.
        """
        self.imageQueue = queue.Queue(maxsize=50)
        self.thread = threading.Thread(target=self.store_image)
        self.thread.start()
        self.label = Label()
        self.shape = Shape()

    def store_image(self):
        """
        Process and store images from the image queue.
        """
        while True:
            try:
                if self.imageQueue.qsize() > 0:
                    image, location, label = self.imageQueue.get()
                    if label:
                        for cb in image:
                            cb[0](cb[1])
                    else:
                        cv2.imwrite(location, image)
                else:
                    time.sleep(0.01)
            except Exception as e:
                print(e)
                time.sleep(0.01)
                continue

    def set_image(self, image, location):
        """
        Add an image to the image queue.
        """
        self.imageQueue.put([image, location, False])
        return True

    def set_defect_image(self, image, location):
        """
        Add a defect image to the image queue.
        """
        self.imageQueue.put([image, location, False])
        return True

    def set_label(self, image, result, coordinates, location, exposure, gain):
        """
        Add a label to the image and save it.
        """
        self.label = Label()
        self.shape = Shape()
        cb = []
        cb.append([self.shape.add_label, result])
        x1, y1, x2, y2 = coordinates
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cb.append([self.shape.add_points, [[x1, y1], [x2, y2]]])
        cb.append([self.shape.add_shape_type, 'rectangle'])
        cb.append([self.label.add_shapes, self.shape])
        cb.append([self.label.add_exposure, exposure])
        cb.append([self.label.add_gain, gain])
        cb.append([self.label.add_imagePath, location.split("/")[-1]])
        cb.append([self.label.set_image, image])
        location = location[:-3] + "json"
        cb.append([self.label.saveLabel, location])
        if not self.imageQueue.full():
            self.imageQueue.put([cb, "", True])
        del self.label
        del self.shape
        return True