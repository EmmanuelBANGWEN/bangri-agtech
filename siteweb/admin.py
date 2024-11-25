from django.contrib import admin
from .models import Post, Newsletter , Category, Comment, Subscriber, Ebook
from .views import send_newsletter

# Gestion du modèle Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'statut', 'created', 'published', 'update', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')
    ordering = ('author', 'statut', 'published')
    list_filter = ('author', 'created', 'published', 'update')

# Gestion du modèle Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created', 'parent')
    list_filter = ('post', 'author')

# Gestion du modèle Category
admin.site.register(Category)

# Action d'administration pour envoyer la newsletter
@admin.action(description='Envoyer une newsletter')
def send_newsletter_action(modeladmin, request, queryset):
    for newsletter in queryset:
        send_newsletter(newsletter.subject, newsletter.message)

# Gestion des newsletters (assurez-vous d'avoir un modèle Newsletter défini)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'created_at']
    actions = [send_newsletter_action]

# Si vous avez un modèle "Newsletter", vous devez l'enregistrer ici
admin.site.register(Newsletter, NewsletterAdmin)

# Si vous avez un modèle "Newsletter", vous devez l'enregistrer ici
# admin.site.register(Subscriber)




admin.site.register(Ebook)
