from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [  # path('', HomeView.as_view(), name='index'),
    path('', index, name='index'),
    path('category/<int:category_id>/', category_page, name='category'),
    path('about_dev', about_dev, name='about_dev'),
    path('search/', search_results, name='search'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('logout/', auth_views.LogoutView.as_view, name='logout'),
    path('register/', register, name='register'),
    path('post/<int:post_id>/', post_detail, name='post'),
    path('post_update/<int:id>/', update_post, name='update'),
    path('post_delete/<int:id>/', delete_post, name='delete_post'),
    path('add_comment/<int:pk>/', save_comment, name='save_comment'),
    path('add_or_delete_mark/<int:post_id>/<str:action>/', add_or_delete_mark, name='mark'),
    path('my_page/', user_profile, name='my_page'),
    path('contact/', contact_us, name='contact'),
    path('map_page.html/', map_page, name='map'),
    # path('edit_profile/', edit_profile, name='edit_profile'),
]
