
import mlrun
import os

class Setup:
    """
    Setup for solution
    """

    def __init__(self, dataset_name, mlrun_env_file: list[str], hard_variables: dict=None):
        """Define setting for testing

        :param dataset_name:    name of data set e.g. "01-size-100"
        :param mlrun_env_file:  list of *.env files, first valid file will be
                                used e.g. ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"]
        :param hard_variables:  new or replacement of variables from *.env file
        """
        # set variables based on environment files
        for env_file in mlrun_env_file:
            if os.path.isfile(env_file):
                self._variables=mlrun.set_env_from_file(env_file, return_dict=True)
                break

        # create new or rewrite variables
        if hard_variables:
            for key in hard_variables.keys():
                self._variables[key]=hard_variables[key]

        self._variables["DIR"]=os.getcwd()

        # set model dirs
        #self._model_definition=self._variables['QGATE_DEFINITION']
        #self._model_output=self._variables['QGATE_OUTPUT']

        # set data set size
        self._dataset_name=dataset_name

    def __str__(self):
        ret=""
        for key in self._variables.keys():
            ret+=key+ ": "+ "'" + self._variables[key] + "'\n"
        return ret[:-1]

    @property
    def variables(self):
        variable_list=[]
        for key in self._variables.keys():
            itm = {}
            itm['key']=key
            itm['value']=self._variables[key]
            variable_list.append(itm)
        return variable_list

    @property
    def model_output(self):
        return self._variables['QGATE_OUTPUT']

    @property
    def model_definition(self):
        return self._variables['QGATE_DEFINITION']

    @property
    def dataset_name(self):
        return self._dataset_name

    @property
    def redis(self):
        return self._variables.get('QGATE_REDIS', None)
