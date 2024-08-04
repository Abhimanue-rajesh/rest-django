from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializers import PersonSerializer
from django.shortcuts import get_object_or_404

@api_view(["GET", "POST"])
def index(request):
    courses = {
            "course_name": "Python",
            "learn": ['flask', 'Django', 'Tornado', 'FastAPI'], 
            "provider": "someone"
        }
    if request.method == 'POST':
        data = request.data
        print("this is the data",data)
        print("POST method IN")
        return Response(courses)
    elif request.method == 'GET':
        print("GET method IN")
        return Response(courses)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def person(request):
    if request.method == "GET":
        person_object = Person.objects.all()
        serializer = PersonSerializer(person_object, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == "PUT": 
        # Here we need to pass in all the data to be updated
        # this will need all the values 
        data = request.data 
        reference_object = get_object_or_404(Person, id=data["id"])
        serializer = PersonSerializer(instance=reference_object, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == "PATCH": 
        # here we only need to pass in the needed data to be updated
        # partial updating supported here
        # this will only need the id and the changing field
        data = request.data
        reference_object = get_object_or_404(Person, id=data["id"])
        serializer = PersonSerializer(instance=reference_object ,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    elif request.method == "DELETE":
        data = request.data
        reference_object = get_object_or_404(Person, id=data["id"])
        reference_object.delete()
        return Response({"message": "Person has been deleted"})

