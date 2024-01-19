import ctypes
import os
import json
from typing import Dict

class Sixvan:

    def __init__(self) -> None:

        #获取当前目录
        default_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,'libs') 
        libdir = os.environ.get("SIXVAN_LIBDIR", default_directory)
        self._so = ctypes.cdll.LoadLibrary(f"{libdir}/libsixvan.so") 

    def get_all(self, url:str, uuid:str):
        assert isinstance(url, str)
        assert isinstance(uuid, str)
        self._so.get_all.restype = ctypes.c_char_p
        res = self._so.get_all(url.encode(), uuid.encode())
        return json.loads(res.decode())

    def get_one(self, url:str, uuid:str, id:str):
        assert isinstance(url, str)
        assert isinstance(uuid, str)
        assert isinstance(id, str)
        self._so.get_one.restype = ctypes.c_char_p
        res = self._so.get_one(url.encode(), uuid.encode(), id.encode())
        return json.loads(res.decode())
    
    def set_one(self, url:str, uuid:str, id:str, payload:Dict):
        assert isinstance(url, str)
        assert isinstance(uuid, str)
        assert isinstance(id, str)
        assert isinstance(payload, dict)
        data = {
            'uuid': uuid,
            'id': id,
            'payload': payload
        }
        return self._so.set_one(url.encode(), json.dumps(data).encode())

sixvan = Sixvan()