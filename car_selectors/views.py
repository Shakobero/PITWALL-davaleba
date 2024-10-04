from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Make, Model, CarType
from django.db.models import Q

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'  
    max_page_size = 100  

class CarSearchView(viewsets.ViewSet):
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        query = request.query_params.get('make', '')
        texts_to_search = query.split()

        if not texts_to_search:
            return Response({"items": []})

        
        q_objects = Q()
        for text in texts_to_search:
            q_objects |= (
                Q(model__make__name__icontains=text) |
                Q(model__name__icontains=text) |
                Q(name__icontains=text)
            )

        results = CarType.objects.filter(q_objects).select_related('model__make').distinct()

        
        if not results.exists():
            return Response({"items": [], "message": "No cars found matching your search."})

        
        items = [{
            "make": result.model.make.name,
            "model": result.model.name,
            "car_type": result.name,
            "car_type_id": result.id,
        } for result in results]

        
        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(results, request)

        if paginated_results is not None:
            paginated_items = [{
                "make": result.model.make.name,
                "model": result.model.name,
                "car_type": result.name,
                "car_type_id": result.id,
            } for result in paginated_results]
            return paginator.get_paginated_response({"items": paginated_items})

       
        return Response({"items": items})
