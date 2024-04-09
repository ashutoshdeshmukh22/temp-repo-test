import requests
import random
import pandas as pd
import json
import os
import datetime

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth import logout, authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Count
from django.db import connection

from django.forms.models import model_to_dict
from .models import ClientProfile, app_configs, Scripts, Transactions, SquredOffTransactions
from .serializers import ScriptsSerializers, TransactionsSerializers
from .forms import TransactionForm

from django.utils import timezone



def download_app(request):
    file_path = os.path.join('static', "Melody.apk")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/app")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser or user.is_staff:
                django_login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/login?error=True")    
        else:
            return HttpResponseRedirect("/login?error=True")

def logout_app(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required(login_url='/login')
def index(request):

    context = {}
    user = request.user
    user = ClientProfile.objects.filter(user_id=user.id).first()
    context['client'] = user

    total_user_count = User.objects.filter(is_active=True).count()
    context['total_user_count'] = total_user_count

    total_active_transactions_count = Transactions.objects.filter(status=True).count()
    context['total_active_transactions_count'] = total_active_transactions_count

    current_date = timezone.now().date()
    context['total_squaredoff_transactions'] = 0
    query = f"""
        SELECT COUNT(*) 
        FROM playground_squredofftransactions 
        WHERE DATE(created_at) = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [current_date])
        records_inserted_today = cursor.fetchone()[0]
        context['total_squaredoff_transactions'] = records_inserted_today


    configs = app_configs.objects.values()
    response = render(request, 'pages/index.html',context)

    for config in configs:
        response.set_cookie(config['name'], config['value'])

    return response 

@login_required(login_url='/login')
def users(request):

    """
    This function is responsible for managing users endpoint.
    using this function admin/sub-admin will be able to list all their customer and create new user accounts.
    For newly created account, Admin/Sub-Admin just have to provide the newly generated ClientID to customer for login purpose,
    where he/she can create password and login in to their account.
    """

    if request.method == 'GET':
        
        context = {}
        user = request.user
        
        parent_ = ClientProfile.objects.filter(user_id=request.user.id).first()
        #return HttpResponse(parent_.parent_id);
    
        user = ClientProfile.objects.filter(user_id=user.id).first()
        context['client'] = user

        defaultLimit = app_configs.objects.filter(name="initial_limit").first()
        context['defaultLimit'] = defaultLimit.value
        
        if(request.user.is_superuser):
            users = ClientProfile.objects.all().annotate(
                active_transaction_count=Count('transactions', filter=Q(transactions__status=1)),
            )            
        else:
            users = ClientProfile.objects.filter(parent_id=parent_.client_id).annotate(
                active_transaction_count=Count('transactions', filter=Q(transactions__status=1))
            )
        
        context['users'] = users
        return render(request, 'pages/users.html', context)
    
    else:
        name, email, phone, limit, role = (
            request.POST.get(key) for key in ["client_name", "client_email", "client_phone", "client_limit", "client_role"]
        )
        
        if name:

            parent_id = ClientProfile.objects.filter(user_id=request.user.id)[0].client_id
            
            def generate_random_code():
                return random.randint(100, 999)
            
            def create_profile() -> None:
                while True:
                    code = generate_random_code()
                    if not User.objects.filter(username=code).exists():
                        return f"{parent_id}{code}", code

            merged_client_id, only_client_id  = create_profile()

            user = User.objects.create_user(
                first_name = name,
                email=email,
                is_staff=True if role != 'normal_client' else False,
                username=merged_client_id,
                password='123123'
            )

            clientprofile = ClientProfile(user=user)
            if request.user.is_staff:

                clientprofile.client_id = only_client_id
                clientprofile.limit = int(limit)
                clientprofile.phone = phone
                clientprofile.parent_id = parent_id
                clientprofile.save()
            
                response = HttpResponseRedirect("/users?success=True")
                response.set_cookie('ClientID', user.username)
                response.set_cookie('ClientPassword', '123123')
                return response
        else:
            return HttpResponseRedirect("/users?error=True")
        

@login_required(login_url='/login')
def transactions(request):
    context = {}
    user = request.user
    
    user = ClientProfile.objects.filter(user_id=user.id).first()
    GetMyClient = ClientProfile.objects.filter(parent_id=user.client_id).values_list('client_id')
    
    context['client'] = user

    if user.user.is_superuser :
        transactions = Transactions.objects.filter(status=1).order_by('client')
    else:
        transactions = Transactions.objects.filter(client_id__in=list(GetMyClient)).order_by('client')
        
    context['transactions'] = transactions

    scripts = Scripts.objects.filter(status=True)
    scripts_serializer  = ScriptsSerializers(scripts, many=True)
    context['scripts'] = scripts_serializer.data

    apptoken = app_configs.objects.filter(name="api_token").first()
    context['api_token'] = apptoken.value
    return render(request, 'pages/transactions.html', context)


@login_required(login_url='/login')
def squaredofftransactions(request):
    context = {}
    user = request.user
    
    user = ClientProfile.objects.filter(user_id=user.id).first()
    GetMyClient = ClientProfile.objects.filter(parent_id=user.client_id).values_list('client_id', flat=True)
    client_ids = list(GetMyClient)
    
    if len(client_ids) == 1:
        client_ids_string = str(client_ids[0])
    else:
        client_ids_string = ','.join(map(str, client_ids))

    transactions = []

    context['client'] = user

    cursor = connection.cursor()

    
    if user.user.is_superuser :
        #cursor.execute('''SELECT t.client_id as client, CONCAT(cp.parent_id, t.client_id) as client_id, t.transaction_id, t.name, t.expirydate, t.quantity, t.offerPrice, t.bidPrice, t.profit_loss, t.created_at FROM playground_squredofftransactions as t JOIN playground_clientprofile as cp ON cp.client_id = t.client_id;''')
        cursor.execute('''
            SELECT
                t.client_id as "systemclient",
                concat(u.parent_id,t.client_id) as "client",
                s.script_code,
                s.name as "name", 
                s.quantity as "lot", 
                s.multiplier as "multipler",
                s.profit_loss as "profit_loss",
                (200 * s.quantity) as "brokrage",
                t.offerPrice AS "buy_price",
                s.bidPrice AS "sell_price",
                t.created_at AS "buy_time",
                s.created_at AS "sell_time"
            FROM
                playground_squredofftransactions s
            LEFT JOIN
                playground_transactions t ON t.transaction_id = s.parent_transaction
            LEFT JOIN 
                playground_clientprofile u ON t.client_id = u.client_id
            WHERE
                t.action = 'Buy'
                AND s.action = 'Sell'
                AND s.created_at >= NOW() - INTERVAL 7 DAY
            UNION ALL
            SELECT
                t.client_id as "systemclient",
                concat(u.parent_id,t.client_id) as "client",
                s.script_code,
                s.name as "name", 
                s.quantity as "lot", 
                s.multiplier as "multipler",
                s.profit_loss as "profit_loss",
                (200 * s.quantity) as "brokrage",
                t.offerPrice AS "buy_price",
                s.bidPrice AS "sell_price",
                t.created_at AS "buy_time",
                s.created_at AS "sell_time"
            FROM
            playground_squredofftransactions s
            LEFT JOIN
                playground_transactions t ON t.transaction_id = s.parent_transaction
            LEFT JOIN 
                playground_clientprofile u ON t.client_id = u.client_id
            WHERE
                t.action = 'Sell' 
                AND s.action = 'Buy'
                AND s.created_at >= NOW() - INTERVAL 7 DAY;     
        ''')
        columns = [col[0] for col in cursor.description]
        transactions =  [dict(zip(columns, row)) for row in cursor.fetchall()]
    else:
    
        # return HttpResponse("OK")
        if(len(list(GetMyClient)) > 0):
            # cursor.execute(f'''SELECT CONCAT(cp.parent_id, t.client_id) as client_id, t.transaction_id, t.name, t.expirydate, t.quantity, t.offerPrice, t.bidPrice, t.profit_loss, t.created_at 
            #     FROM playground_squredofftransactions as t 
            #     JOIN playground_clientprofile as cp ON cp.client_id = t.client_id 
            #     WHERE t.client_id IN ({client_ids_string});'''
            # )
            cursor.execute(f'''
                SELECT
                    t.client_id as "systemclient",
                    concat(u.parent_id,t.client_id) as "client",
                    s.script_code,
                    s.name as "name", 
                    s.quantity as "lot", 
                    s.multiplier as "multipler",
                    s.profit_loss as "profit_loss",
                    (200 * s.quantity) as "brokrage",
                    t.offerPrice AS "buy_price",
                    s.bidPrice AS "sell_price",
                    t.created_at AS "buy_time",
                    s.created_at AS "sell_time"
                FROM
                    playground_squredofftransactions s
                LEFT JOIN
                    playground_transactions t ON t.transaction_id = s.parent_transaction
                LEFT JOIN 
                    playground_clientprofile u ON t.client_id = u.client_id
                WHERE
                    t.client_id IN ({client_ids_string})
                    AND t.action = 'Buy'
                    AND s.action = 'Sell'
                    AND s.created_at >= NOW() - INTERVAL 7 DAY
                UNION ALL
                SELECT
                    t.client_id as "systemclient",
                    concat(u.parent_id,t.client_id) as "client",
                    s.script_code,
                    s.name as "name", 
                    s.quantity as "lot", 
                    s.multiplier as "multipler",
                    s.profit_loss as "profit_loss",
                    (200 * s.quantity) as "brokrage",
                    t.offerPrice AS "buy_price",
                    s.bidPrice AS "sell_price",
                    t.created_at AS "buy_time",
                    s.created_at AS "sell_time"
                FROM
                playground_squredofftransactions s
                LEFT JOIN
                    playground_transactions t ON t.transaction_id = s.parent_transaction
                LEFT JOIN 
                    playground_clientprofile u ON t.client_id = u.client_id
                WHERE
                    t.client_id IN ({client_ids_string})
                    AND t.action = 'Sell'
                    AND s.action = 'Buy'
                    AND s.created_at >= NOW() - INTERVAL 7 DAY;     
            ''')

            columns = [col[0] for col in cursor.description]
            transactions =  [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    context['transactions'] = transactions    

    return render(request, 'pages/squaredofftransactions.html', context)


@login_required(login_url='/login')
def clients(request):
    context = {}
    user = request.user
    user = ClientProfile.objects.filter(user_id=user.id).first()
    context['client'] = user

    GetMyUsers = User.objects.filter(is_active=True).values_list('id')
    
    Users = ClientProfile.objects.filter(user_id__in=GetMyUsers).annotate(
        active_transaction_count=Count('transactions', filter=Q(transactions__status=1))
    ).filter(active_transaction_count__gt=0)
    context['users'] = Users

    transactions = Transactions.objects.filter(status=1).order_by('client')
    transaction_serilizer = TransactionsSerializers(transactions, many=True)
    context['transactions'] = transaction_serilizer.data   
    

    scripts = Scripts.objects.filter(status=True)
    scripts_serializer  = ScriptsSerializers(scripts, many=True)
    context['scripts'] = scripts_serializer.data

    apptoken = app_configs.objects.filter(name="api_token").first()
    context['api_token'] = apptoken.value
    
    return render(request, 'pages/clients.html', context)

@login_required(login_url='/login')
def settings(request):
    context = {}
    user = request.user
    user = ClientProfile.objects.filter(user_id=user.id).first()
    context['client'] = user

    all_settings = app_configs.objects.all()
    for setting in all_settings:
        context[setting.name] = setting.value

    scripts = Scripts.objects.filter(status=True)
    context['scripts'] = scripts
    return render(request, 'pages/settings.html', context)

@login_required(login_url='/login')
def help(request):
    context = {}
    user = request.user
    user = ClientProfile.objects.filter(user_id=user.id).first()
    context['client'] = user
    return render(request, 'pages/help.html', context)

@login_required(login_url='/login')
def add_transaction_page(request):
    if request.method == "POST":
        t = TransactionForm(request.POST)
        if t.is_valid():
            t.save()
        return HttpResponseRedirect("/transactions")
    else:
        context = {}

        user = request.user
        user = ClientProfile.objects.filter(user_id=user.id).first()
        context['client'] = user

        form = TransactionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            # save the form data to model
            form.save()
    
        context['form']= form
        return render(request, "pages/add_transaction.html", context)    


@login_required(login_url='/login')
def user_details(request, clientID):
    
    context = {}
    user = request.user
    user = ClientProfile.objects.filter(user_id=user.id).first()
    context['client'] = user

    user = ClientProfile.objects.filter(client_id=clientID).first()
    # GetMyClient = ClientProfile.objects.filter(parent_id=user.client_id).values_list('client_id')
    
    context['request_client'] = user

    transactions = Transactions.objects.filter(client_id=user.client_id)
    context['transactions'] = transactions
    
    # user = ClientProfile.objects.filter(client_id=clientID).first()
    return render(request, 'pages/user_details.html', context)


@login_required(login_url='/login')
def get_script(request):
    symbol = request.GET.get('symbol')
    
    if os.path.exists("scripts.csv"):
        df = pd.read_csv("scripts.csv")
        df = df[df['optionType'] == "FUT"]
        df = df[df['tradingSymbol'] == symbol]
        json_data = df.to_json(orient='records')        
        return HttpResponse(json_data, content_type='application/json')
    else:
        return "Please refresh script list"

@login_required(login_url='/login')
def add_script(request):
    
    data = json.loads(request.body)
    scriptCode = data.get('scriptCode')

    if os.path.exists("scripts.csv"):
        
        script = Scripts.objects.filter(script_code=scriptCode, status=True).first()
        if script:
            return HttpResponse("The Requested Script is Already Added")
        else:
            df = pd.read_csv("/var/www/html/melody-dev/scripts.csv")
            df = df[df['scripCode'] == int(scriptCode)]
            json_data = df.to_json(orient='records')
            json_data = json.loads(json_data)

            if len(json_data) > 0:
                script = Scripts()
                script.script_code = json_data[0]['scripCode']
                script.tradingSymbol = json_data[0]['tradingSymbol']
                script.lotSize = int(json_data[0]['lotSize'])
                script.multiplier = int(json_data[0]['multiplier'])
                script.optionType = json_data[0]['optionType']

                expiry = datetime.datetime.strptime(json_data[0]['expiry'], "%d/%m/%Y")
                script.expiryDate = expiry.date()

                script.status = True
                script.save()
                return HttpResponse("success")
            else:
                return HttpResponse("Script Code was not found")
    else:
        return HttpResponse("There was an erro Processing your request, please try again")

@login_required(login_url='/login')
def save_script_list_file(request):
    try:
        token = app_configs.objects.get(name="api_token")
        # return [
        #   { "symbol": "AAPL", "expirydate": "2023-06-30", "code": 1234 }
        # ]
        url = "https://api.sharekhan.com/skapi/services/master/MX"

        payload = ""
        headers = {
            'access-token': token.value,
            'api-key': '2ndfeZojiGUjxuBaHvjsvwG7UIS4CZhH',
            'Cookie': 'JSESSIONID=FE75F808C4A613C1002851C188B58E4D; TS014cf12d=010aca028e701df0640e82ae6399ab91b1bcd31f89141ea77c6879608bb48166673adc391a9bfc64fbc0ea75e676cbb228f9c99c469ea205e30ce53780a075635b8908ce24; TS0177cd8b=010aca028e32fd0357baa8fdaaf8fb9c9b4ad464c4141ea77c6879608bb48166673adc391a63d3c1c9e0f56b3349b77040fcf74d9d'
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            jsonData = response.json()
            df = pd.json_normalize(jsonData['data'])
            df.to_csv("/var/www/html/melody-dev/scripts.csv", index=False)
            return HttpResponse("Scripts Updated")
        
        return HttpResponse("Unable to update scripts")
    except Exception:
        return HttpResponse("Internal server error")

    
