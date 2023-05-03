from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"{self.name}"


class Diary(models.Model):
    note = models.CharField(max_length=50, blank=False)
    date_time_issued = models.DateTimeField(blank=False)
    day = models.CharField(max_length=50, blank=False)
    # Category can have many Diary Entries, but a particular Diary Entry can have only one Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.note}"
