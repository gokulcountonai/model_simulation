import datetime
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
    
    def fetch_all_machines(self):
        query = "SELECT mill_name, machine_name FROM mill_details JOIN machine_details ON mill_details.mill_id = machine_details.mill_id"
        rows = self.db.select(query)
        print(rows)
        return rows
    

    def insert_validation_log(self, data):
        query = f"""
        INSERT INTO public.validation_log(validation_id, mill_name, machine_name, simulation_type, score, fps, report_availability, folder_path, "timestamp")
        VALUES ('{(data['mill'])}', '{str(data['machine'])}', {str(data['simulation_type'])}, {str(data['score'])}, {str(data['fps'])}, {str(data['report_availability'])}, {str(data['folderpath'])}, {datetime.datetime.now()})
        """
        return self.db.insert(query)


    def fetch_machine_details_by_mill_name(self, mill_name):
        # Fetch mill_id for the given mill_name
            mill_id_query = f"select machine_name from machine_details where mill_id = '{mill_name}'"    
            mill_id_result = self.db.select(mill_id_query)
            # print(mill_id_result)
            # Fetch machine details for the fetched mill_id
            machine_details_query = f"select machine_name from machine_details where mill_id = {mill_name}"
            machine_details_result = self.db.select(machine_details_query)
            machine_names = [row['machine_name'] for row in machine_details_result]
            print(machine_names)
            return machine_names
    

    def add_machine(self, data):
        query = f"""
        INSERT INTO public.machine_details(machine_name, mill_id)
        VALUES ('{data['machine_name']}', '{data['mill_id']}')
        """
        return self.db.insert(query)


    def insert_millname(self,data):
        query=f"""
        Insert into public.mill_details (mill_name)
        VALUES ('{data['name']}')
        """
        return self.db.insert(query)


    

db = ProcessDB()
db.fetch_all_machines()