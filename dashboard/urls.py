from django.urls import path
from . import views

urlpatterns = [

    path('', views.mon_dashboard, name='mon_dashboard'),
    path('dashboards/buttons', views.buttons, name='buttons'),
    path('dashboards/cards', views.cards, name='cards'),
    path('dashboards/not_found', views.not_found, name='not_found'),
    path('dashboards/blank', views.blank, name='blank'),
    path('dashboards/charts', views.charts, name='charts'),
    path('dashboards/forgot_password', views.forgot_password, name='forgot_password'),
    path('dashboards/login', views.login, name='login'),
    path('dashboards/register', views.register, name='register'),
    # path('dashboards/tables', views.tables, name='tables'),
    path('dashboards/utilities_animations', views.utilities_animation, name='utilities_animation'),
    path('dashboards/utilities_border', views.utilities_border, name='utilities_border'),
    path('dashboards/utilities_color', views.utilities_color, name='utilities_color'),
    path('dashboards/utilities_others', views.utilities_other, name='utilities_other'),



    path('dashboards/tables', views.tables, name='tables'),
]



