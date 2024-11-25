from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .models import Post, Comment, Category, Subscriber, Ebook
from .forms import CommentForm, SearchPost, SubscriptionForm, ConsultationForm, ContactForm, EmailPostForm, PostShareForm
from taggit.models import Tag
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage



def home(request):
    return render(request, 'siteweb/bangri.html')

def home_view(request):
    recent_posts = Post.objects.order_by('-published')[:3]
    is_administrateur = request.user.groups.filter(name='administrateur').exists()

    return render(request, 'siteweb/index.html', {'recent_posts': recent_posts, 
                                                  'is_administrateur': is_administrateur,
                                                  })


def category_view(request, category):
    categories = Category.objects.all()
    if category:
        category = get_object_or_404(Category, slug=category)
        posts = Post.objects.filter(category=category).order_by('published')
    return render(request, 'siteweb/category.html', {
        'category': category,
        'posts': posts,
        'categories' : categories,
    })
def tag_view(request, tag_slug):
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])

    return render(request, 'siteweb/tag.html', {
        'tag_slug': tag_slug,
        'posts': posts,
        'tag' : tag,
    })
def blog_details_view(request, year: int, month: int, day: int, slug: str, category=None, tag_slug=None):
    post = get_object_or_404(Post, slug=slug, statut='published', published__year=year, 
                             published__month=month, published__day=day)
    comments = post.comments.filter(parent__isnull=True).prefetch_related('replies')
    form = CommentForm()

    categories = Category.objects.all()
    tags = Tag.objects.all()

    posts = Post.objects.all()

    if category:
        category = get_object_or_404(Category, slug=category)
        posts = posts.filter(category=category).order_by('published')
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    new_comment = None
    if request.method =='POST':
        if request.user.is_authenticated:

            form = CommentForm(request.POST)

            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    parent_comment = Comment.objects.get(id=parent_id)
                    new_comment.parent = parent_comment
                new_comment.save()
                return redirect(reverse('blog_details_view', kwargs={
                    'year': year,
                    'month': month,
                    'day': day,
                    'slug': slug
                }))
        else:
            messages.error(request, "Veillez vous connecter ! ")
            return redirect('login_view')
    else:
        comment_form = CommentForm()
    posts_tag_id = post.tags.values_list("id", flat=True)
    similar_post = Post.objects.filter(tags__in=posts_tag_id).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published')[:3]
    recent_posts = Post.objects.all().exclude(id=post.id)
    recent_posts = recent_posts.order_by('-published')[:3]
        
    return render(request, 'siteweb/blog-details.html',  {
                                                    'post': post,
                                                    'comments': comments,
                                                    'form': form,
                                                    'new_comment': new_comment,
                                                    'comment_form': comment_form,   
                                                    'categories': categories,
                                                    'category': category,
                                                    'tags': tags,
                                                    'similar_post': similar_post,
                                                    'recent_posts': recent_posts,
                                                    })


def blog_view(request):
    posts = Post.published_posts.all()
    posts = posts.order_by('-published')

    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger :
        posts = paginator.page(1)
    except EmptyPage :
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts' : posts,
        'page'  : page,
        
}
    return render(request, 'siteweb/blog.html', context)

def contact_view(request):
    return render(request, 'siteweb/contact.html')

def services_view(request):
    return render(request, 'siteweb/services.html')

def blog_details(request):
    return render(request, 'siteweb/services.html')


# def testimonials_view(request):
#     return render(request, 'siteweb/testimonials.html')

