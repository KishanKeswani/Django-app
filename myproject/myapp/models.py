from django.db import models
import pandas as pd

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y')
