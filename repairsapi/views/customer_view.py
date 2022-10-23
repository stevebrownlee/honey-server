"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import Customer


class CustomerView(ViewSet):
    """Honey Rae API customers view"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer record
        """

        # Step 1: Get a single customer based on the primary key in the request URL
        customer = Customer.objects.get(pk=pk)

        # Step 2: Serialize the customer record as JSON
        serialized = CustomerSerializer(customer, context={'request': request})

        # Step 3: Send JSON response to client with 200 status code
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all customers

        Returns:
            Response -- JSON serialized list of customers
        """

        # Step 1: Get all customer data from the database
        customers = Customer.objects.all()

        # Step 2: Convert the data to JSON format
        serialized = CustomerSerializer(customers, many=True)

        # Step 3: Respond to the client with the JSON data and 200 status code
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for single customer

        Returns:
            Response -- No response body. Just 204 status code.
        """

        # TODO: Only allow a customer to delete their own account
        # TODO: Add a "Delete my account" feature to client application

        # Step 1: Get a single customer based on the primary key in the request URL
        customer = Customer.objects.get(pk=pk)

        # Step 2: Delete the customer from the database
        customer.delete()

        # Step 3: Respond with no body and a 204 status code
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """Handle PUT requests for single customer

        Returns:
            Response -- No response body. Just 204 status code.
        """
        try:
            # Get the customer based on primary key in the URL
            customer = Customer.objects.get(pk=pk)

            # Verify that the request was made by the person being updated
            if request.auth.user == customer.user:

                # Update the record and save back to the database
                customer.address = request.data["address"]
                customer.save()

                # Respond with no body and a 204 status code
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            # The PUT request was made by someone who isn't this customer
            else:
                return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        # A PUT request was made for a customer that doesn't exist
        except Customer.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        # Capture any other exceptions that might occur and respond with 500 status code
        except Exception as ex:
            return HttpResponseServerError(ex)


class CustomerSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""

    class Meta:
        model = Customer
        fields = ('id', 'address', 'full_name')
