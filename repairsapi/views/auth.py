from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from repairsapi.models import Customer, Employee


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    email = request.data['email']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=email, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    account_type = request.data.get('account_type', None)
    if account_type is None:
        return Response({'message': 'You must supply an account type'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['email'],
        email=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    # Now save the extra info in the levelupapi_gamer table

    account = None

    if account_type == 'customer':
        account = Customer.objects.create(
            address=request.data['address'],
            user=new_user
        )
    elif account_type == 'employee':
        account = Employee.objects.create(
            specialty=request.data['specialty'],
            user=new_user
        )


    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=account.user)
    # Return the token to the client
    data = { 'token': token.key }
    return Response(data)
