import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
import json
import os
import requests



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    today = datetime.datetime.today()
    wellcome_message = "Hello, world. Today is " + str(today)
    return HttpResponse(wellcome_message)


def map(request):
    template_path = BASE_DIR.__str__() + "/GeoIPMap/templates/geoipmap.html"
    doc_ext = open(template_path)
    mapgeoip = Template(doc_ext.read())
    doc_ext.close()
    ctx = Context()
    document = mapgeoip.render(ctx)
    return HttpResponse(document)

def geoip(request):
    template_path = BASE_DIR.__str__() + "/GeoIPMap/templates/geoip.html"
    doc_ext = open(template_path)
    geoip = Template(doc_ext.read())
    doc_ext.close()
    now = datetime.date.today()
    ip_address_client = str(request.META.get("REMOTE_ADDR"))
    client_ip_request = "http://ip-api.com/json/" + ip_address_client
    url_request = requests.get(client_ip_request)
    text = url_request.text
    data = json.loads(text)
    log_file(data)
    if data["countryCode"]:
        country_code = data["countryCode"]
    if data["country"]:
        country_name = data["country"]
    #flag_country = FlagCountry(country = country_code)
    flag_link = "https://flagsworld.org/img/cflags/" + country_name +  "-flag.png"
    add_flag = {"flag": flag_link}
    data.update(add_flag)
    log_file(str(request.META.get("REMOTE_ADDR")))
    ip_address_client = str(request.META.get("REMOTE_ADDR"))
    return render(request, template_path, data)


def about(request):
    template_path = BASE_DIR.__str__() + "/GeoIPMap/templates/acercade.html"
    doc_ext = open(template_path)
    geo = Template(doc_ext.read())
    doc_ext.close()
    return render(request, template_path)
