from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from .serializers import Book_Seri,Author_Seri, Category_Seri, Return_Seri, Borrow_Seri,Register_Seri
from .permissions import Amin_Other

from datetime import date
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import User
from .models import User
from .models import Borrow
from .models import Book, Author, Category

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework import generics
from rest_framework import generics


User = get_user_model()

class User_Register_View(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Register_Seri



class Book_View(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = Book_Seri
    permission_classes = [Amin_Other]
    filter_backends = [filters.SearchFilter]
    search_fields = ['author__name', 'category__name']

class Author_View(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = Author_Seri
    permission_classes = [Amin_Other]

class Category_View(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = Category_Seri
    permission_classes = [Amin_Other]



# Borrow Views

class Borrow_Book_View(generics.CreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = Borrow_Seri
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class User_Borrow_View(generics.ListAPIView):
    serializer_class = Borrow_Seri
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user, return_date__isnull=True)



# borrow histor of an Athinticated User

class User_Borrow_History_View(generics.ListAPIView):
    serializer_class = Borrow_Seri
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user).order_by('-borrow_date')
        

# Return a book by an user

class User_Return_Book_View(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Return_Seri 

    def post(self, request):
        borrow_id = request.data.get('borrow_id')
        try:
            borrow = Borrow.objects.get(id=borrow_id, user=request.user)
        except Borrow.DoesNotExist:
            return Response({'error': 'Invalid borrow ID'})

        borrow.return_date= date.today()
        if borrow.return_date:
            return Response({'error': 'Book already returned'})
        

        # Start making penalty points after 14 days       
        if date.today() > borrow.due_date:
            days_late = (date.today() - borrow.due_date).days
            request.user.penalty_points += days_late
            request.user.save()

        # update inventory     
        with transaction.atomic():
            borrow.book.available_copies += 1
            borrow.book.save()
            borrow.save()

        return Response({'message': 'Book returned successfully'})


# Penalty View

class User_Penalty_View(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request):
        user = self.get_object()
        if request.user != user and not request.user.is_staff:
            return Response({'error': 'Not authorized'})
        return Response({'username': user.username, 'penalty_points': user.penalty_points})
