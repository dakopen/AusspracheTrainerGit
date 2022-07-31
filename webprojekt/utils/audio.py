from datetime import datetime
import pathlib
import time
from utils.IPA import IPA
import speech_recognition as sr
from utils.IBM_API import send_to_IBM

from utils.AusspracheTrainerKIStartup import AusspracheTrainerKI
aussprachetrainer = AusspracheTrainerKI()

r = sr.Recognizer()


def generate_time_stamp():
    datetime_obj = datetime.now()
    timestamp = datetime_obj.strftime("%d-%b-%Y_%H_%M_%S-%f")
    return timestamp


class Audioverarbeitung:
    def __init__(self, targetsatz, cleantargetsatz, audiopath):
        self.targetsatz = targetsatz
        self.cleantargetsatz = cleantargetsatz
        self.audiopath = audiopath
        self.ipa = IPA()

    
    def IBM(self):
        try:
                
            IBM_KI = send_to_IBM(self.audiopath)
            if IBM_KI != "#*# ERROR RECEIVED IBM":
                IBM_IPAKI, _ = self.ipa.text_zu_IPA(self.ipa.text_preparation(" ".join(IBM_KI).lower()))
            else:
                IBM_IPAKI = IBM_KI

            return IBM_IPAKI, " ".join(IBM_KI)
        except:
            return "#*# ERROR RECEIVED IBM", ""


    def google(self):
        try:
            audiofile = sr.AudioFile(self.audiopath)
            with audiofile as source:
                audio = r.record(source)
                google_pred = r.recognize_google(audio, language="de-DE")
                Google_KI_for_IPA = str(google_pred).strip().lower()
                Google_IPAKI, _ = self.ipa.text_zu_IPA(self.ipa.text_preparation(Google_KI_for_IPA))
                
            return Google_IPAKI, str(google_pred).strip()
        except:
            return "#*# ERROR RECEIVED GOOGLE", ""
    
    def AT(self):
        global aussprachetrainer
        if time.time() - aussprachetrainer.creationdate > 84000:  # wird jeden Tag neu gestartet
            del aussprachetrainer
            aussprachetrainer = AusspracheTrainerKI()
        try:
            AusspracheTrainerIPAKI = aussprachetrainer.aussprachetrainer_predict(self.audiopath)
            AusspracheTrainerIPAKI = [item for sublist in AusspracheTrainerIPAKI for item in sublist]
            return " ".join(AusspracheTrainerIPAKI)
        except:
            return "#*# ERROR RECEIVED AUSSPRACHETRAINERKI"

    def delete_audio(self):
        audio_file = pathlib.Path(self.audiopath)
        try:
            audio_file.unlink()
        except FileNotFoundError:
            #logger.info("Fehler die Audiodatei zu löschen")
            print("Error unlinking file!")
