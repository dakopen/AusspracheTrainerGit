from datetime import datetime
import pathlib
import logging
from utils.IPA import IPA



def generate_time_stamp():
    datetime_obj = datetime.now()
    timestamp = datetime_obj.strftime("%d-%b-%Y_%H_%M_%S-%f")
    return timestamp


class Audioverarbeitung:
    def __init__(self, targetsatz, cleantargetsatz, audiopath):
        self.targetsatz = targetsatz
        self.cleantargetsatz = cleantargetsatz
        self.audiopath = audiopath
    
    def IBM(self):
        print("IBM")
    
    def google(self):
        print("Google")
    
    def AT(self):
        print("AT")

    def delete_audio(self):
        audio_file = pathlib.Path(self.audiopath)
        try:
            audio_file.unlink()
        except FileNotFoundError:
            logging.debug("Fehler die Audiodatei zu löschen")
            print("Error unlinking file!")
    ipa = IPA()