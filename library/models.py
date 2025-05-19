from django.contrib.auth.models import AbstractUser 
from django.db import models
from datetime import timedelta

class User(AbstractUser):
    penalty_points = models.IntegerField(default=0)

    
class Author(models.Model):
    name= models.CharField(max_length=100)
    bio= models.TextField()

    def __str__(self):
        return self.name
        
    
class Category(models.Model):
    name= models.CharField(max_length=100)
    def __str__(self):
        return self.name

    
class Book(models.Model):
    title= models.CharField(max_length=200)
    description= models.TextField()
    author= models.ForeignKey(Author, on_delete=models.CASCADE)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    total_copies= models.PositiveIntegerField()
    available_copies= models.PositiveIntegerField()

    def __str__(self):
        return self.title
    

class Borrow(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    book= models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date= models.DateField(auto_now_add=True)
    due_date= models.DateField()
    return_date= models.DateField(null=True)

    def save(self,*args, **kwargs):
        if not self.pk and not self.due_date:
            self.due_date= self.borrow_date+timedelta(days= 14)
        super().save(*args,**kwargs)    
    