def post_search(request):
    query = None
    results = []
    search_form = SearchPost()

    if 'query' in request.GET:
        search_form = SearchPost(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            vector_search = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            query_search = SearchQuery(query)
            # results = Post.published_posts.annotate(
            #     search=vector_search, rank=SearchRank(vector_search,query_search)
            # ).filter(rank__gte=0.3).order_by('rank')
            results = Post.published_posts.annotate(
                                                    similarity=TrigramSimilarity("title", query),
                                                    ).filter(similarity__gt=0.1).order_by("-similarity")

    return render(request, 'siteweb/search.html', {
        'search_form': search_form,
        'query': query,
        'results': results,
    })

def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to our newsletter.')
            return redirect('home_view')  # Remplace par l'URL de redirection souhaitée
    # else:
    #     form = SubscriptionForm()
    # return render(request, 'siteweb/subscribe.html', {'form': form})
    return render(request, 'siteweb/index.html')

def send_newsletter(subject, message):
    subscribers = Subscriber.objects.values_list('email', flat=True)
    # send_mail(subject, message, 'bikoyemmanuel531@gmail.com', list(subscribers))
    html_message = render_to_string('siteweb/newsletter_template.html', {'subject': subject, 'message': message})
    email = EmailMessage(subject, html_message, 'bikoyemmanuel531@gmail.com', list(subscribers))
    email.content_subtype = "html"  # Important pour envoyer l'email en HTML
    email.send()

def send_newsletter_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_newsletter(subject, message)
        messages.success(request, 'Newsletter envoyée avec succès !')
        return redirect('admin_dashboard_view')  # Redirection vers un tableau de bord admin
    return render(request, 'siteweb/send_newsletter.html')

def contact_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ContactForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                    
                # Logique pour envoyer un email (ou sauvegarder dans la base de données)
                send_mail(
                    subject=f"Message de : {name}",
                    message=f"Subject: {subject}\n\nMessage: {message}",
                    from_email=email,
                    recipient_list=['bikoyemmanuel531@gmail.com'],  # Remplacez par l'email de réception
                    )
                
                messages.success(request, 'Votre message a été envoyé avec succès!')
                return redirect('contact_view')  # Redirection après succès
    
        else:
            messages.error(request, "Vous devez être connecté pour nous contacter.")
            return redirect('login_view')
    else:
        form = ContactForm()
    return render(request, 'siteweb/contact.html', {'form': form})  # Retour au formulaire si GET


def terms_of_service(request):
    return render(request, 'siteweb/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'siteweb/privacy_policy.html')

def developpement_logiciel(request):
    return render(request, 'siteweb/developpement_logiciel.html')

def analyse_donnees(request):
    return render(request, 'siteweb/analyse_donnees.html')

def consultation(request):
    return render(request, 'siteweb/consultation.html')

def marketing_digital(request):
    return render(request, 'siteweb/marketing_digital.html')

def contact(request):
    return render(request, 'siteweb/contact.html')


def assistance(request):
    return render(request, 'siteweb/assistance.html')


def consultation_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ConsultationForm(request.POST)
            if form.is_valid():
                # Récupération des données du formulaire
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                consultation_type = form.cleaned_data['consultation_type']
                message = form.cleaned_data['message']
                
                # Logique pour envoyer un email (ou sauvegarder dans la base de données)
                send_mail(
                    subject=f"Consultation demandée par {name}",
                    message=f"Type de consultation: {consultation_type}\n\nMessage: {message}",
                    from_email=email,  # Utilisation correcte de l'email de l'expéditeur
                    recipient_list=['bikoyemmanuel531@gmail.com'],  # Remplacez par l'email de réception
                )
                messages.success(request, 'Votre demande de consultation a été envoyée avec succès!')
                return redirect('consultation_view')
        else:
            # Envoyer un message d'erreur
            messages.error(request, "Vous devez être connecté !")
            return redirect('login_view')

    else:
        form = ConsultationForm()

    return render(request, 'siteweb/consultation.html', {'form': form})

def faq_view(request):
    faq_items = [
        ("Qu'est-ce que Bangri ?", "Bangri est une startup AgTech qui utilise la technologie pour améliorer la productivité agricole et la durabilité."),
        ("Comment Bangri aide-t-elle les agriculteurs ?", "Nous fournissons des solutions basées sur des données pour optimiser les rendements et réduire les coûts."),
        ("Quels types de cultures sont couverts par Bangri ?", "Nous travaillons avec une variété de cultures, y compris les céréales, les fruits et légumes."),
        ("Comment puis-je m'inscrire à vos services ?", "Pour vous inscrire, visitez notre site web et remplissez le formulaire d'inscription."),
        ("Proposez-vous des essais gratuits ?", "Oui, nous offrons des essais gratuits pour permettre aux agriculteurs de tester nos solutions."),
        ("Comment puis-je contacter le support client ?", "Vous pouvez nous contacter via notre page de contact ou par email à contact@bangri.com."),
        ("Y a-t-il des frais d'abonnement ?", "Nous proposons différents plans d'abonnement adaptés aux besoins des agriculteurs."),
        ("Comment mes données sont-elles protégées ?", "Nous prenons la sécurité des données très au sérieux et utilisons des protocoles de sécurité avancés."),
        ("Puis-je annuler mon abonnement à tout moment ?", "Oui, vous pouvez annuler votre abonnement à tout moment sans frais supplémentaires."),
        ("Quels sont les avantages de l'utilisation de Bangri ?", "Nos solutions aident à augmenter les rendements, réduire les coûts et améliorer la durabilité des pratiques agricoles."),
        ("Comment puis-je créer un compte sur Bangri ?", "Pour créer un compte, cliquez sur 'S'inscrire' et remplissez le formulaire avec vos informations d'exploitation agricole."),
        # ("Quels sont les services gratuits disponibles sur Bangri ?", "La gestion des cultures, le suivi des rendements et les rapports de base sont gratuits."),
        ("Quels outils Bangri propose-t-il pour la gestion des exploitations agricoles ?", "Bangri offre des outils pour la planification des cultures, le suivi des intrants et des rendements, et bien plus encore."),
        ("Puis-je suivre mes cultures avec des capteurs IoT via Bangri ?", "Oui, Bangri s'intègre aux capteurs IoT pour surveiller la température, l'humidité, et d'autres paramètres en temps réel."),
        ("Comment puis-je accéder aux fonctionnalités premium ?", "Vous pouvez accéder aux fonctionnalités premium en souscrivant à un abonnement directement depuis votre tableau de bord."),
        ("Comment puis-je contacter le support Bangri ?", "Notre support est disponible via la page de contact, par email, ou via le chatbot intégré pour des réponses instantanées."),
        ("Quels types d'analyses avancées sont proposés dans l'offre premium ?", "Les analyses incluent des prévisions de rendement, des rapports sur les maladies, et l’optimisation de l’utilisation des ressources."),
        ("Bangri offre-t-il des services de gestion financière ?", "Oui, vous pouvez suivre vos dépenses, calculer les marges et générer des rapports financiers automatisés."),
        ("Puis-je utiliser Bangri pour gérer plusieurs exploitations agricoles ?", "Absolument, Bangri permet de gérer plusieurs exploitations avec des tableaux de bord distincts."),
        ("Comment puis-je planifier mes cultures pour la saison à venir ?", "Utilisez notre outil de planification des cultures pour entrer vos données et recevoir des recommandations."),
       ("Quels types de données sur les rendements des cultures puis-je analyser avec Bangri ?", 
         "Vous pouvez analyser les rendements par hectare, par culture, et sur plusieurs saisons pour mieux comprendre l'évolution de vos récoltes."),
        
        ("Comment Bangri m'aide-t-il à anticiper les rendements futurs ?", 
         "Bangri propose des prévisions basées sur des données historiques et des modèles météorologiques avancés."),
        
        ("Puis-je obtenir des recommandations pour améliorer mes rendements ?", 
         "Oui, Bangri fournit des recommandations personnalisées en fonction de vos données et des pratiques agricoles optimales."),
        
        ("Comment les prévisions météorologiques influencent-elles mes décisions agricoles ?", 
         "Vous recevrez des alertes en fonction des prévisions pour adapter vos pratiques (irrigation, semences, récoltes)."),
        
        ("Puis-je analyser les coûts de production de manière détaillée ?", 
         "Oui, Bangri permet de suivre chaque coût (main-d'œuvre, intrants, machines) et de calculer vos marges."),
        
        ("Comment puis-je optimiser l'utilisation des ressources agricoles ?", 
         "Bangri vous propose des solutions pour une gestion optimale de l'eau, des fertilisants et des pesticides."),
        
        ("Quelles données IoT puis-je intégrer dans Bangri ?", 
         "Vous pouvez intégrer des capteurs pour surveiller la température, l'humidité du sol et d'autres facteurs environnementaux."),
        
        ("Bangri propose-t-il des rapports sur les maladies des cultures ?", 
         "Oui, Bangri analyse vos données pour détecter les signes de maladies et vous propose des traitements adaptés."),
        
        ("Comment les analyses avancées m'aident-elles à réduire mes coûts ?", 
         "En optimisant les ressources et en améliorant les rendements grâce aux recommandations, vous réduisez vos dépenses."),
        
        ("Puis-je suivre les tendances de productivité sur plusieurs années ?", 
         "Oui, Bangri vous permet de visualiser l'évolution de vos rendements sur plusieurs saisons pour identifier des tendances."),

        # Questions sur les tableaux de bord personnalisés
        ("Quels types d'indicateurs clés puis-je voir dans le tableau de bord ?", 
         "Vous pouvez suivre les rendements, les coûts, les bénéfices, les prévisions météorologiques, et les alertes sur la santé des cultures."),
        
        ("Puis-je personnaliser les indicateurs selon mes besoins ?", 
         "Oui, vous pouvez sélectionner les indicateurs les plus pertinents pour votre exploitation et configurer le tableau de bord en conséquence."),
        
        ("Comment filtrer les données par parcelle ou type de culture ?", 
         "Bangri vous permet de filtrer les informations selon vos parcelles, vos cultures, ou vos besoins spécifiques."),
        
        ("Est-ce que Bangri propose un tableau de bord pour chaque exploitation agricole que je gère ?", 
         "Oui, si vous gérez plusieurs exploitations, Bangri fournit des tableaux de bord distincts pour chacune."),
        
        ("Puis-je exporter les données de mon tableau de bord ?", 
         "Oui, les données peuvent être exportées en différents formats (Excel, PDF) pour une analyse plus approfondie."),
        
        ("Comment puis-je obtenir des alertes personnalisées via le tableau de bord ?", 
         "Vous pouvez configurer des alertes sur les indicateurs clés tels que la météo, les rendements ou la santé des cultures."),
        
        ("Bangri me permet-il de visualiser des cartes pour mes parcelles ?", 
         "Oui, une vue cartographique est disponible pour visualiser l'emplacement de vos parcelles et les données associées."),
        
        ("Quels filtres avancés puis-je appliquer dans mon tableau de bord ?", 
         "Vous pouvez appliquer des filtres par culture, saison, parcelle, ou encore par type de coût."),
        
        ("Comment le tableau de bord m'aide-t-il à planifier mes actions futures ?", 
         "Grâce aux indicateurs et prévisions, vous pouvez prendre des décisions éclairées pour les semis, l'irrigation ou les récoltes."),
        
        ("Puis-je comparer mes performances avec d'autres exploitations agricoles ?", 
         "Oui, Bangri propose des analyses comparatives anonymisées avec d'autres exploitations pour évaluer votre position."),

        # Questions sur le support technique prioritaire
        ("Comment accéder au support technique prioritaire ?", 
         "Les utilisateurs premium peuvent accéder au support prioritaire via appels, chat en direct, ou par email."),
        
        ("Quelle est la disponibilité du support prioritaire ?", 
         "Le support prioritaire est disponible 24/7 pour répondre à toutes vos questions."),
        
        ("Puis-je utiliser un chatbot pour résoudre mes problèmes ?", 
         "Oui, Bangri propose un chatbot intelligent qui peut répondre aux questions fréquemment posées et vous orienter vers une solution."),
        
        ("Le support technique inclut-il des tutoriels ?", 
         "Oui, vous pouvez accéder à des vidéos et tutoriels détaillant l'utilisation des différentes fonctionnalités de Bangri."),
        
        ("Puis-je obtenir de l'aide en cas de problème technique avec mes capteurs IoT ?", 
         "Absolument, notre équipe peut vous assister dans la configuration et l'intégration de vos capteurs IoT."),
        
        ("Quel est le délai moyen de réponse pour le support technique prioritaire ?", 
         "Les réponses sont généralement fournies en moins de 30 minutes pour les utilisateurs premium."),
        
        ("Puis-je planifier des sessions de formation avec le support technique ?", 
         "Oui, des sessions de formation personnalisées peuvent être programmées pour optimiser l'utilisation de Bangri."),
        
        ("Comment le support technique m'aide-t-il à interpréter les analyses ?", 
         "Nos experts peuvent vous guider dans l'interprétation des rapports et analyses avancées fournies par Bangri."),
        
        ("Puis-je soumettre une demande de fonctionnalité personnalisée au support ?", 
         "Oui, les utilisateurs premium peuvent soumettre des demandes pour des fonctionnalités supplémentaires adaptées à leurs besoins."),
        
        ("Y a-t-il une documentation technique pour résoudre les problèmes courants ?", 
         "Oui, vous avez accès à une documentation complète pour résoudre vous-même les problèmes techniques."),

        # Questions sur la gestion financière et comptable
        ("Comment suivre mes dépenses agricoles avec Bangri ?", 
         "Vous pouvez entrer et suivre vos dépenses par catégorie (intrants, main-d'œuvre, matériel)."),
        
        ("Puis-je générer des rapports financiers automatisés ?", 
         "Oui, Bangri génère automatiquement des rapports financiers basés sur les données de votre exploitation."),
        
        ("Comment calculer mes marges avec Bangri ?", 
         "Les marges sont calculées en fonction des coûts de production et des rendements."),
        
        ("Puis-je suivre mes flux de trésorerie avec Bangri ?", 
         "Oui, vous pouvez suivre vos entrées et sorties de trésorerie pour mieux gérer vos finances."),
        
        ("Comment Bangri m'aide-t-il à gérer mes prêts agricoles ?", 
         "Vous pouvez suivre vos remboursements de prêts et voir leur impact sur vos finances."),
        
        ("Puis-je enregistrer des ventes et des revenus dans Bangri ?", 
         "Oui, en enregistrant vos ventes, Bangri calcule automatiquement vos bénéfices et marges."),
        
        ("Comment puis-je prévoir mes bénéfices pour les saisons futures ?", 
         "Bangri utilise vos données actuelles et passées pour estimer les bénéfices futurs."),
        
        ("Est-ce que Bangri peut m'aider à optimiser mes dépenses ?", 
         "Oui, vous recevrez des recommandations pour réduire vos coûts et maximiser vos profits."),
        
        ("Puis-je générer des factures à partir de Bangri ?", 
         "Oui, Bangri vous permet de générer et d'envoyer des factures pour vos ventes agricoles."),
        
        ("Comment suivre mes subventions agricoles avec Bangri ?", 
         "Vous pouvez suivre les subventions reçues et les associer à vos dépenses et investissements."),
        
        ("Puis-je gérer la paie de mes employés agricoles avec Bangri ?", 
         "Oui, Bangri offre un module pour la gestion de la paie, incluant le calcul des salaires et des heures travaillées."),
        
        ("Comment gérer mes dettes avec Bangri ?", 
         "Vous pouvez suivre vos dettes et leurs échéances pour mieux planifier vos paiements."),
        
        ("Puis-je comparer mes performances financières avec d'autres agriculteurs ?", 
         "Oui, Bangri vous permet de comparer anonymement vos résultats financiers avec d'autres exploitations."),
        
        ("Comment gérer mes investissements agricoles avec Bangri ?", 
         "Vous pouvez suivre vos investissements et analyser leur impact sur vos bénéfices."),
        
        ("Puis-je établir un budget annuel avec Bangri ?", 
         "Oui, Bangri vous permet de créer et suivre un budget basé sur vos prévisions de coûts et de revenus."),
        
        ("Comment suivre mes frais d'amortissement ?", 
         "Vous pouvez enregistrer l'amortissement de vos équipements et machines pour une gestion financière complète."),
        
        ("Bangri m'aide-t-il à gérer la fiscalité de mon exploitation ?", 
         "Oui, vous pouvez suivre vos obligations fiscales et générer des rapports nécessaires pour les déclarations."),
        
        ("Puis-je intégrer Bangri avec mon logiciel de comptabilité actuel ?", 
         "Oui, Bangri s'intègre avec certains logiciels comptables pour une synchronisation des données financières."),
        
        ("Comment suivre mes revenus par culture ?", 
         "Vous pouvez catégoriser vos revenus par type de culture pour analyser la rentabilité de chaque parcelle."),
        
    ]
    return render(request, 'siteweb/faq.html', {'faq_items': faq_items})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == 'POST':
        form = PostShareForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            to = form.cleaned_data['to']
            message = form.cleaned_data['message']

            # Envoyer l'e-mail
            send_mail(
                f"{name} recommande {post.title}",
                message,
                email,
                [to],
                fail_silently=False,
            )
            sent = True
            messages.success(request, "Votre message a été envoyé avec succès.")
        else:
            messages.error(request, "Erreur lors de l'envoi de l'e-mail. Veuillez vérifier le formulaire.")

    else:
        form = PostShareForm()

    return render(request, 'siteweb/share.html', {'post': post, 'form': form, 'send': sent, 'messages': messages.get_messages(request)})

def liste_ebooks(request):
    ebooks = Ebook.objects.all()
    return render(request, 'ebooks/liste_ebooks.html', {'ebooks': ebooks})

def detail_ebook(request, ebook_id):
    ebook = get_object_or_404(Ebook, id=ebook_id)
    return render(request, 'ebooks/detail_ebook.html', {'ebook': ebook})


def redirection_whatsapp(request, ebook_id):
    # Optionnel : récupérer les informations de l'ebook si besoin
    ebook = get_object_or_404(Ebook, id=ebook_id)
    return render(request, 'ebooks/redirect_whatsapp.html', {'ebook': ebook})
