# этот файл описывает таблицы базы данных на языке Python. 
# Каждый класс — это одна таблица, каждый атрибут класса 
# — один столбец. Django сам превращает это в реальные таблицы 
# (через миграции), и сам переводит твои Python-команды в SQL


from django.db import models
from django.contrib.auth.models import User


# Database table for files 

class Scan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64) # SHA-256 hash (64 char)
    created_at = models.DateTimeField(auto_now_add=True)
    verdict = models.CharField(max_length=100, null=True, blank=True)

    # defines how the object is shown as text( UrlScan object (1) > the actual link)
    def __str__(self):
        return self.file_name
    
    # Returns a CSS class name based on the verdict (coloring)
    def badge_class(self):
        if self.verdict == "Clean":
            return "badge-clean"
        if self.verdict and self.verdict.startswith("Dangerous"):
            return "badge-danger"
        return "badge-unknown"

# Database table for urls

class UrlScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(max_length=500)
    verdict = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    screenshot = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.url

    # Returns a CSS class name based on the verdict (coloring)
    def badge_class(self):
        if self.verdict == "Clean":
            return "badge-clean"
        if self.verdict and self.verdict.startswith("Dangerous"):
            return "badge-danger"
        return "badge-unknown"