from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .requestor import Requestor
from elasticsearch import exceptions


# Create your views here.
class BuildIndexNameSearch(APIView):
    '''
        View to expose Post method for searching
        Expected payload
        {
            "term": "what to search for",
            "address": {
                "country": "two letters country abbreviation"
                "location": "geo_point with format lat, lon"
            },
            "preferences": ["List of","regularly bought","products"]
        }
    '''

    def post(self, request):
        requestor = Requestor()
        try:
            matches = requestor.get_matches(request.data)

        except exceptions.ConnectionTimeout:
            return Response({"Error": "ES did timeout"}, status= status.HTTP_408_REQUEST_TIMEOUT)
        except exceptions.ConnectionError:
            return Response({"Error":"ES not found"}, status= status.HTTP_404_NOT_FOUND)

        return Response(matches, status= status.HTTP_200_OK)