from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    

    path('download_app/', views.download_app, name="Download App"),

    path('login/', views.login, name="login"),
    path('logout/', views.logout_app, name="logout"),
    
    # Pages
    path('', views.index, name="home"),
    path("users/", views.users, name="All Users"),
    path("transactions/", views.transactions, name="All Transactions"),
    path("squaredtransactions/", views.squaredofftransactions, name="All Squared-Off Transactions"),
    path("clients/", views.clients, name="Clients"),
    path("settings/", views.settings, name="All Settings"),
    path("help/", views.help, name="Help"),
    path("user/<str:clientID>", views.user_details, name="Use Details"),
    path("add_transaction/", views.add_transaction_page, name="Add Transaction"),

    # APIs
    path('script/add', views.add_script, name='Add Script'),
    path('script/get', views.get_script, name='Get Script'),
    path('scripts/refresh', views.save_script_list_file, name='Refresh Scripts')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)