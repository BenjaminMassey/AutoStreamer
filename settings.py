from xml.etree import ElementTree as ET

class Settings():
    
    data = None
    
    def __init__(self):
        self.data = ET.parse("settings.xml")
        
    def get(self, key):
        for setting in self.data.findall('setting'):
            if setting.attrib['name'] == key:
                return setting.attrib["value"]
        return ""