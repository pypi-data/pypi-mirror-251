"""Enderbyte Programs App data Library"""

from platform import system as oss
import os
import json
WINDOWS = oss() == "Windows"

APP_NAME = ""
def register_app_name(name:str):
    global APP_NAME
    APP_NAME = name

class AppDataFile:
    def __init__(self,name="data"):
        """A fully featured app data system"""
        if WINDOWS:
            self.folder = os.path.expandvars(f"%APPDATA%\\{APP_NAME}")
        else:
            self.folder = os.path.expanduser(f"~/.local/share/{APP_NAME}")
        self.path = self.folder + "/" + name + ".json"
        self.default = {}
        self.data = self.default
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
    def setdefault(self,data:dict):
        """Set the default data in this dictionary"""
        self.default = data
        self.data = self.default
    def load(self) -> dict:
        """Return data from file, else return default. Also loads internal data. MUST BE CALLED!"""
        if not os.path.isfile(self.path):
            return self.default
        else:
            try:
                with open(self.path) as f:
                    d = f.read()
                rz = json.loads(d)
                self.data = rz
                return rz
            except:
                return self.default
    def update(self,data: dict):
        """Completely replace internal dictionary with data"""
        self.data = data
    def write(self):
        """Commit app data to the disk"""
        with open(self.path,"w+") as f:
            f.write(json.dumps(self.data))
    def __getitem__(self,item):
        """Overwrite to allow this class to function as a dictionary style object"""
        return self.data[item]
    def keys(self):
        """Bring-forward of dict function"""
        return self.data.keys()
    def values(self):
        """Bring-forward of dict function"""
        return self.data.values()
    def items(self):
        """Bring-forward of dict function"""
        return self.data.items()
    def __setitem__(self,key,value):
        self.data[key] = value