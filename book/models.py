from django.db import models
# from django.contrib.auth.models import User
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    tags = models.ManyToManyField('Tag')
    date_marked = models.DateTimeField(null=True, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ReadBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # user_id = models.IntegerField()
    date_read = models.DateField(auto_now_add=True)



