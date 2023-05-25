import os
from dotenv import dotenv_values

class CommonUtils:
    def __init__(self):
        pass
    def get_environment_variable(self,variable_name):
        """
        param varaible name
        :return: enviromewnt varaible
        """
        if os.environ.get(variable_name) is None:
            enironment_variables =dotenv_values(".env")
            return enironment_variables[variable_name]
        else:
            return os.environ.get(variable_name)
