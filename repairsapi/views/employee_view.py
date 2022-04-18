"""View module for handling requests for employee data"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from repairsapi.models import Employee


# TODO: Make employees users of the system that can log in with the client app.
#       Make sure all employees are marked as staff members, but no customers are.

class EmployeeView(ViewSet):
    """Honey Rae API employees view"""

    def create(self, request):
        """Unsupported from customer facing client"""

        # TODO: Once employees can authenticate, make one of them
        return Response({'message': 'Unsupported HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single employee

        Returns:
            Response -- JSON serialized employee record
        """
        employee = Employee.objects.get(pk=pk)
        serialized = EmployeeSerializer(employee, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all employees

        Returns:
            Response -- JSON serialized list of employees
        """
        employees = Employee.objects.all()
        serialized = EmployeeSerializer(employees, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Unsupported from customer facing client"""
        return Response({'message': 'Unsupported HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        """Unsupported from customer facing client"""
        return Response({'message': 'Unsupported HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for employees"""
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    class Meta:
        model = Employee
        fields = ('id', 'name', 'specialty')
