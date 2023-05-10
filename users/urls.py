from django.urls import path
from .views import SignUpView, EditView, DoctoresPageView, UserListView, ErrorView, UserDeleteView, SearchUserListView, SignUpBasicView, EditBasicView

urlpatterns = [
    path('', DoctoresPageView.as_view(), name='users'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup_basic/', SignUpBasicView.as_view(), name='signup_basic'),
    path('<int:pk>/edit/', EditView.as_view(), name='edit'),
    path('<int:pk>/editbasic/', EditBasicView.as_view(), name='edit_basic'),
    path('list/', UserListView.as_view(), name='user_list'),#lista de todos los usuarios   
    path('error/', ErrorView.as_view(), name='error'),#lista de todos los usuarios 
    path('<int:pk>/delete/',UserDeleteView.as_view(), name='delete'),#borrar articulos 
    path('search/', SearchUserListView.as_view(),name='search_users'), #Lista de pacientes del buscador 
]