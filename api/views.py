from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Campaign, Category
from api.serializers import CampaignSerializer, CategorySerializer
import json
from django.db.models import Q
import urllib
import random
#from api.fields import JSONField
#TEst test Tttests

class CampaignList(APIView):
    '''Get all campaings or create a category'''
    @csrf_exempt
    def get(self, request, format=None):
        camp = Campaign.objects.all()[:500]
        if request.query_params.get('title'):
            camp = camp.filter(title__contains=request.query_params.get('title'))
        elif request.query_params.get('category_id'):
            camp = camp.filter(category_id__contains=request.query_params.get('category_id'))
        serializer = CampaignSerializer(camp, many=True)
        return Response(serializer.data)
        
    @csrf_exempt
    def post(self, request, format=None):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CampaignDetail(APIView):
    @csrf_exempt
    def get(self, request, pk, format=None):
        camp = Campaign.objects.get(id=pk)
        serializer = CampaignSerializer(camp)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk, format=None):
        camp = Campaign.objects.get(id=pk)
        serializer = CampaignSerializer(camp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, pk, format=None):
        camp = Campaign.objects.get(id=pk)
        camp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryList(APIView):
    '''Get all categories or create a category'''
    @csrf_exempt
    def get(self, request, format=None):
        cats = Category.objects.all()
        if request.query_params.get('category_id'):
            cats = cats.filter(category_id__contains=request.query_params.get("category_id"))
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    '''Work with an individual Category object'''
    @csrf_exempt
    def get(self, request, pk, format=None):
        cat = Category.objects.get(id=pk)
        serializer = CategorySerializer(cat)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk, format=None):
        cat = Category.objects.get(id=pk)
        serializer = CategorySerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, pk, format=None):
        cat = Category.objects.get(id=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SearchCampaign(APIView):
    
    @csrf_exempt
    def post(self, request, format=None):
        search_in = request.data.get('search_in', 'everything')
        search = request.data.get('search')
        campaigns = []

        if search:
            query = search.split(" ")

            if search_in == 'everything':
                q_object = Q(title__icontains=query[0]) | Q(user_first_name__icontains=query[0]) | Q(location_city__icontains=query[0]) | Q(location_country__icontains=query[0])
                query = query[1:]
                for term in query:
                    q_object.add(Q(title__icontains=term) | Q(user_first_name__icontains=term) | Q(location_city__icontains=term) | Q(location_country__icontains=term), Q.AND)
                
                q_object_match = Q(title__iexact=search) | Q(user_first_name__iexact=search) | Q(location_city__iexact=search) | Q(location_country__iexact=search)
    
            if search_in == 'title':
                q_object = Q(title__icontains=query[0])
                query = query[1:]
                for term in query:
                    q_object.add(Q(title__icontains=term), Q.AND)
                
                q_object_match = Q(title__iexact=search)
    
            if search_in == 'user_first_name':
                q_object = Q(user_first_name__icontains=query[0])
                query = query[1:]
                for term in query:
                    q_object.add(Q(user_first_name__icontains=term), Q.AND)
                
                q_object_match = Q(user_first_name__iexact=search)
    
            if search_in == 'location_city':
                q_object = Q(location_city__icontains=query[0])
                query = query[1:]
                for term in query:
                    q_object.add(Q(location_city__icontains=term), Q.AND)
                
                q_object_match = Q(location_city__iexact=search)
    
            if search_in == 'location_country':
                q_object = Q(location_country__icontains=query[0])
                query = query[1:]
                for term in query:
                    q_object.add(Q(location_country__icontains=term), Q.AND)
                
                q_object_match = Q(location_country__iexact=search)

            #Get query results count for exact
            exactCount=Campaign.objects.filter(q_object_match).count()
            search_done=True if exactCount >= 100 else False

            if search_done == True:
                campaigns=Campaign.objects.filter(q_object_match)[:100]
            else:
                containLimit=100 - exactCount
                # Get IDs for excluding duplicates from icontains queryset
                exactIDs=Campaign.objects.filter(q_object_match).values_list('id', flat=True)
                campaignsExact=Campaign.objects.filter(q_object_match)
                #Get query results for contain while excluding the exact results and limited total results to 100
                campaignsContain=Campaign.objects.filter(q_object).exclude(id__in=exactIDs)[:containLimit]
                #combine both queries while preserving order (iexact query then icontain query)
                campaigns=list(campaignsExact) + list(campaignsContain)

        campSerializer = CampaignSerializer(campaigns, many=True)

        return Response(campSerializer.data)
        
class Predict(APIView):
        
    @csrf_exempt
    def post(self, request, format=None):
        goal = request.data.get('goal')
        is_charity = request.data.get('is_charity')
        has_beneficiary = request.data.get('has_beneficiary')
        visible_in_search = request.data.get('visible_in_search')

        data =  {

            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["current_amount", "goal", "donators", "days_active", "has_beneficiary", "visible_in_search", "is_charity", "num_updates"],
                        "Values": [ [ "0", goal, random.randrange(23, 52, 1), random.randrange(2, 6, 1), has_beneficiary, visible_in_search, is_charity, "0" ] ]
                    },        
            },
            "GlobalParameters": {
            }
        }
    
        body = str.encode(json.dumps(data))
        
        url = 'https://ussouthcentral.services.azureml.net/workspaces/28c200bc63134d0ca21a29c5fd9024ca/services/f4496d433b9b47709873dedb98c1d0ac/execute?api-version=2.0&details=true'
        api_key = '' # Replace this with the API key for the web service
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers) 

        try:
            response = urllib.request.urlopen(req)

            # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
            # req = urllib.request.Request(url, body, headers) 
            # response = urllib.request.urlopen(req)

            result = response.read()
            amount = json.loads(result)['Results']['output1']['value']['Values'][0][8]
            print(result) 
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())

            print(json.loads(error.read()))    


        return Response(amount)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
 
 


                                            