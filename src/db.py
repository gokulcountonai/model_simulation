import datetime
import requests

class DatabaseAPI:
    def __init__(self, base_url):
        """
        Initializes the DatabaseAPI class with the base URL.
        """
        self.base_url = base_url

    def execute_query(self, query, function):
        """
        Executes a query by sending a POST request to the API endpoint.

        Args:
            query (str): The SQL query to execute.
            function (str): The function name for the API endpoint.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If there is an error in the request.
        """
        try:
            url = f"{self.base_url}/{function}"
            payload = {"query": query}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error executing query: {e}")
            return None

    def insert(self, query):
        """
        Executes an insert query.

        Args:
            query (str): The SQL insert query.

        Returns:
            dict: The JSON response from the API.
        """
        return self.execute_query(query, "insert")

    def insert_by_id(self, query):
        """
        Executes an insert query and returns the inserted ID.

        Args:
            query (str): The SQL insert query.

        Returns:
            dict: The JSON response from the API.
        """
        return self.execute_query(query, "insertReturnId")
    
    def select(self, query):
        """
        Executes a select query.

        Args:
            query (str): The SQL select query.

        Returns:
            dict: The JSON response from the API.
        """
        return self.execute_query(query, "select")
    
    def update(self, query):
        """
        Executes an update query.

        Args:
            query (str): The SQL update query.

        Returns:
            dict: The JSON response from the API.
        """
        return self.execute_query(query, "update")
    
    def delete(self, query):
        """
        Executes a delete query.

        Args:
            query (str): The SQL delete query.

        Returns:
            dict: The JSON response from the API.
        """
        return self.execute_query(query, "delete")

class ProcessDB:
    def __init__(self):
        """
        Initializes the ProcessDB class and creates an instance of DatabaseAPI.
        """
        self.db = DatabaseAPI("http://100.121.194.26:5431")

    def fetch_mill_details(self):
        """
        Fetches all mill details.

        Returns:
            dict: The JSON response from the API.
        """
        query = "select * from mill_details"
        rows = self.db.select(query)
        return rows
    
    def fetch_mill_details_by_millname(self, mill_name):
        """
        Fetches mill details by mill name.

        Args:
            mill_name (str): The mill name.

        Returns:
            dict: The JSON response from the API.
        """
        query = f"select * from mill_details where mill_name = '{mill_name}'"
        rows = self.db.select(query)
        return rows[0]
    
    def fetch_machine_details(self, data):
        """
        Fetches machine details by mill ID.

        Args:
            data (str): The mill ID.

        Returns:
            dict: The JSON response from the API.
        """
        query = "select * from machine_details where mill_id = " + data
        rows = self.db.select(query)
        return rows
    
    def fetch_all_machines(self):
        """
        Fetches all machines with their corresponding mill names.

        Returns:
            dict: The JSON response from the API.
        """
        query = "SELECT mill_name, machine_name FROM mill_details JOIN machine_details ON mill_details.mill_id = machine_details.mill_id"
        rows = self.db.select(query)
        return rows
    

    def insert_validation_log(self, data):
        """
        Inserts a validation log.

        Args:
            data (dict): The validation log data.

        Returns:
            dict: The JSON response from the API.
        """
        query = f"""
        INSERT INTO public.validation_log(validation_id, mill_name, machine_name, simulation_type, score, fps, report_availability, folder_path, "timestamp")
        VALUES ('{(data['mill'])}', '{str(data['machine'])}', {str(data['simulation_type'])}, {str(data['score'])}, {str(data['fps'])}, {str(data['report_availability'])}, {str(data['folderpath'])}, {datetime.datetime.now()})
        """
        return self.db.insert(query)


    def fetch_machine_details_by_mill_name(self, mill_name):
        """
        Fetches machine details by mill name.

        Args:
            mill_name (str): The mill name.

        Returns:
            list: The list of machine names.
        """
        try:
            # Fetch mill_id for the given mill_name
            mill_id_query = f"select machine_name from machine_details where mill_id = '{mill_name}'"    
            mill_id_result = self.db.select(mill_id_query)
            
            # Fetch machine details for the fetched mill_id
            machine_details_query = f"select machine_name from machine_details where mill_id = {mill_name}"
            machine_details_result = self.db.select(machine_details_query)
            
            machine_names = [row['machine_name'] for row in machine_details_result]
            return machine_names
        except Exception as e:
            print(f"Error fetching machine details: {e}")
            return []
    

    def add_machine(self, data):
        """
        Adds a new machine.

        Args:
            data (dict): The machine data.

        Returns:
            dict: The JSON response from the API.
        """
        query = f"""
        INSERT INTO public.machine_details(machine_name, mill_id)
        VALUES ('{data['machine_name']}', '{data['mill_id']}')
        """
        return self.db.insert(query)


    def insert_millname(self, data):
        """
        Inserts a mill name.

        Args:
            data (dict): The mill name data.

        Returns:
            dict: The JSON response from the API.
        """
        query = f"""
        Insert into public.mill_details (mill_name)
        VALUES ('{data['name']}')
        """
        return self.db.insert(query)
