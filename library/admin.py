from django.contrib import admin
from .models import User, Author, Category, Book, Borrow

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Borrow)
