from django.db import models

class Satzscore(models.Model):
    score = models.DecimalField(max_digits=10, decimal_places=7)
    
    target_satz = models.CharField(max_length=120)
    target_ipa = models.TextField()

    google_transcript = models.TextField()
    google_ipa = models.TextField()

    ibm_transcript = models.TextField()
    ibm_ipa = models.TextField()

    at_ipa = models.TextField()

    # Logging Informationen
    session_id = models.CharField(max_length=10)
    zeit = models.DateField(auto_now_add=True)
    

