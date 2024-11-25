from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(statut='published')

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="category_posts")
    STATUT_CHOICES =(
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    statut = models.CharField(choices=STATUT_CHOICES,
                               default='draft', max_length=10)
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posted',  )
    image =models.ImageField(upload_to='post_images/', blank=True, null=True)
    objects = models.Manager() #default manager
    published_posts = PublishedManager() #custom manager
    tags = TaggableManager()

    def __str__(self):
        return self.body
    
    def get_absolute_url(self):
        return reverse("blog_details_view", args=[self.published.year, self.published.month, self.published.day, self.slug ] )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    def is_reply(self):
        return self.parent is not None


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject



class Ebook(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    fichier = models.FileField(upload_to='ebooks/')
    couverture = models.ImageField(upload_to='couvertures/', blank=True, null=True)
    date_publication = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titre
