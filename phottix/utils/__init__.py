from django.shortcuts import render_to_response
from django.template import RequestContext


PAGE_SIZE = 10

def render_response(request, template, dic):
    return render_to_response(template, dic, context_instance=RequestContext(request))