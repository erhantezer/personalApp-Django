from rest_framework import status
from rest_framework import generics
from personalApp.models import Department, Personal
from rest_framework.generics import GenericAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from personalApp.serializers import DepartmentPersonalSerializer, DepartmentSerializer, PersonalSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class DepartmentView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    # permission_classes = [IsAuthenticated]
    #! only logged in users can make a get request 👆

class DepartmentPersonalView(generics.ListAPIView):
    serializer_class = DepartmentPersonalSerializer
    queryset = Department.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        name = self.kwargs['department']
        return Department.objects.filter(name__iexact=name)
        #! We have made a dynamic url. The user will be able to send requests based on the department name and display only the relevant department.
        #?"name__iexact" method to ignore lowercase or uppercase. This method is used to filter.

class PersonalListCreate(ListCreateAPIView):
    queryset = Personal.objects.all()
    serializer_class=PersonalSerializer
    # permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_superuser or self.request.user.is_staff:
            #! If the related user is "staff" or "superuser", he/she can "create personnel" 👆
            self.perform_create(serializer)
            data = {
                "message": f"Personal {serializer.validated_data.get('first_name')} saved successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "message": "You are not authorized to perform this operation"
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    def perform_create(self, serializer):
        serializer.save()

class PersonalGetUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Personal.objects.all()
    serializer_class=PersonalSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    #! Since the default lookup-field is "pk", when we send it from the url with pk, it happens even if we don't write it. 👆

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.update(request, *args, **kwargs)
        else:
            data = {
                "message": "You are not authorized to perform this operation"
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_superuser:
            self.perform_destroy(instance)
            data = {
                "message": f"Name: {instance.first_name} deleted."
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            data = {
                "message": "You are not authorized to perform this operation"
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def perform_destroy(self, instance):
        instance.delete()