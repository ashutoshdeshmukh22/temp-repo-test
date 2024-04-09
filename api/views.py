import os
import requests
import json
from datetime import datetime
from cryptography.fernet import Fernet

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from playground.models import ClientProfile, app_configs, Transactions, SquredOffTransactions,  token_log, Scripts
from .serializers import ClientSerializer, AppConfigSerializer, TransactionSerializer,  SquaredOffTransactionSerializer, ScriptsSerializers

from .utilities import error, logerror
from .Encode_Decode import DecodeEncodeString


@api_view(['POST'])
def login(request):

    jsonData = request.data
    if ('username' in jsonData) and ('password' in jsonData):
        username = jsonData['username']
        password = jsonData['password']

        user = authenticate(request, username=username, password=password)
        # print(user)
        
        if user is not None:
            token = RefreshToken.for_user(user)
            client = ClientProfile.objects.filter(user_id=user.id).first()

            data = { "status": "success",
                "data": {
                    "username": user.username,
                    "client_id": client.client_id,
                    "name": user.first_name, 
                    "email": user.email,
                    "limit": float(client.limit),
                    "access_token": str(token.access_token),
                    "created_at": client.user.date_joined.strftime("%Y-%m-%d %H:%M")
                    #"refresh_token": str(token),
                    #"expires_after": 86400
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(error("Invalid username or password, please try again"), status=status.HTTP_401_UNAUTHORIZED)
    else:
        
        return Response(error("Please provide Username and password"), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_password(request):
    try:
        jsonData = request.data
        if 'new_password' in jsonData:

            client = User.objects.filter(id=request.user.id).first()
            client.set_password(jsonData['new_password'])
            client.save()
            data = {
                "status": "success",
                "message": "Password Changed Successfully."
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(error("Please input required parameter"), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(str(e))
        return Response(error("Internal server error, please try again later."), status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def profile(request):
    profile_payload = request.data.get("client_id")
    user_details = ClientProfile.objects.filter(client_id=str(profile_payload)).first()
    
    # data = ClientSerializer(user_details, many=False)    
    jsonData = {
        "success": True,
        "message": "",
        "data": {
            "limit": user_details.limit,
            "client_id": user_details.client_id,
            "app_version": "1.0.0",
            "created_at": user_details.user.date_joined.strftime("%Y-%m-%d %H:%M")
        }
    }
    return Response(jsonData, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def token_add(request):
    try:
        post_data = request.data
        if 'request_id' in post_data:
            
            primary_token = ""
            request_token = post_data['request_id']
            obj = DecodeEncodeString(request_token=request_token)
            new_token = obj.get_token()

            token_log_obj = token_log()
            token_log_obj.request_url = request_token
            token_log_obj.encrypted_token = new_token
            token_log_obj.save()
            
            url = "https://api.sharekhan.com/skapi/services/access/token"

            payload = {
                "apiKey": "2ndfeZojiGUjxuBaHvjsvwG7UIS4CZhH",
                "requestToken": new_token.decode("UTF-8"),
                "versionId": 1005
            }
            headers = { 'Content-Type': 'application/json' }

            response = requests.request("POST", url, headers=headers, json=payload)
            jsonData = response.json()
            if jsonData['status'] == 200 and 'data' in jsonData:
                primary_token = jsonData['data']['token']

                # cipher_suite = Fernet(os.getenv('IvKEY', ''))
                # primary_token = cipher_suite.encrypt(primary_token.encode())

                appconfigs = app_configs.objects.filter(name="api_token").first()
                appconfigs.value = primary_token
                appconfigs.save()
            else:
                return Response(error(jsonData['message']), status=status.HTTP_400_BAD_REQUEST)
            

            return Response({"status": "success", "message": "Data Added", "data": {}}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(error(f"Something went wrong, please try again {str(e)}"), status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def edit_user(request):
    post_data = request.data
    username = post_data.get("username")
    user = User.objects.filter(username=username).first()

    if user:
        if "name" in post_data:
            user.first_name = post_data.get("name")
        if "email" in post_data:
            user.email = post_data.get("email")
        if "is_active" in post_data:
            user.is_active = post_data.get("is_active")

        client = ClientProfile.objects.filter(user_id=user.id).first()
        if client:
            if "phone" in post_data:
                client.phone = post_data.get("phone")
            if "limit" in post_data:
                client.limit = post_data.get("limit")

        user.save()
        if client:
            client.save()

        return Response({"status": "success", "message": "Data updated", "data": {}}, status=status.HTTP_200_OK)
    else:
        return Response(error("Incorrect User details provided."), status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_user(request):
    jsonData = request.data
    if 'username' in jsonData:
        user = User.objects.filter(username=jsonData['username']).first()
        items = ClientProfile.objects.filter(user=user).first()
        transactions = Transactions.objects.filter(client_id=items.client_id)
        transactions_serializer = TransactionSerializer(transactions, many=True)

        data = {
            "status": "success",
            "data": {
                "clientID": user.username,
                "name": user.first_name,
                "email": user.email,
                "phone": items.phone,
                "limit": items.limit,
                "note": items.note,
                "transactions": transactions_serializer.data
            }
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(error("Please provide username"), status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def settings(request):
    try:
        all_settings = app_configs.objects.all()
        serializer = AppConfigSerializer(all_settings, many=True)
        
        available_scripts = Scripts.objects.filter(status=True)
        ScriptsSerializer = ScriptsSerializers(available_scripts, many=True)
        
        data = {
            "status": "success",
            "data": serializer.data,
            "active_scripts": ScriptsSerializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logerror(request, str(e))
        return Response(error("Internal Error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_settings(request):
    try:
        post_data = request.data
        for key, value in post_data.items():
            all_settings = app_configs.objects.filter(name=key).first()
            all_settings.value = value
            all_settings.save()
    
        data = {
            "status": "success",
            "message": "Configuration Updated Successfully",
            "data": {}
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logerror(request, str(e))
        return Response(error("Internal Error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_transaction(request):
    
    configuration = app_configs.objects.filter(name="transaction_status").first()
    if configuration.value == "False":
        return Response(error("Please try again after sometimes."))
    
    try:
        payload = request.data
        fields_to_validate = ['client_id', 'script_code', 'name', 'quantity','price','action', 'created_by']
        if all(key in payload for key in fields_to_validate):
            
            client_id = payload['client_id']
            if payload['action'] == "Buy" or payload['action'] == "Sell":
                
                client_profile = ClientProfile.objects.filter(client_id=client_id).first()
                
                if client_profile.limit <= 0:
                    return Response(error("Insufficient limit.")) 
                
                existing_transactions = Transactions.objects.filter(client_id=client_profile.client_id, status=1, script_code=payload['script_code']).first()
                
                if existing_transactions:
                    if(existing_transactions.action == "Buy" and payload['action'] == "Sell"):
                        return Response(error("Please sell item from holding.")) 
                    
                    if(existing_transactions.action == "Sell" and payload['action'] == "Buy"):
                        return Response(error("Please buy item from holding.")) 

                transaction = Transactions()
                transaction.client_id = client_profile
                transaction.script_code = payload['script_code']
                transaction.name = payload['name']
                transaction.quantity = payload['quantity']
                transaction.price = payload['price']
                transaction.action = payload['action']
                transaction.created_by = payload['created_by']
                transaction.bidPrice = float(payload['bidPrice'])
                transaction.offerPrice = float(payload['offerPrice'])
                transaction.expirydate = payload['expirydate']
                transaction.multiplier = payload['multiplier']
                transaction.lotSize = payload['lotSize']
                transaction.save()
                
                #client_profile.limit = client_profile.limit - payload['price']
                #client_profile.save()

                transactionSerializer = TransactionSerializer(transaction, many=False) 
                data = {
                    "status": "success",
                    "message": "Order has been Placed Successfully",
                    "data": [transactionSerializer.data]
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(error("You account will be block soon."), status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(error("There was error processing your request, please try again after."))

    except Exception as e:
        logerror(request, str(e))
        return Response(error(), status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_squaredoff_transactions(request):
    
    try:
        payload = request.data
        transactions = SquredOffTransactions.objects.all()

        if 'client_id' in payload:
            if payload['client_id'] != "":
                transactions = transactions.filter(client_id=payload["client_id"]).order_by('-created_at')
            else:
                return Response(error("Please provide valid ClientID"), status=status.HTTP_400_BAD_REQUEST)

        if 'start_date' in payload:
            try:
                if payload['start_date'] != "":
                    date = datetime.strptime(payload["start_date"], "%d-%m-%Y");
                    transactions = transactions.filter(created_at__gte=date).order_by('-created_at')
                else:
                    return Response(error("Please provide valid date"), status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(error("Date Format should be DD-MM-YYYY format"), status=status.HTTP_400_BAD_REQUEST)
            
        
        transactionserializer = SquaredOffTransactionSerializer(transactions, many=True)
        data = {
            "status": "success",
            "message": "",
            "data": transactionserializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        logerror(request, str(e))
        return Response(error(), status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_transactions(request):
    
    try:
        payload = request.data
        transactions = Transactions.objects.filter(status=True)

        if 'client_id' in payload:
            if payload['client_id'] != "":
                transactions = transactions.filter(client_id=payload["client_id"]).order_by('-created_at')
            else:
                return Response(error("Please provide valid ClientID"), status=status.HTTP_400_BAD_REQUEST)

        # if 'start_date' in payload:
        #     try:
        #         if payload['start_date'] != "":
        #             date = datetime.strptime(payload["start_date"], "%d-%m-%Y");
        #             transactions = transactions.filter(created_at__gte=date)
        #         else:
        #             return Response(error("Please provide valid date"), status=status.HTTP_400_BAD_REQUEST)
        #     except Exception as e:
        #         return Response(error("Date Format should be DD-MM-YYYY format"), status=status.HTTP_400_BAD_REQUEST)
            
        
        transactionserializer = TransactionSerializer(transactions, many=True)
        data = {
            "status": "success",
            "message": "",
            "data": transactionserializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        logerror(request, str(e))
        return Response(error(), status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_transaction(request):
    try:
        payload = request.data
        if all(key in payload for key in ['client_id', 'transaction_id']):
           
            try:
                client_id = payload['client_id']
                transaction_id = payload['transaction_id']

                transaction = Transactions.objects.filter(transaction_id=transaction_id).first()

                if 'price' in payload:
                    transaction.price = payload['price']
                
                if 'created_at' in payload:
                    transaction.created_at = payload['created_at']

                if 'updated_at' in payload:
                    transaction.created_at = payload['updated_at']

                if 'script_code' in payload:
                    transaction.script_code = payload['script_code']

                if 'quantity' in payload:
                    transaction.quantity = payload['quantity']

                transaction.updated_by = client_id
                transaction.updated_at = datetime.now()

                transaction.save()
                data = {
                    "status": "success",
                    "message": "Transaction updated successfully",
                    "data": []
                }
                return Response(data, status=status.HTTP_200_OK)

            except Exception as e:
                logerror(request, str(e))
                return Response(error(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(error("Please provide sufficient details"), status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print
        logerror(request, str(e))
        return Response(error(), status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_squredoff_transaction(request):
    
    configuration = app_configs.objects.filter(name="transaction_status").first()
    if configuration.value == "False":
        return Response(error("Please try again after sometimes."))

    try:
        payload = request.data
        fields_to_validate = ['transaction_id', 'client_id', 'script_code', 'name', 'quantity','price','action', 'created_by']
        if all(key in payload for key in fields_to_validate):
            
            client_id = payload['client_id']
            if payload['action'] == "Buy" or payload['action'] == "Sell":
                
                client_profile = ClientProfile.objects.filter(client_id=client_id).first()
                parent_transaction = Transactions.objects.filter(transaction_id=payload['transaction_id']).first()

                if (parent_transaction.action == "Buy" and payload['action'] == "Sell") or parent_transaction.action == "Sell" and payload['action'] == "Buy":
                    if parent_transaction:
                        quantity_check = parent_transaction.quantity #5
                        #existing_squared_off_transactions = SquredOffTransactions.objects.filter(parent_transaction=payload['transaction_id']) #1 
                        
                        if parent_transaction.quantity >= payload['quantity']:

                            quantity_check = quantity_check - payload['quantity']

                            if quantity_check == 0:
                                parent_transaction.status = 0

                            parent_transaction.quantity = quantity_check
                            parent_transaction.save()
                        else:
                            return Response(error("Insufficient stock"), status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(error("Invalid Transaction attempted."), status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(error("Invalid transaction."), status=status.HTTP_400_BAD_REQUEST)
                
                transaction = SquredOffTransactions()
                transaction.client_id = client_profile.client_id
                transaction.parent_transaction = payload['transaction_id']
                transaction.script_code = payload['script_code']
                transaction.name = payload['name']
                transaction.quantity = payload['quantity']
                transaction.price = payload['price']
                transaction.profit_loss = round(payload['profit_loss'],2)
                transaction.action = payload['action']
                transaction.created_by = payload['created_by']
                transaction.bidPrice = payload['bidPrice']
                transaction.offerPrice = payload['offerPrice']
                transaction.expirydate = payload['expirydate']
                transaction.multiplier = payload['multiplier']
                transaction.lotSize = payload['lotSize']
                transaction.save()

                client_profile.limit = client_profile.limit + transaction.profit_loss
                client_profile.save()

                data = {
                    "status": "success",
                    "message": "Order has been Completed Successfully",
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(error("You account will be block soon."), status=status.HTTP_403_FORBIDDEN)
        
        else:
            return Response(error("There was error processing your request, please try again after."))

    except Exception as e:
        print(str(e))
        logerror(request, str(e))
        return Response(error(), status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def scripts(request):
    try:
        all_Scripts = Scripts.objects.filter(status=True)
        serializer = ScriptsSerializers(all_Scripts, many=True)

        data = {
            "status": "success",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logerror(request, str(e))
        return Response(error("Internal Error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_script(request):
    try:
        code = request.data.get("script_code")
        lot_size = request.data.get("lot_size")
        multiplier = request.data.get("multiplier")
        script_id = request.data.get("script_id")

        Scriptdata = Scripts.objects.filter(id=int(script_id)).first()
        Scriptdata.lotSize = lot_size
        Scriptdata.multiplier = multiplier
        Scriptdata.save()

        data = {
            "status": "success",
            "data": "Script Updated"
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logerror(request, str(e))
        return Response(error(str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #return Response(error("Internal Error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def remove_scripts(request):
    try:
        scripts_code = request.GET.get("script_code")
        script = Scripts.objects.filter(script_code=int(scripts_code), status=True).first()
        script.status = False

        script.save()

        data = {
            "success": True,
            "data" : [],
            "message": ""
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logerror(request, str(e))
        return Response(error("Internal Server Error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def resolveAll(request):
    
    try:

        profile_payload_client_id = request.data.get("client_id")
        profile = ClientProfile.objects.filter(client_id=profile_payload_client_id).first()

        if profile.limit <= 0:
            return Response(error("Insufficient limit"))
        
        profile.limit = 0
        profile.save()
        
        try:
            request_transactions = json.loads(request.data.get("transactions"))
        except TypeError as e:
            request_transactions = request.data.get("transactions")
            
        transactions = Transactions.objects.filter(client_id=profile_payload_client_id)
        # transactions = transactions.filter(client_id=profile_payload_client_id)
        
        for trans in transactions:

            profit_loss = 0.00
            for req_transaction in request_transactions:
                if trans.transaction_id == req_transaction['transaction_id']:
                    profit_loss = req_transaction['profit_loss']

            transaction = SquredOffTransactions()
            transaction.client_id = profile_payload_client_id
            transaction.script_code = trans.script_code
            transaction.name = trans.name
            transaction.quantity = trans.quantity
            transaction.price = trans.price
            
            if trans.action == "Buy":
                transaction.action = "Sell"
            else:
                transaction.action = "Buy"

            # transaction.created_by = trans.created_by
            transaction.bidPrice = trans.bidPrice
            transaction.offerPrice = trans.offerPrice
            transaction.expirydate = trans.expirydate
            transaction.multiplier = trans.multiplier
            transaction.lotSize = trans.lotSize
            transaction.parent_transaction = trans.transaction_id
            transaction.profit_loss = round(profit_loss, 2)
            transaction.save()
            trans.status = 0;
            trans.save()
        
        data = {
            "success": True,
            "data" : [],
            "message": "All Tranasctions has been Squared-Off."
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logerror(request, str(e))
        return Response(error("Internal Server Error"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def fetch_cliens_portfolio(request):
    
    try:
        
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        print(one_minute_ago)

        transactions = Transactions.objects.filter(status=1, created_at__gte=one_minute_ago).order_by('client')
        transaction_serilizer = TransactionSerializer(transactions, many=True)
        
        data = {
            "success": True,
            "data" : transaction_serilizer.data,
            "message": ""
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(error("Internal Server Error"), status=status.HTTP_400_BAD_REQUEST)