import sys
import os
import time
import ast
import cv2,threading
from src.infer import Inference
from src.storeimages import StoreImage
from src.db import ProcessDB

db = ProcessDB()

class ImageProcessor:
    def __init__(self):
        try:
            self.storeimages = StoreImage()
            self.inference = Inference()
            self.score = 0.1
            self.batch_id = ""
            self.path = ""
            thread = threading.Thread(target=self.get_infer_result)
            thread.start()
        except Exception as e:
            print(str(e))

    def read_images(self, path, fps, camtype="1"):
        try:
            filesList = os.listdir(path)
            for file in filesList:
                image = cv2.imread(path + file)
                self.inference.inferImage(image, str(camtype)+"_" + str(file))
                time.sleep(1 / int(fps))
                print("Infering image:", file)
            print("ALL IMAGES READ")
            return True
        except Exception as e:
            print("Error in reading images:", e)
            return False

    def get_infer_result(self):
        while True:
            try:
                ret, data = self.inference.getInferResult()
                if ret != False:
                    # print(data)
                    data['batch_id'] = self.batch_id
                    if data["classType"] == "None":
                        print(data)         
                        continue

                    classType = [n.strip() for n in ast.literal_eval(data["classType"])]
                    conf = [n for n in ast.literal_eval(data["conf"])]
                    xyxy = [n for n in ast.literal_eval(data["xyxy"])]
                    imageId = data["imageId"]
                    print(data)  

                    print(self.path + "/" + imageId[2:])
                    img = cv2.imread(self.path + imageId[2:])
                    unbox = img.copy()

                    for i, cls in enumerate(classType):
                        print("Class:", cls)
                        print("Confidence:", conf[i])
                        print("Bounding Box:", xyxy[i])
                        print("Image Id:", imageId)

                        if conf[i] > self.score:
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

                            jsonlocation = "output/" + cls + "/"
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
            except Exception as e:
                print(str(e))

            time.sleep(0.005)