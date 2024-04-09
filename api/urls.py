from django.urls import path
from . import views

BASE_URL = "v1/"

urlpatterns = [
    path(f'{BASE_URL}login', views.login, name="Login"),

    # Token Log
    path(f'{BASE_URL}token/add', views.token_add, name="Add Token"),

    # Users
    path(f'{BASE_URL}profile', views.profile, name="Profile"),
    path(f'{BASE_URL}user/edit', views.edit_user, name="Edit user"),
    path(f'{BASE_URL}user/details', views.get_user, name="Edit user"),
    path(f'{BASE_URL}user/update_password', views.update_password, name="Update Password"),

    # Settings
    path(f'{BASE_URL}settings', views.settings, name="Get Settings"),
    path(f'{BASE_URL}settings/update', views.update_settings, name="Update Settings"),

    # Transactions
    path(f'{BASE_URL}transactions', views.get_transactions, name="Get Transaction"),
    path(f'{BASE_URL}transaction/add', views.add_transaction, name="Add Transaction"),
    path(f'{BASE_URL}transaction/update', views.update_transaction, name="Update Transaction"),
    path(f'{BASE_URL}fetch_active_transactions/', views.fetch_cliens_portfolio, name="Fetch New Transactions"),

    # Sqaured-Off Transactions
    path(f'{BASE_URL}SquaredOffTransactions', views.get_squaredoff_transactions, name="Get Squared-Off Transaction"),
    path(f'{BASE_URL}SquaredOffTransaction/add', views.add_squredoff_transaction, name="Complete Transaction"),
    path(f'{BASE_URL}SquaredOffTransaction/all', views.resolveAll, name="Resolve All Transaction"),
    #path(f'{BASE_URL}transaction/update', views.update_transaction, name="Update Transaction"),

    # Scripts
    path(f'{BASE_URL}scripts', views.scripts, name="Get all active scripts"),
    path(f'{BASE_URL}update_script', views.update_script, name="update script"),
    path(f'{BASE_URL}remove_script', views.remove_scripts, name="remove scripts")

    
    
]