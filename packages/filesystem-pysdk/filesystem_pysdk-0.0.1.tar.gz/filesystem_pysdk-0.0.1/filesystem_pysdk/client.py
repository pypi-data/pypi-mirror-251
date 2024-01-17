import os.path

import requests
from enum import Enum
from .user import User
from .bucket import Bucket
from .file import File


class PATH(object):
    URL_REFRESH: str = "/refresh"
    URL_VERSION: str = "/version"
    URL_BUCKET: str = "/bucket"
    URL_USER: str = "/user"

    URL_FILE_UPLOAD = "/file/upload"
    URL_FILE_DOWNLOAD = "/file/download"
    URL_FILE_MOVE = "/file/move"
    URL_FILE_COPY = "/file/copy"
    URL_FILE_DELETE = "/file/delete"


class Config(object):
    def __init__(self, user: str, auth: str, apiHost: str, webHost: str):
        self._user = user
        self._auth = auth
        self._api_host = apiHost
        self._webHost = webHost

    def get_auth_header(self) -> dict:
        """generate request auth header."""
        return {
            "user": self._user,
            "auth": self._auth
        }


class Client(Config):
    def __init__(self, user: str, auth: str, api_host: str, web_host: str):
        super().__init__(user, auth, api_host, web_host)
        self._session = requests.Session()

    def check_connection(self) -> bool:
        """ check api host connection.
        :return: True if connection is ok, else False
        """
        try:
            res = self._session.get(f"{self._api_host}{PATH.URL_VERSION}")
            if res.status_code == 200:
                return True
            return False
        except Exception:
            return False

    def check_auth(self) -> bool:
        return True

    def add_user(self, user: User) -> str | None:
        """ add user
        :param user: must User type, otherwise raise TypeError
        :return: If success is None, or error message.
        """
        if not isinstance(user, User):
            raise TypeError(f"Invalid user type. need type is User, but got {type(user)}")
        res = self._session.post(f"{self._api_host}{PATH.URL_USER}",
                                 headers=self.get_auth_header(),
                                 json=user.to_dict())
        if res.status_code != 201:
            return f"request error ({res.status_code}): {res.text}"

    def delete_user(self, name: str) -> str | None:
        """ delete user
        :param name: the user name
        :return: If success is None, or error message"""
        res = self._session.delete(f"{self._api_host}{PATH.URL_USER}",
                                   headers=self.get_auth_header(),
                                   json={"name": name})
        if res.status_code != 204:
            return f"request error ({res.status_code}): {res}"

    def add_bucket(self, bucket: Bucket) -> str | None:
        """ add bucket"""
        if not isinstance(bucket, Bucket):
            raise TypeError(f"Invalid bucket type. need type is Bucket, but got {type(bucket)}")

        res = self._session.post(f"{self._api_host}{PATH.URL_BUCKET}",
                                 headers=self.get_auth_header(),
                                 json=bucket.to_dict())
        if res.status_code != 201:
            return f"request error ({res.status_code}): {res.text}"

    def delete_bucket(self, name: str) -> str | None:
        """ delete bucket
        :param name: the bucket name
        :return: If success is None, or error message"""
        res = self._session.delete(f'{self._api_host}{PATH.URL_BUCKET}',
                                   headers=self.get_auth_header(),
                                   json={"name": name})
        if res.status_code != 204:
            return f"request error ({res.status_code}): {res.text}"
        pass

    def upload_file(self, file: File, data) -> str | None:
        if not isinstance(file, File):
            raise TypeError(f"file must be of type File, but got {type(file)}")
        if data is None:
            raise TypeError(f"data must be not None")

        res = self._session.post(f"{self._api_host}{PATH.URL_FILE_UPLOAD}",
                                 files=[("file", (os.path.basename(file.key), data, "application/octet-stream"))],
                                 data=file.to_dict(),
                                 headers=self.get_auth_header())

        if res.status_code != 201:
            return f"request error ({res.status_code}): {res.text}"
        pass

    def delete_file(self, file: File) -> str | None:
        if not isinstance(file, File):
            raise TypeError(f"file must be of type File, but got type {type(file)}")

        res = self._session.delete(f"{self._api_host}{PATH.URL_FILE_DELETE}",
                                   json=file.to_dict(),
                                   headers=self.get_auth_header())
        if res.status_code != 204:
            return f"request error ({res.status_code}): {res.text}"

    def move_file(self, sour: File, dest: File) -> str | None:
        if not isinstance(sour, File):
            raise TypeError(f"file must be of type File, but got type {type(sour)}")
        if not isinstance(dest, File):
            raise TypeError(f"file must be of type File, but got type {type(dest)}")

        res = self._session.post(f"{self._api_host}{PATH.URL_FILE_MOVE}",
                                 json={"s_bucket": sour.bucket, "s_key": sour.key, "d_bucket": dest.bucket,
                                       "d_key": dest.key},
                                 headers=self.get_auth_header())
        if res.status_code != 200:
            return f"request error ({res.status_code}): {res.text}"

    def copy_file(self, sour: File, dest: File) -> str | None:
        if not isinstance(sour, File):
            raise TypeError(f"source must be of type File, but got type {type(sour)}")
        if not isinstance(dest, File):
            raise TypeError(f"destination must be of type File, but got {type(dest)}")
        res = self._session.post(f"{self._api_host}{PATH.URL_FILE_COPY}",
                                 json={"s_bucket": sour.bucket, "s_key": sour.key, "d_bucket": dest.bucket,
                                       "d_key": dest.key},
                                 headers=self.get_auth_header())
        if res.status_code != 200:
            return f"request error ({res.status_code}): {res.text}"

    def download_file(self, file: File) -> bytes | str | None:
        if not isinstance(file, File):
            raise f"file must be of type File, but got type {type(file)}"
        res = self._session.get(f"{self._api_host}{PATH.URL_FILE_DOWNLOAD}?bucket={file.bucket}&key={file.key}",
                                headers=self.get_auth_header())
        if res.status_code != 200:
            return f"request error ({res.status_code}): {res}"
        return res.content


def new_client(user: str, auth: str, api_host: str, web_host: str) -> (Client | None, str | None):
    client = Client(user, auth, api_host, web_host)
    if not client.check_connection():
        return None, "api connect error"
    if not client.check_auth():
        return None, "api auth error"
    return client, None
