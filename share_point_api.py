from office365.sharepoint.client_context import ClientContext
import os
import tempfile

class Sharepoint():
    targeted_folder_path = "Shared Documents/Resumes/unprocessed"
    def __init__(self, username: str, password: str, url: str):
        if not all([username, password, url]):
            raise ValueError('All input parameters must be provided')
        self.username: str = username
        self.url: str = url
        try:
            self.ctx = ClientContext(self.url).with_user_credentials(self.username, password)
        except Exception as e:
            raise ValueError('Failed to create client context: {e}')
        self.download_dir: str = tempfile.mkdtemp()


    def get_files(self) -> list[str]:
        try:
            root_folder = self.ctx.web.get_folder_by_server_relative_path(self.targeted_folder_path)
        except Exception as e:
            raise ValueError(f'Falied to get folder: {e}')
        try:
            files = root_folder.get_files(True).execute_query()

        except Exception as e:
            raise ValueError(f'Failed to get files: {e}')
        return [[file.properties.get('Name', None) for file in files], [file.properties.get('ServerRelativeUrl', None) for file in files]]

    
    def download_file(self, file_name: str) -> str:
        file_name: str = os.path.join(self.targeted_folder_path, file_name)
        download_path: str = os.path.join(self.download_dir, os.path.basename(file_name))
        try:
            with open(download_path, 'wb') as local_file:
                file = self.ctx.web.get_file_by_server_relative_url(file_name).download(local_file).execute_query()
        except Exception as e:
            raise ValueError(f'Failed to download {file_name}: {e}')
        return download_path
    
    def download_files(self, file_names: list[str]):
        return [self.download_file(file_name) for file_name in file_names]