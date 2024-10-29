### Python Chris Client Implementation ###

from base_client import BaseClient
from chrisclient import client

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
        # search for dicom dir
        # run dircopy
        # run dicom_headeredit
        pass

    def __create_feed(self, plugin_id: str,params: dict):
        response = self.cl.create_plugin_instance(plugin_id, params)
        return response

    def __get_plugin_id(self, params: dict):
        response = self.cl.get_plugins(params)
        if response['total'] > 0:
            return response['data'][0]['id']
        raise Exception(f"No plugin found with matching search criteria {params}")

    def __get_dir_path(self, params: dict):
        params["limit"] = 100000
        files = self.cl.get_pacs_files(params)
        l_dir_path = set()
        for file in files['data']:
            file_path = file['fname']
            file_name = file_path.split('/')[-1]
            dir_path = file_path.replace(file_name, '')
            l_dir_path.add(dir_path)
        return ','.join(l_dir_path)

