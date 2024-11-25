
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home_view, name='home_view'),
    path('blog/', views.blog_view, name='blog_view'),
    path('contact/', views.contact_view, name='contact_view'),
    path('services/', views.services_view, name='services_view'),
    path('blog_details/', views.blog_details, name='blog_details'),
    path('category/<slug:category>/', views.category_view, name='category_view'),
    path('tag/<slug:tag_slug>/', views.tag_view, name='tag_view'),
    path('blog_details/<int:year>/<int:month>/<int:day>/<slug>/', views.blog_details_view, 
                                                    name='blog_details_view'),
    path('search/', views.post_search, name='post_search'),
    path('/', views.subscribe_view, name='subscribe_view'),
    path('send_newsletter/', views.send_newsletter_view, name='send_newsletter_view'),
    path('contact/', views.contact, name='contact'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('developpement_logiciel/', views.developpement_logiciel, name='developpement_logiciel'),
    path('analyse_donnees/', views.analyse_donnees, name='analyse_de_données'),
    path('consultation/', views.consultation, name='consultation'),
    path('marketing_digital/', views.marketing_digital, name='marketing_digital'),
    path('assistance/', views.assistance, name='assistance'),
    path('consultations/', views.consultation_view, name='consultation_view'),
    path('contacts/', views.contact_view, name='contact_view'),
    path('faq/', views.faq_view, name='faq_view'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('ebooks/', views.liste_ebooks, name='liste_ebooks'),
    path('ebook/<int:ebook_id>/', views.detail_ebook, name='detail_ebook'),
    path('acheter/<int:ebook_id>/', views.redirection_whatsapp, name='redirection_whatsapp'),

]

