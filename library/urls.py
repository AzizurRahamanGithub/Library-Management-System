from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import User_Register_View, Book_View, Author_View, Category_View, Borrow_Book_View, User_Borrow_View, User_Borrow_History_View, User_Return_Book_View, User_Penalty_View 

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register('books', Book_View, basename='books')
router.register('authors', Author_View, basename='authors')
router.register('categories', Category_View, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', User_Register_View.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('borrow/', Borrow_Book_View.as_view(), name='borrow-book'),
    path('borrow/list/', User_Borrow_View.as_view(), name='my-borrows'),
    path('return/', User_Return_Book_View.as_view(), name='return-book'),
    path('users/<int:id>/penalties/', User_Penalty_View .as_view(), name='penalty-points'),
    path("borrow/history/", User_Borrow_History_View.as_view(), name="borrow-history"),
]
