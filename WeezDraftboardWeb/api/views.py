from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Adp  # Player
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response

"""
class PlayerListView(viewsets.ModelViewSet):  # APIView   
    def list(self, request):
        players = Player.objects.all()  # Retrieve all Player objects from the database
        serializer = PlayerSerializer(players, many=True)  # Serialize the players
        return Response(serializer.data)  # Return the serialized data as a response
    
    def get_queryset(self):
        return Player.objects.all()
"""
class ReactView(APIView):
    def get(self, request):
        output = [{'name': output.name, 
                   'position': output.position, 
                   'team': output.team,
                   } for output in Adp.objects.all()]
        return Response(output)
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# Create your views here.
def main(request):
    return HttpResponse("Hello")
    # return render(request, 'main.html')

def draftboard(request):
    return HttpResponse("Draftboard")

def react(ReactView):
    return HttpResponse(ReactView)

