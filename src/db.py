import requests

class DatabaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def execute_query(self, query, function):
        url = f"{self.base_url}/{function}"
        payload = {"query": query}
        response = requests.post(url, json=payload)
        return response.json()

    def insert(self, query):
        return self.execute_query(query, "insert")

    def insert_by_id(self, query):
        return self.execute_query(query, "insertReturnId")
    
    def select(self, query):
        return self.execute_query(query, "select")
    
    def update(self, query):
        return self.execute_query(query, "update")
    
    def delete(self, query):
        return self.execute_query(query, "delete")

class ProcessDB:
    def __init__(self):
        self.db = DatabaseAPI("http://100.121.194.26:5431")

    def fetch_mill_details(self):
        query = "select * from mill_details"
        rows = self.db.select(query)
        # print(rows)
        return rows
    
    def fetch_mill_details_by_millname(self,mill_name):
        query = f"select * from mill_details where mill_name = '{mill_name}'"
        rows = self.db.select(query)
        # print(rows)
        return rows[0]
    
    def fetch_machine_details(self,data):
        query = "select * from machine_details where mill_id = " + data
        rows = self.db.select(query)
        return rows
    

    
    def insert_validation_log(self, data):
        query = f"""
        INSERT INTO validation_log (mill_name, machine_name, tp, fp, fda, score, fps, report_availability) 
        VALUES ('{data['mill']}', '{data['machine']}', {data['tp']}, {data['fp']}, {data['fda']}, {data['score']}, {data['fps']}, {data['report_availability']})
        """
        return self.db.insert(query)
