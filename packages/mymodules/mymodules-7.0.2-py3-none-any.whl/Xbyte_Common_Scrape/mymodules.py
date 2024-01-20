import hashlib
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import re
import requests
import shutil
import numpy as np
import pandas as pd
import pymongo
import json
import collections
import pymysql

class YourFrameworkErrorCodes:
    SUCCESS = 0
    ERROR_CODE = 1

class ScrapyAutomation:

    @staticmethod
    def get_useragent(os_type='WINDOWS'):
        """
               Generate Random UserAgents Android/IOS/Windows.

               Args:
               - os_type (str): Android/Windows/IOS types.

               Returns:
               - UserAgent: String like UserAgents.
               """
        if str(os_type).upper() == 'ANDROID' or str(os_type).upper() == 'IOS':
            software_names = [SoftwareName.CHROME.value,SoftwareName.SAFARI.value]
            operating_systems = [OperatingSystem.ANDROID.value,OperatingSystem.IOS.value]
            user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems)
            return user_agent_rotator.get_random_user_agent()
        elif str(os_type).upper() == 'LINUX':
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.LINUX.value]
            user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems)
            return user_agent_rotator.get_random_user_agent()
        else:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
            user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems)
            return user_agent_rotator.get_random_user_agent()

    @staticmethod
    def create_table(conn_string, columns, params_lst):
        """
        Creates a table in the database with the given columns.

        Args:
        - conn_string (obj): The connection string of the database, containing db host, db name, table name.
        - columns (dict): Dictionary containing column names and their data types.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        - con, cursor: Returns con and cursor if successfully executed.
        """

        if not columns or not conn_string:
            print("No columns provided / No conn_string provided")
            return False

        #todo - fetch data from conn string
        conn_data = json.loads(conn_string)
        db_host = conn_data.get('db_host')
        db_user = conn_data.get('db_user')
        db_passwd = conn_data.get('db_passwd')
        db_name = conn_data.get('db_name')
        table_name = conn_data.get('table_name')

        con = pymysql.connect(host=db_host, user=db_user, password=db_passwd)
        db_cursor = con.cursor()

        try:
            create_db = f"create database if not exists {db_name} CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci"
            db_cursor.execute(create_db)

            con = pymysql.connect(host=db_host, user=db_user, password=db_passwd, database=db_name, autocommit=True, use_unicode =True, charset="utf8")
            cursor = con.cursor()

            #todo - Constructing the CREATE TABLE query dynamically
            data = {'id': 1, 'name': 'John Doe', 'skuid': '12345', 'header name': 'some value'}

            for key, value in data.items():
                if ' ' in key:
                    raise ValueError(f"Invalid key: {key}. Spaces not allowed in keys.")

            column_definitions = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
            params_str = ",".join(params_lst)
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id bigint NOT NULL AUTO_INCREMENT, `download_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,`html_path` text,  `screenshot_path` text, `scrap_status` int NOT NULL DEFAULT '0', `retry` int NOT NULL DEFAULT '0',{column_definitions} ,{params_str}) ENGINE=MyISAM DEFAULT CHARSET=utf8"

            cursor.execute(create_table_query)
            con.commit()
            cursor.close()

            print(f"Table '{table_name}' created successfully.")
            return con,cursor
        except Exception as e:
            print(f"Error creating table: {str(e)}")
            con.rollback()
            return False

    @staticmethod
    def fetch_pending_data(conn, database_type, params):
        """
        Fetch data from database

        Args:
        - conn (obj): The connection of the Database.
        - cursor (obj): The cursor of the database.
        - database_type (str): SQL/Mongo database types.
        - params (dict): conditions for fetch database.

        Returns:
        - data (tuple): Data which fetched from database.
        """
        if database_type.lower() == "mysql":
            # Assuming 'params' contains the necessary SQL command and table/collection name

            query = params['query']  # SQL query to fetch data where status is "Pending"
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result

        elif database_type.lower() == "mongodb":
            # Assuming 'params' contains the necessary MongoDB commands and collection name

            collection = conn[params['db']][params['collection']]
            query = params['query']  # MongoDB query to fetch data where status is "Pending"
            # query['status'] = 'Pending'
            result = collection.find(query)
            return list(result)

        else:
            print("Invalid database type specified")
            return None

    @staticmethod
    def save_page(response, file_path):
        """
        Saves the content of a web page to a file.

        Args:
        - response (obj): The response of the request Url.
        - file_path (str): The path where the content will be saved.

        Returns:
        - bool: True if the content is successfully saved, False otherwise.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response)
            return True

    @staticmethod
    def read_page(file_path):
        """
        Reads the content of a file.

        Args:
        - file_path (str): The path of the file to be read.

        Returns:
        - bytes or None: Content of the file if found, None otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return None

    @staticmethod
    def make_request(url, headers, region,request_type="GET", proxy=None, payload=None,retries=1):
        """
            Sends a request to the specified URL.

            Args:
            - url (str): The URL for the GET/POST request.
            - headers (dict, optional): Headers for the request.
            - proxy (dict, optional): Proxy for the request.
            - payload (dict, optional): Payload for the POST request.
            - request_type (dict, optional): request_type like GET/POST request.

            Returns:
            - ResponseStatuscode : The response Statuscode.
            - ResponseText : The response object.
        """
        blocked_responses = ['Limit Reach', 'Max Retries Exceed', 'Too Many Requests', ' Download attempts failed',
                             'Forbidden Error', 'Permission To Access']
        allowed_status_codes = ['200', '404']
        retries_count = 0
        for _ in range(retries):
            retries_count+=1
            if proxy:
                proxy_obj = {'http': proxy, 'https': proxy}
                if 'scraper' in proxy:
                    your_key = ''
                    link = f'http://api.scraperapi.com?api_key={your_key}&url={url}&keep_headers=true&country_code={region.lower()}'
                    response = requests.get(link, headers=headers)
                elif 'crawlera' in proxy:
                    headers['x-requested-with'] = "XMLHttpRequest"
                    headers['X-Crawlera-Cookies'] = "disable"
                    headers['X-Crawlera-Region'] = f"{region.upper()}"
                    if request_type.upper() == "GET":
                        response = requests.get(url, proxies=proxy_obj, headers=headers, verify=False)
                    else:
                        response = requests.post(url, proxies=proxy_obj, headers=headers, data=payload,
                                                 verify=False)
                else:
                    if request_type.upper() == "GET":
                        response = requests.get(url, proxies=proxy_obj, headers=headers, verify=False)
                    else:
                        response = requests.post(url, proxies=proxy_obj, headers=headers, data=payload,
                                                 verify=False)
            else:
                if request_type.upper() == "GET":
                    response = requests.get(url, headers=headers)
                else:
                    response = requests.post(url, headers=headers, data=payload)

            response_text = response.text
            response_status_code = response.status_code

            if all(str(checkpoint).lower() not in str(response_text).lower() for checkpoint in blocked_responses) and str(
                    response_status_code) in allowed_status_codes:
                return response_text, response_status_code, retries_count

        return 'Error in request', 'Error in request'  # Or handle the case when all retries fail

    @staticmethod
    def insert(conn, database_type, params):
        """
        Fetch data from database

        Args:
        - conn (obj): The connection of the Database.
        - cursor (obj): The cursor of the database.
        - database_type (str): SQL/Mongo database types.
        - params (dict): conditions for fetch database.

        Returns:
        - data (tuple): Data inserted in given database.
        """
        if database_type.lower() == "mysql":
            try:
                # Assuming 'params' contains the necessary SQL command and table/collection name
                item = params['item']  # SQL query to fetch data where status is "Pending"

                field_list = []
                value_list = []
                for field in item:
                    field_list.append(str(field))
                    value_list.append(str(item[field]).replace("'", "\\'").replace('"', '\\"'))
                fields = '`,`'.join(field_list)
                values = "','".join(value_list)
                insert_db = "INSERT INTO " + params['collection'] + "( `" + fields + "` ) values ( '" + values + "' )"
                print(insert_db,"|--------------------------------------------------------------------------------------------------|")

                cursor = conn.cursor()
                cursor.execute(insert_db)
                conn.commit()
                return f"{YourFrameworkErrorCodes.SUCCESS} : Data inserted successfully"
            except Exception as e:
                if "duplicate" in str(e).lower():
                    return f"{YourFrameworkErrorCodes.ERROR_CODE} : Duplicate entry, {e}"
                return f"{YourFrameworkErrorCodes.ERROR_CODE} : error in inserting data, {e}"

        elif database_type.lower() == "mongodb":
            # Assuming 'params' contains the necessary MongoDB commands and collection name

            collection = conn[params['db']][params['collection']]
            item = params['item']  # MongoDB query to fetch data where status is "Pending"
            try:
                collection.insert_one(item)
                return f"{YourFrameworkErrorCodes.SUCCESS} : Data inserted successfully"
            except Exception as e:
                if "duplicate" in str(e).lower():
                    return f"{YourFrameworkErrorCodes.ERROR_CODE} : Duplicate entry, {e}"
                return f"{YourFrameworkErrorCodes.ERROR_CODE} : error in inserting data, {e}"
        else:
            return f"{YourFrameworkErrorCodes.ERROR_CODE} : Invalid database type specified"

    @staticmethod
    def update(conn, database_type, params):
        """
        Fetch data from database

        Args:
        - conn (obj): The connection of the Database.
        - cursor (obj): The cursor of the database.
        - database_type (str): SQL/Mongo database types.
        - params (dict): conditions for fetch database.

        Returns:
        - data (tuple): Data updated in given database.
        """
        if database_type.lower() == "mysql":
            # Assuming 'params' contains the necessary SQL command and table/collection name
            try:
                item = params['item']  # SQL query to update data where status is "Pending"
                make_update_query = f'update {params["collection"]} set '
                for key, value in item.items():
                    make_update_query += "`" + key + "`" + "=" + "'" + str(value).replace('"', '\\"').replace("'","\\'") + "'" + ","
                update_query = f'''{make_update_query} where {params['condition']}="{params["condition_value"]}"'''.replace(f', where {params["condition"]}=', f' where {params["condition"]}=')
                cursor = conn.cursor()
                cursor.execute(update_query)
                conn.commit()
                print("....................Data updated.....................")
                return f"{YourFrameworkErrorCodes.SUCCESS} : Data Updated successfully"
            except Exception as e:
                return f"{YourFrameworkErrorCodes.ERROR_CODE} : error in updating data, {e}"

        elif database_type.lower() == "mongodb":
            # Assuming 'params' contains the necessary MongoDB commands and collection name

            collection = conn[params['db']][params['collection']]
            item = params['item']  # MongoDB query to update data where status is "Pending"
            try:
                collection.update_one(params['condition'],{"$set":item})
                return f"{YourFrameworkErrorCodes.SUCCESS} : Data Updated successfully"
            except Exception as e:
                return f"{YourFrameworkErrorCodes.ERROR_CODE} : error in updating data, {e}"
        else:
            return f"{YourFrameworkErrorCodes.ERROR_CODE} : Invalid database type specified"

    @staticmethod
    def c_replace(html=''):
        """
            This method for some more than replace method need to apply in
            one string so in this method customize all replace like \n \r \t or extra space
            all are replce and return proper string.
        """

        if isinstance(html, str):

            html = html.replace("&gt;", ">")
            html = html.replace("&lt;", "<")
            html = html.replace("&amp;", "&")
            html = html.replace("\r\n", " ")
            html = html.replace("", "")
            # html = html.replace(vbLf, " ").replace(vbCrLf, " ").replace(vbCr, " ")
            html = html.replace("\t", " ")
            html = html.replace("\n", " ")
            html = html.replace("\r", " ")
            html = html.replace("&nbsp;", " ")
            html = re.sub("<script[^>]*>([\w\W]*?)</script>", " ", html)
            html = re.sub("\* style specs start[^>]*>([\w\W]*?)style specs end *", " ", html)
            html = re.sub("<style[^>]*>([\w\W]*?)</style>", " ", html)
            html = re.sub("<!--([\w\W]*?)-->", " ", html)
            html = re.sub("<([\w\W]*?)>", " ", html)
            html = re.sub("<.*?>", " ", html)
            html = re.sub(" +", " ", html)

            return html.strip()

        elif isinstance(html, list):
            return [j for j in [ScrapyAutomation.c_replace(i) for i in html] if j]
        else:
            raise TypeError(f'must be str or list - object pass is ({type(html)}) object....')

    @staticmethod
    def unknownrepl(data_string):
        """
                    Remove unknown characters from the string.

                    Args:
                    - take the string which contains unknown characters.

                    Returns:
                    - clean data string.
                """
        data_string = ScrapyAutomation.c_replace(data_string)
        data_string = data_string.encode('unicode_escape').decode('ascii')
        regex_string = r'\\u[\w]{4}'
        clean_text = ScrapyAutomation.c_replace(re.sub(regex_string, '', data_string))
        clean_text = ScrapyAutomation.c_replace(clean_text)
        return clean_text

    @staticmethod
    def img_download(url, file_name):
        """
                    Download image from url.

                    Args:
                    - take the url which you want to download.
                    - take the file name which you want to save.

                    Returns:
                    - clean data string.
                """

        # check file path
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
                res = requests.get(url, stream=True, headers=headers)

                if res.status_code == 200:
                    with open(file_name, 'wb') as f:
                        shutil.copyfileobj(res.raw, f)
                    print('Image sucessfully Downloaded: ', file_name)
                    return True
                else:
                    print('Image Couldn\'t be retrieved')
                    return None
            except Exception as e:
                print("Error :: Image Couldn\'t be retrieved :", e)
                return None
        else:
            print(
                "--------->|| Please Provide File path with image Extension. Check The Extension of a File. ||<--------- ")
            return None

    @staticmethod
    def generate_hash(product_url,post_code=None):
        """
                            Generate hash_id from url.

                            Args:
                            - take the data string you want to convert into hash_id.

                            Returns:
                            - hash_id.
        """

        try:

            # Update the hash with the encoded product URL and post code
            hash_utf8 = (str(product_url).encode('utf8')) + (str(post_code).encode('utf8'))

            # Obtain the hexadecimal digest and convert it to an integer
            hash_as_int = int(hashlib.md5(hash_utf8).hexdigest(), 16)

            # Convert the integer to a string and take the first 12 characters
            hash_id = str(hash_as_int)[:12]

            return hash_id

        except Exception as e:
            print(f"Error generating hash: {e}")
            return None

    @staticmethod
    def export(params):
        # todo : export file using mongodb
        if params.get('database') == 'mongodb':
            mongo_string = params.get('mongo_string')
            mongo_db = params.get('mongo_db')
            mongo_tbl = params.get('mongo_tbl')
            filepath = params.get('filepath')
            headers_all = params.get('headers_all')
            file_type_lst = params.get('file_type_lst')
            try:
                query = params.get('query')
            except:
                query = {}

            # TODO - Connect to MongoDB
            client = pymongo.MongoClient(mongo_string)
            db = client[mongo_db]
            collection = db[mongo_tbl]

            # TODO - MongoDB query
            data = list(collection.find(query))

            # TODO - DataFrame creation
            data_frame = pd.DataFrame(data)

            # TODO - According Headers
            data_frame = data_frame[headers_all]

            # TODO - Dataframe-decode
            data_frame = data_frame.applymap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

        # todo : export file using mysql
        elif params.get('database') == 'mysql':
            mysql_host = params.get('mysql_host')
            mysql_user = params.get('mysql_user')
            mysql_password = params.get('mysql_password')
            mysql_db = params.get('mysql_db')
            mysql_tbl = params.get('mysql_tbl')
            file_type_lst = params.get('file_type_lst')
            filepath = params.get('filepath')
            headers_all = params.get('headers_all')
            try:
                query = params.get('query')
            except:
                query = ""

            conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db,
                                   use_unicode=True, charset="utf8")

            select_sql_query = f"""select {",".join(headers_all)} from {mysql_tbl} {query}"""
            data_frame = pd.read_sql(select_sql_query, conn)
            # TODO - Dataframe-decode
            data_frame = data_frame.applymap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
        else:
            return "Please give valid database type in params it should be only mongodb or mysql"
        try:
            if "xlsx" in file_type_lst:
                # TODO - Initializing Options for xlsxwriter engine
                options = {}
                options['strings_to_formulas'] = False
                options['strings_to_urls'] = False
                # TODO - XLSX
                try:
                    with pd.ExcelWriter(f'{filepath}.xlsx', engine='xlsxwriter',engine_kwargs={'options': options}) as writer:
                        data_frame.to_excel(writer, index=False)
                except:
                    with pd.ExcelWriter(f'{filepath}.xlsx', engine='xlsxwriter', options=options) as writer:
                        data_frame.to_excel(writer, index=False)
            if "csv" in file_type_lst:
                # TODO - CSV
                data_frame.to_csv(f'{filepath}.csv', index=False, encoding='utf8')

            if "tsv" in file_type_lst:
                # TODO - TSV
                data_frame.to_csv(f'{filepath}.tsv', index=False, sep='\t', encoding='utf-8-sig')

            if "jsonl" in file_type_lst or "json" in file_type_lst:
                # TODO - JSON
                objects_list = []
                json_counter = 0
                data_frame = data_frame.fillna(np.nan).replace([np.nan], [None])
                for index, row in data_frame.iterrows():
                    try:
                        d = collections.OrderedDict()
                        json_counter += 1

                        for column, value in row.items():
                            try:
                                if str(value).startswith('[') or str(value).startswith('{'):
                                    d[column] = json.loads(json.dumps(value))
                                else:
                                    d[column] = value
                            except Exception as e:
                                return f"Issue in - Row : {json_counter} || Header Name : {column} Values: {value} || {e}"

                        objects_list.append(d)

                    except Exception as e:
                        return f"Error in generating file : {e}"
                if "jsonl" in file_type_lst:
                    with open(f'{filepath}.jsonl', "w", encoding='utf-8') as f:
                        f.write(json.dumps(objects_list, ensure_ascii=False))
                        f.close()
                else:
                    with open(f'{filepath}.json', "w", encoding='utf-8') as f:
                        f.write(json.dumps(objects_list, ensure_ascii=False))
                        f.close()

        except Exception as e:
            return f"Error in generating file : {e}"