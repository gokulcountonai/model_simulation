import sys
import os
import time
import ast
import cv2,threading
from src.infer import Inference
from src.storeimages import StoreImage

class ImageProcessor:
    def __init__(self):
        self.storeimages = StoreImage()
        self.inference = Inference()
        thread = threading.Thread(target=self.get_infer_result)
        thread.start()

    def read_images(self, path, camtype, fps):
        filesList = os.listdir(path)
        for file in filesList:
            image = cv2.imread(path + file)
            self.inference.inferImage(image, str(camtype) + str(file))
            time.sleep(1 / int(fps))
            print("Infering image:", file)

    def get_infer_result(self, path, camtype, fps):
        while True:
            ret, data = self.inference.getInferResult()
            print(data)
            if ret != False:
                if data["classType"] == "None":
                    continue

                classType = [n.strip() for n in ast.literal_eval(data["classType"])]
                conf = [n for n in ast.literal_eval(data["conf"])]
                xyxy = [n for n in ast.literal_eval(data["xyxy"])]
                imageId = data["imageId"]

                print(path + "/" + imageId[2:])
                img = cv2.imread(path + imageId[2:])
                unbox = img.copy()

                for i, cls in enumerate(classType):
                    print("Class:", cls)
                    print("Confidence:", conf[i])
                    print("Bounding Box:", xyxy[i])
                    print("Image Id:", imageId)

                    if conf[i] > 0.1:
                        os.makedirs("output", exist_ok=True)
                        os.makedirs("output/box/", exist_ok=True)
                        os.makedirs("output/unbox/", exist_ok=True)

                        os.makedirs("output/box/" + cls, exist_ok=True)
                        os.makedirs("output/unbox/" + cls, exist_ok=True)

                        x1, y1, x2, y2 = xyxy[i]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        cv2.putText(img, str(conf[i]), (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                        jsonlocation = "/home/kniti/projects/knit-i/knitting-core/src/output/json/" + cls + "/"
                        os.makedirs(jsonlocation, exist_ok=True)
                        print(imageId)
                        self.storeimages.setLabel(
                            img.copy(),
                            str(conf[i]),
                            xyxy[i],
                            jsonlocation + imageId,
                            500,
                            10,
                        )

                        cv2.imwrite("output/box/" + cls + "/" + imageId + "_" + str(conf[i]) + ".png", img)
                        cv2.imwrite("output/unbox/" + cls + "/" + imageId + str(conf[i]) + ".png", unbox)

            time.sleep(0.005)

# # Usage example:
# path = sys.argv[1]
# camtype = sys.argv[2]
# fps = sys.argv[3]

# image_processor = ImageProcessor()
# image_processor.read_images(path, camtype, fps)
# image_processor.get_infer_result(path, camtype, fps)
