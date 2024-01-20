# -*- coding: utf-8 -*-
import time
import allure
import json
import unittest
import requests
from Andreani_QA_parameters.Parameters import Parameters
from Andreani_QA_Functions.Functions import Functions


class Api(Functions, Parameters):
    windows = {}
    driver = None
    value_to_find = None
    get_locator_type = None
    number_windows = None
    exception = None
    json_strings = None
    complete_json_path = None
    message_container = None
    message_error = None
    json_on_loaded = None
    global_date = time.strftime(
        Parameters.date_format)  # formato dd/mm/aaaa    global_time = time.strftime(Parameters.time_format)  # formato 24 houras
    lista_pasos = []
    lista_descripcion_pasos = []
    driver_port_status = False
    record = None

    def create_file_validations(self, data_validations, name_template):
        return Functions.create_file_validations(data_validations, name_template)

    def send_service(self, data):

        """
            Description:
                Envía un servicio.
            Args:
                data: recibe los siguientes parámetros en formato json:
                    tipoPeticion (str): Tipo de petición del servicio.
                    endPoint (str): Endpoint del servicio.
                    headers (str): Headers del servicio.
                    payload (str): Payload del servicio.
                    time (int): Tiempo de espera de la respuesta del servicio.
                    statusCodeEsperado (int): Codigo de estatus esperado en la respuesta.
                    responseEsperado: (dict_to_json):
            Returns:
                Retorna un request si la petición es exitosa y un array con las
                diferencias obtenidas. De lo contrario imprime el error por consola.
        """

        response = ""
        validation_structure = "None"
        differences = []
        validate_cant_records = "None"
        cant_registros_db = ""
        cant_registros_api = ""
        statuscode = None
        validation_status_code = None

        total_retry = Parameters.number_retries

        # Se realiza el llamado a la api, si falla reintenta nuevamente.
        for retry in range(total_retry):
            if data['headers'] is not None:
                try:
                    response = requests.request(data['tipoPeticion'], data['endPoint'], headers=data['headers'],
                                                data=data['payload'], timeout=data['time'])
                    print(f"El servicio '{data['endPoint']}' respondio con status code {response.status_code}")
                    break
                except requests.exceptions.Timeout:
                    print("Hubo un error por timeout al enviar el servicio")
            else:
                try:
                    response = requests.request(data['tipoPeticion'], data['endPoint'], timeout=data['time'])
                    print(f"El servicio '{data['endPoint']}' respondio con status code {response.status_code}")
                    break
                except requests.exceptions.Timeout:
                    print("Hubo un error por timeout al enviar el servicio")

        # Se valida es status code del request.
        try:
            unittest.TestCase().assertNotEqual(str(type(response)), "<class 'str'>",
                                               "Error Status Code: No se obtuvo response valido. Response de tipo String (TimeOut)")
            validation_status_code = self.validate_status_code(data['statusCodeEsperado'], response.status_code)
            statuscode = response.status_code
        except AttributeError as e:
            Api.exception_logger(e)
            print(f"Error al obtener el status code del servicio.")

        # Se valida la estructura/integridad del response.
        if 'validateStructure' in data.keys():
            if data['validateStructure']:
                validation_structure, differences = self.validate_structure(data['responseEsperado'], response)
            else:
                validation_structure = "None"

        # Se compara la cantidad de registros entre la DB y la API.
        if 'validateCantData' in data.keys():
            if data['validateCantData']:
                validate_cant_records, cant_registros_db, cant_registros_api = \
                    self.validate_cant_records(data, response)
            else:
                validate_cant_records = "None"
                cant_registros_db = "None"
                cant_registros_api = "None"

        # Se adjuntan las validaciones en formato HTML o formato JSON.
        if 'attach_validations' in data.keys():
            if data['attach_validations']:

                # Se imprime en el template los datos utilizados para las validaciones.
                if 'test_data' in data.keys():
                    data_validations = {
                        'precondition_data': data['test_data'],
                        'validations': [
                            {
                                'validation': 'Status code esperado',
                                'result': validation_status_code,
                                'status_code_esperado': data['statusCodeEsperado'],
                                'status_code_obtenido': response.status_code
                            },
                            {
                                'validation': 'Cantidad de registros',
                                'result': validate_cant_records,
                                'cantidad_datos_origen': cant_registros_db,
                                'cantidad_datos_destino': cant_registros_api
                            },
                            {
                                'validation': 'Estructura del response',
                                'result': validation_structure,
                                'differences': differences
                            }
                        ]
                    }
                else:
                    data_validations = {
                        'validations': [
                            {
                                'validation': 'Status code esperado',
                                'result': validation_status_code,
                                'status_code_esperado': data['statusCodeEsperado'],
                                'status_code_obtenido': response.status_code
                            },
                            {
                                'validation': 'Cantidad de registros',
                                'result': validate_cant_records,
                                'cantidad_datos_origen': cant_registros_db,
                                'cantidad_datos_destino': cant_registros_api
                            },
                            {
                                'validation': 'Estructura del response',
                                'result': validation_structure,
                                'differences': differences
                            }
                        ]
                    }

                # Formato de template que se adjunta en Allure.
                if 'template' in data.keys():
                    file = Api.create_file_validations(data_validations, data['template'])
                else:
                    file = Api.create_file_validations(data_validations, 'cards')

                # Se adjunta el archivo HTML en un step de Allure existente o nuevo.
                if 'step_allure' in data.keys():
                    if data['step_allure']:
                        with allure.step(u"PASO: Se realizan las siguientes validaciones"):
                            allure.attach.file(file, name="Validaciones", attachment_type=None, extension=".html")
                    else:
                        allure.attach.file(file, name="Validaciones", attachment_type=None, extension=".html")
                else:
                    allure.attach.file(file, name="Validaciones", attachment_type=None, extension=".html")

                # Se realizan los asserts de las validaciones.
                for i in range(len(data_validations['validations'])):
                    validataion = data_validations['validations'][i]['validation']
                    result = data_validations['validations'][i]['result']
                    if validataion == "Status code esperado" and not result:
                        unittest.TestCase().assertEqual(data['statusCodeEsperado'], response.status_code,
                                                        f"El status code no es el esperado, el value obtenido es "
                                                        f"{response.status_code}")

                    elif validataion == "Cantidad de registros" and not result:
                        unittest.TestCase().assertEqual(cant_registros_db, cant_registros_api,
                                                        "No coinciden la cantidad de datos entre origen y destino.")

                    elif validataion == "Estructura del response" and not result:
                        unittest.TestCase().assertEqual(len(differences), 0,
                                                        "Se encontraron differences en la estructura del response.")

                data_validations.clear()
            else:
                dict = {
                    'status_code_esperado': data['statusCodeEsperado'],
                    'status_code_obtenido': statuscode
                }
                self.attach_json(dict)
        else:
            dict = {
                'status_code_esperado': data['statusCodeEsperado'],
                'status_code_obtenido': statuscode
            }
            self.attach_json(dict)

        return response, differences

    @staticmethod
    def validate_status_code(status_code_esperado, status_code_obtenido):

        """
            Description:
                Se valida el status code de un servicio.
            Args:
                status_code_esperado (int): Código de estado esperado en la respuesta.
                status_code_obtenido (int): Código de estado obtenido en la respuesta.
            Returns:
                Retorna un booleano con el resultado de la validación.
        """

        if status_code_esperado == status_code_obtenido:
            validation = True
        else:
            validation = False
        return validation

    def validate_cant_records(self, data, response):

        """
            Description:
                Se valida la cantidad de registros de un servicio.
            Args:
                data: Diccionario con tados de DB.
                response: Response obtenido en la respuesta.
            Returns:
                Retorna un booleano con el resultado de la validación.
                Retorna la cantidad de datos obtenidos del origen y destino.
        """

        cant_registros_api = 0
        response = json.loads(response.text)

        # Se obtiene cantidad de datos existentes en la DB.
        cant_registros_db = Api.check_base_sqlserver(data['data_db']['server_name'],
                                                     data['data_db']['consulta'])
        if len(cant_registros_db) > 0:
            cant_registros_db = cant_registros_db[0]

        # Se obtiene cantidad de datos existentes de la API.
        # Se debe pasar una 'key' del response obtenido para que cuente la cantidad de registros devueltos por la API.
        if str(type(response)) != "<class 'dict'>":
            for i in range(len(response)):
                if data['searchKey'] in response[i]:
                    cant_registros_api = cant_registros_api + 1
        else:
            if data['searchKey'] in response:
                cant_registros_api = cant_registros_api + 1

        if cant_registros_db == cant_registros_api:
            validation = True
        else:
            validation = False

        print(f"Cantidad de datos obtenidos desde la DB: {cant_registros_db}")
        print(f"Cantidad de datos obtenidos desde la API: {cant_registros_api}")

        return validation, cant_registros_db, cant_registros_api

    @staticmethod
    def validate_structure(expected_response, response_obtained):

        """
            Description:
                Se valida la estructura de un servicio.
            Args:
                expected_response: Diccionario con la estructura del response esperado.
                response_obtained: Diccionario con la estructura del response obtenido.
            Returns:
                Retorna un booleano con el resultado de la validación.
                Retorna un array con las diferencias encontradas.
        """

        diferencias = Api.compare_structure(expected_response, response_obtained)

        if len(diferencias) == 0:
            validation = True
        else:
            validation = False

        print(f"Response esperado: {expected_response}")
        print(f"Response obtenido: {response_obtained.text}")

        return validation, diferencias

    @staticmethod
    def compare_structure(expected_response, response_obtained):

        """
            Description:
                Compara estructuras de una respuesta esperada con una respuesta obtenida de un servicio.
            Args:
                expected_response: Respuesta esperada en formato json.
                response_obtained: Respuesta obtenida en formato json.
            Returns:
                Retorna un array con las diferencias encontradas.
        """

        differences = []
        try:

            unittest.TestCase().assertNotEqual(str(type(response_obtained)), "<class 'str'>",
                                               "Error: El response obtenido es de tipo String")
            response_obtained = json.loads(response_obtained.text)
        except ValueError:
            unittest.TestCase().assertEqual(True, False, "Error al convertir el json value_text en diccionario.")

        if len(expected_response) > 0 and str(type(expected_response)) != "<class 'dict'>":
            expected_response = expected_response[0]

        if len(response_obtained) > 0 and str(type(response_obtained)) != "<class 'dict'>":
            response_obtained = response_obtained[0]

        # Busca y compara las key del json1 en json2.
        for key in expected_response:
            if key not in response_obtained.keys():
                error = {
                    'description': 'Keys que se encuentran en origen pero no en destino',
                    'missing_key': key
                }
                differences.append(error)

        # Busca y compara las key del json2 en json1.
        for key in response_obtained:
            if key not in expected_response.keys():
                error = {
                    'description': 'Keys que se encuentran en destino pero no en origen',
                    'missing_key': key
                }
                differences.append(error)

        return differences

    @staticmethod
    def attach_json(dict_to_json):

        """
             Description:
                Adjunta la validación del status code en un paso de Allure en formato json.
             Args:
                dict_to_json (dict): Diccionario con información de la validación realizada.
        """

        with allure.step(u"PASO: Se valida el status code esperado"):
            allure.attach(json.dumps(dict_to_json, indent=4), "Validación de status code",
                          attachment_type=allure.attachment_type.JSON)
            unittest.TestCase().assertEqual(dict_to_json['status_code_esperado'], dict_to_json['status_code_obtenido'],
                                            f"El status code no es el esperado, el value obtenido es "
                                            f"{dict_to_json['status_code_obtenido']}")

    def set_timeout_base_sql_server(self, time_seconds):

        """
            Description:
                Configura el value de timeout (segundos) configurado para las conexiones a bases sqlServer.
            Args:
                time_seconds: Valor (int) que representa una cantidad en segundos.
        """

        Functions.set_timeout_base_sql_server(self, time_seconds)

    def get_timeout_base_sql_server(self):

        """
            Description:
                Devuelve el value de timeout configurado para la conexion a bases sqlServer.
            Return:
                Devuelve el value de timeout (segundos) configurado para la conexion a bases sqlServer.
        """

        return Functions.get_timeout_base_sql_server(self)

    def establish_connection_sqlserver(self, db_name):

        """
            Description:
                Realiza conexión a una base de datos sqlServer.
            Args:
                server: Servidor ip
                base: nombre de la base
                user: usuario
                password: Contraseña
            Return:
                Devuelve una variable con la conexion a la base de datos sqlServer.
        """

        return Functions.establish_connection_sqlserver(self, db_name)

    def check_base_sqlserver(self, db_name, query):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                db_name: Nombre de la data base.
                query: Consulta Query.
            Returns:
                <class 'pyodbc.Row'>: Retorna un class 'pyodbc.Row' si la consulta y la conexión es exitosa. De lo
                contrario imprime por consola "Se produjo un error en la base de datos."
        """

        return Functions.check_base_sqlserver(self, db_name, query)

    def execute_sp_base_sqlserver(self, db_name, query, parameters: tuple):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                server (str): Servidor ip.
                base (str): Nombre de la base.
                user (str): Usuario.
                password (str): Contraseña.
                query (str): Consulta Query.
                parameters (tuple): Tupla con parametros para el sp.
            Returns:
                Lista con los resultados.
        """

        return Functions.execute_sp_base_sqlserver(self, db_name, query, parameters)

    def get_list_base_sqlserver(self, db_name, query):
        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                server (str): Servidor ip.
                base (str): Nombre de la base.
                user (str): Usuario.
                password (str): Contraseña.
                query (str): Consulta Query.
            Returns:
                Lista con los resultados.
        """

        return Functions.get_list_base_sqlserver(self, db_name, query)

    def delete_reg_base_sqlserver(self, db_name, query):

        """
            Description:
                Elimina un registro de la base de datos. El método incluye la desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        Functions.delete_reg_base_sqlserver(self, db_name, query)

    def insert_reg_base_sqlserver(self, db_name, query):

        """
            Description:
                Inserta un registro de la base de datos. El método incluye la desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        Functions.insert_row_base_sqlserver(self, db_name, query)

    def update_reg_base_sqlserver(self, db_name, query):

        """
            Description:
                Actualiza un registro de la base de datos. El método incluye la desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        Functions.update_row_base_sqlserver(self, db_name, query)

    def establish_connection_oracle(self, db_name):

        """
            Description:
                Realiza conexión a una base de datos sqlServer.
            Args:
                server: Servidor ip
                base: nombre de la base
                user: usuario
                password: Contraseña
            Return:
                Devuelve una variable con la conexion a la base de datos sqlServer.
        """

        return Functions.establish_connection_oracle_db(self, db_name)

    def check_base_oracle(self, db_name, query):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria xOracle. El metodo incluye la
                desconexión.
            Args:
                db_name: Nombre de la data base.
                query: Consulta Query.
            Returns:
                <class 'pyodbc.Row'>: Retorna un class 'pyodbc.Row' si la consulta y la conexión es exitosa. De lo
                contrario imprime por consola "Se produjo un error en la base de datos."
        """
        return Functions.check_base_oracle_db(self, db_name, query)
