import queue,threading,redis,pickle,time

class Inference:
    def __init__(self) -> None:
        try:
            self.client  = redis.Redis(host='localhost', port=6379, db=0,
                                        health_check_interval=10,
                                            socket_connect_timeout=5,
                                            retry_on_timeout=True,
                                            socket_keepalive=True)
            

            self.p = self.client.pubsub()
            self.p.subscribe('channel2')
            self.imageQueue = queue.Queue(maxsize=10)
            self.thread = threading.Thread(target=self.valuePooling)
            self.thread.start()
        except Exception as e:
            print(str(e))
    def inferImage(self,image,imageId=0):
        try:
            data = {}
            data["image"] = image
            data["imageId"] = imageId
            serialized = pickle.dumps(data)
            try:
                self.client.publish('channel1', serialized)
            except Exception as e:
                print(e)
                return {"status": 500}
            # data = r.json()
            data["status"] = 200
            return data
        except Exception as e:
            print(str(e))
            return {"status": 500}
    
    def valuePooling(self):
        try:
            while True:
                try:
                    data = self.p.get_message()
                    # print("data: ", data)
                    if data == None or data['data'] == 1:
                        time.sleep(0.001)
                        continue
                    if self.imageQueue.full() == False:
                        self.imageQueue.put(pickle.loads(data['data']))
                except Exception as e:
                    print(str(e))

                time.sleep(0.001)
        except Exception as e:
            print(str(e))

    def getInferResult(self):
        try:
            if self.imageQueue.empty() == False:
                return True,self.imageQueue.get()
            else:
                return False,""
        except Exception as e:
            print(str(e))
            return False,""


