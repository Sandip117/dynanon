### Python Chris Client Implementation ###

from base_client import BaseClient
from chrisclient import client
import json

class ChrisClient(BaseClient):
    def __init__(self, url: str, username: str, password: str):
        self.cl = client.Client(url, username, password)

    def create_con(self,params:dict):
        return self.cl

    def pacs_pull(self):
        pass
    def pacs_push(self):
        pass

    def anonymize(self, params: dict):
        prefix = "dynanon"
        feed_name = self.__create_feed_name(prefix,params["search"])
        # search for dicom dir
        dicom_dir = self.__get_dir_path(params["search"])
        anon_params = json.dumps(params["anon"])

        # run dircopy
        pl_id = self.__get_plugin_id({"name":"pl-dsdircopy","version":"1.0.2"})
        pv_in_id = self.__create_feed(pl_id,{"previous_id":26,'dir':dicom_dir,'title':feed_name})
        # run dicom_headeredit
        pl_sub_id = self.__get_plugin_id({"name":"pl-pfdicom_tagsub", "version":"3.3.4"})
        data = {"previous_id": pv_in_id, "tagStruct": anon_params, 'fileFilter': '.dcm'}
        self.__create_feed(pl_sub_id, data)
        pass

    def __create_feed(self, plugin_id: str,params: dict):
        response = self.cl.create_plugin_instance(plugin_id, params)
        return response['id']

    def __create_feed_name(self, prefix: str, params: dict) -> str:
        name = ""
        for val in params.values():
            name += f"-{val}"
        return  f"{prefix}{name}"

    def __get_plugin_id(self, params: dict):
        response = self.cl.get_plugins(params)
        if response['total'] > 0:
            return response['data'][0]['id']
        raise Exception(f"No plugin found with matching search criteria {params}")

    def __get_dir_path(self, params: dict):
        mylist = []
        for key in params.keys():
            mylist.append(params[key])

        files = self.cl.get_pacs_files({"fname_icontains": mylist[0]})
        l_dir_path = set()
        for file in files['data']:
            file_path = file['fname']
            file_name = file_path.split('/')[-1]
            dir_path = file_path.replace(file_name, '')
            l_dir_path.add(dir_path)
        return ','.join(l_dir_path)


