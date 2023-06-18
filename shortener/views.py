import csv

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Url
from .serializers import UrlSerializer


class UrlListViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer


class UrlShortener(APIView):
    def post(self, request, origin_url):
        try:
            url = Url.objects.get(url=origin_url)
        except:
            url = Url(url=origin_url)
            url.save()
        short_url = url.short_url
        return Respose(short_url)


class UrlView(APIView):
    def get(self, request, hash):
        url = Url.objects.get(url_hash=hash)
        url = url.url

        return HttpResponseRedirect(url)

class UrlExport(APIView):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export.csv'
        writer = csv.writer(response)
        fileds = Url.objects.all().values_list('url', 'short_url')
        for row in fields:
            writer.writerow(row)

        return response