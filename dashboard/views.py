from django.shortcuts import render

def mon_dashboard(request):
    return render(request, 'dashboards/dashboards.html')

def buttons(request):
    return render(request, 'dashboards/buttons.html')

def cards(request):
    return render(request, 'dashboards/cards.html')


def not_found(request):
    return render(request, 'dashboards/404.html')

def blank(request):
    return render(request, 'dashboards/blank.html')

def charts(request):
    return render(request, 'dashboards/charts.html')

def forgot_password(request):
    return render(request, 'dashboards/forgot-password.html')

def login(request):
    return render(request, 'dashboards/login.html')

def register(request):
    return render(request, 'dashboards/register.html')

# def tables(request):
#     return render(request, 'dashboards/tables.html')


def utilities_animation(request):
    return render(request, 'dashboards/utilities-animation.html')

def utilities_border(request):
    return render(request, 'dashboards/utilities-border.html')

def utilities_color(request):
    return render(request, 'dashboards/utilities-color.html')

def utilities_other(request):
    return render(request, 'dashboards/utilities-other.html')




from django.shortcuts import render
from .models import Earnings, Task, Request

def dashboard_view(request):
    earnings = Earnings.objects.first()  # Récupérer les données de gains
    tasks = Task.objects.all()
    pending_requests = Request.objects.filter(status='pending').count()

    context = {
        'monthly_earnings': earnings.monthly if earnings else 0,
        'annual_earnings': earnings.annual if earnings else 0,
        'task_completion': tasks.filter(completed=True).count() / tasks.count() * 100 if tasks else 0,
        'pending_requests': pending_requests,
    }

    return render(request, 'dashboards/dashboard.html', context)


from django.shortcuts import render
from django.contrib.auth.models import User  # auth_user correspond au modèle User par défaut

def tables(request):
    users = User.objects.all()  # Récupérer tous les utilisateurs
    return render(request, 'dashboards/tables.html', {'users': users})  # Passer les utilisateurs au template


