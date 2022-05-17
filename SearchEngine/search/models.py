import datetime
from django.db import models


# Create your models here.
class Case(models.Model):
    # 全文
    context = models.TextField()
    # 案号
    case_number = models.CharField(max_length=100)

    def __str__(self):
        return self.case_number
