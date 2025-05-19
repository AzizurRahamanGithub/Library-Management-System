
from .models import Book, Author, Category,Borrow,User

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()

class Register_Seri(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token']

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def create(self, validated_data):
        user= User.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password= validated_data['password']
        )

        return user


# Book, Author, Category Serializers makeing herer

class Author_Seri(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class Category_Seri(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class Book_Seri(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'total_copies', 'available_copies',
            'author', 'category'
        ]


# Borrow Serializer making herer

class Borrow_Seri(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )
    book = Book_Seri(read_only=True)

    class Meta:
        model = Borrow
        fields = ['id', 'book', 'book_id', 'borrow_date', 'due_date', 'return_date']
        read_only_fields = ['borrow_date', 'due_date', 'return_date']

    def validate(self, data):
        user= self.context['request'].user

        # Borrow limit
        active_borrows=  Borrow.objects.filter(user=user, return_date__isnull= True).count()
        
        if active_borrows>=3:
            raise serializers.ValidationError("Your Already Borrow 3 Books. Which is Max Limit Of Borrowing.")

        book= data["book"]
        if book.available_copies<1:
            raise serializers.ValidationError("No Copies Available. Sorry!")

        return data

    def create(self, validated_data):
        user= self.context['request'].user
        book= validated_data['book']

        if book.available_copies<1:
            raise serializers.ValidationError("NO Copies Available")
        book.available_copies=  book.available_copies-1
        book.save()

        borrow= Borrow()
        borrow.user= user;
        borrow.book= book;
        borrow.due_date= date.today()+timedelta(days=14)
        borrow.save()

        return borrow

class Return_Seri(serializers.Serializer):
    borrow_id = serializers.IntegerField()