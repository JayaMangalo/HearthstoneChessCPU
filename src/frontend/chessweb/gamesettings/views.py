from django.http import HttpResponse
from django.template import loader

def index(request):
    latest_question_list = []
    template = loader.get_template('gamesettings/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))