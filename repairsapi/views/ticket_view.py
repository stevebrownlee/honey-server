"""View module for handling requests for serviceTicket data"""
from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import ServiceTicket, Customer, Employee


class ServiceTicketView(ViewSet):
    """Honey Rae API service tickets view"""

    def destroy(self, request, pk=None):
        """Handle DELETE requests for service tickets

        Returns:
            Response: None with 204 status code
        """
        service_ticket = ServiceTicket.objects.get(pk=pk)
        service_ticket.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


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

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single serviceTicket

        Returns:
            Response -- JSON serialized serviceTicket record
        """
        service_ticket = ServiceTicket.objects.get(pk=pk)
        serialized = ServiceTicketSerializer(service_ticket)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all serviceTickets

        Returns:
            Response -- JSON serialized list of serviceTickets
        """
        service_tickets = []

        if "status" in request.query_params:
            if request.query_params['status'] == "done":
                service_tickets = ServiceTicket.objects.filter(date_completed__isnull=False)

            if request.query_params['status'] == "unclaimed":
                service_tickets = ServiceTicket.objects.filter(date_completed__isnull=False, employee__isnull=False)

            if request.query_params['status'] == "inprogress":
                service_tickets = ServiceTicket.objects.filter(date_completed__isnull=False, employee__isnull=True)

            if request.query_params['status'] == "all":
                service_tickets = ServiceTicket.objects.all()

        else:
            if request.auth.user.is_staff:
                service_tickets = ServiceTicket.objects.all()
            else:
                service_tickets = ServiceTicket.objects.filter(customer__user=request.auth.user)



        serialized = ServiceTicketSerializer(service_tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Handle PUT requests for single customer

        Returns:
            Response -- No response body. Just 204 status code.
        """

        # Select the targeted ticket using pk
        ticket = ServiceTicket.objects.get(pk=pk)

        # Get the employee id from the client request
        employee_id = request.data['employee']

        # Select the employee from the database using that id
        assigned_employee = Employee.objects.get(pk=employee_id)

        # Assign that Employee instance to the employee property of the ticket
        ticket.employee = assigned_employee

        # Save the updated ticket
        ticket.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TicketEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('id', 'specialty', 'full_name')


class TicketCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'full_name')


class ServiceTicketSerializer(serializers.ModelSerializer):
    """JSON serializer for serviceTickets"""
    employee = TicketEmployeeSerializer(many=False)
    customer = TicketCustomerSerializer(many=False)

    class Meta:
        model = ServiceTicket
        fields = ( 'id', 'description', 'emergency', 'date_completed', 'employee', 'customer', )











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