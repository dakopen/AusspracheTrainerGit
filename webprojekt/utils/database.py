from base.models import Satzscore
from django.contrib.auth.models import User


class Database:
    def __init__(self, session_id):
        self.session_id = session_id
    
    def save_ergebnis(self,  score, target_satz, target_ipa, google_transcript, google_ipa, ibm_transcript, ibm_ipa, at_ipa):
        s = Satzscore(score=score, target_satz=target_satz, target_ipa=target_ipa, google_transcript=google_transcript, google_ipa=google_ipa, ibm_transcript=ibm_transcript, ibm_ipa=ibm_ipa, at_ipa=at_ipa, session_id=self.session_id)
        s.save()



