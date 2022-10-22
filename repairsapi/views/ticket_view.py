"""View module for handling requests for serviceTicket data"""
from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Customer, Employee, employee


# TODO: Make serviceTickets users of the system that can log in with the client app.
#       Make sure all serviceTickets are marked as staff members, but no customers are.

class ServiceTicketView(ViewSet):
    """Honey Rae API service tickets view"""

    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        new_ticket = ServiceTicket()
        new_ticket.customer = Customer.objects.get(user=request.auth.user)
        new_ticket.description = request.data['description']
        new_ticket.emergency = request.data['emergency']
        new_ticket.save()

        serialized = ServiceTicketSerializer(new_ticket, many=False)

        # TODO: This method should return a JSON serialization of the newly created ticket
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single serviceTicket

        Returns:
            Response -- JSON serialized serviceTicket record
        """
        serviceTicket = ServiceTicket.objects.get(pk=pk)
        serialized = ServiceTicketSerializer(serviceTicket)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all serviceTickets

        Returns:
            Response -- JSON serialized list of serviceTickets
        """

        # TODO: Order tickets by date and ememergency. Incomplete come first
        #       and, of those, emergencies come first.
        #           "django query order by multiple fields"

        if request.auth.user.is_staff:
            serviceTickets = ServiceTicket.objects.all().order_by("date_completed", "-emergency")
        else:
            serviceTickets = ServiceTicket.objects.filter(customer__user=request.auth.user).order_by("date_completed", "-emergency")

        serialized = ServiceTicketSerializer(serviceTickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Unsupported from customer facing client"""
        return Response({'message': 'Unsupported HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        """Handle PUT requests for single customer

        Returns:
            Response -- No response body. Just 204 status code.
        """
        try:
            # Get the customer based on primary key in the URL
            ticket = ServiceTicket.objects.get(pk=pk)

            # Update the record and save back to the database
            ticket.employee = Employee.objects.get(pk=request.data['employee'])
            ticket.save()

            # Respond with no body and a 204 status code
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        # A PUT request was made for a serviceTicket that doesn't exist
        except ServiceTicket.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        # Capture any other exceptions that might occur and respond with 500 status code
        except Exception as ex:
            return HttpResponseServerError(ex)

# class TicketCustomerSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Customer
#         fields = ('id', 'full_name', )

# class TicketEmployeeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Employee
#         fields = ('id', 'full_name', )

class ServiceTicketSerializer(serializers.ModelSerializer):
    """JSON serializer for serviceTickets"""
    # customer = TicketCustomerSerializer()
    # employee = TicketEmployeeSerializer()

    # TODO: The client wants the customer to have a name property.
    #       Currently just has `user` property with primary key value
    class Meta:
        model = ServiceTicket
        fields = ( 'id', 'description', 'emergency', 'date_completed', 'employee', 'customer', )
        depth = 1











        """
        {
        "model": "auth.user",
        "pk": 5,
        "fields": {
            "password": "pbkdf2_sha256$320000$uQoUQDZFaeKVXC2MUgY09S$uMGAQP+ynhKO97riVNkRxPeHou2quYm9Wf0KviDeREs=",
            "last_login": null,
            "is_superuser": false,
            "username": "emily@lemmon.com",
            "first_name": "Emily",
            "last_name": "Lemmon",
            "email": "emily@lemmon.com",
            "is_staff": true,
            "is_active": true,
            "date_joined": "2022-04-16T15:47:31.654Z",
            "groups": [],
            "user_permissions": []
        }
    },
    {
        "model": "auth.user",
        "pk": 6,
        "fields": {
            "password": "pbkdf2_sha256$320000$uQoUQDZFaeKVXC2MUgY09S$uMGAQP+ynhKO97riVNkRxPeHou2quYm9Wf0KviDeREs=",
            "last_login": null,
            "is_superuser": false,
            "username": "leah@gwin.com",
            "first_name": "Leah",
            "last_name": "Gwin",
            "email": "leah@gwin.com",
            "is_staff": true,
            "is_active": true,
            "date_joined": "2022-04-16T15:47:31.654Z",
            "groups": [],
            "user_permissions": []
        }
    },
    {
        "model": "auth.user",
        "pk": 7,
        "fields": {
            "password": "pbkdf2_sha256$320000$uQoUQDZFaeKVXC2MUgY09S$uMGAQP+ynhKO97riVNkRxPeHou2quYm9Wf0KviDeREs=",
            "last_login": null,
            "is_superuser": false,
            "username": "kimmy@bird.com",
            "first_name": "Kimmy",
            "last_name": "Bird",
            "email": "jenna@solis.com",
            "is_staff": true,
            "is_active": true,
            "date_joined": "2022-04-16T15:47:31.654Z",
            "groups": [],
            "user_permissions": []
        }
    },
    {
        "model": "auth.user",
        "pk": 8,
        "fields": {
            "password": "pbkdf2_sha256$320000$uQoUQDZFaeKVXC2MUgY09S$uMGAQP+ynhKO97riVNkRxPeHou2quYm9Wf0KviDeREs=",
            "last_login": null,
            "is_superuser": false,
            "username": "kristen@norris.com",
            "first_name": "Kristen",
            "last_name": "Norris",
            "email": "kristen@norris.com",
            "is_staff": true,
            "is_active": true,
            "date_joined": "2022-04-16T15:47:31.654Z",
            "groups": [],
            "user_permissions": []
        }
    },
    {
        "model": "auth.user",
        "pk": 9,
        "fields": {
            "password": "pbkdf2_sha256$320000$uQoUQDZFaeKVXC2MUgY09S$uMGAQP+ynhKO97riVNkRxPeHou2quYm9Wf0KviDeREs=",
            "last_login": null,
            "is_superuser": false,
            "username": "ryan@tanay.com",
            "first_name": "Ryan",
            "last_name": "Tanay",
            "email": "ryan@tanay.com",
            "is_staff": true,
            "is_active": true,
            "date_joined": "2022-04-16T15:47:31.654Z",
            "groups": [],
            "user_permissions": []
        }
    }
        """