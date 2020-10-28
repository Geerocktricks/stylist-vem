from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import django.utils.timezone as now
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save


# Custom Manager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

# Kategory

class Kategory(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    post_ids = ArrayField( models.IntegerField( default=0 ), default=list )
    created_at = models.DateTimeField(default=now.now, editable=False)
    updated_at = models.DateTimeField(default=now.now)

    class Meta:
        ordering = ('name', )
        verbose_name = 'kategory'
        verbose_name_plural = 'kategories'

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now() # new posts creation date
        self.updated_at = timezone.now() # old posts update date
        return super( Kategory, self ).save( *args, **kwargs )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_list_by_kategory', args=[self.slug])


# Our Post Model

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE,)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    article_image = models.ImageField(upload_to = 'articles/')
    kategory = models.ForeignKey(Kategory, related_name='blog_posts', on_delete=models.CASCADE)

    # The default manager
    objects = models.Manager()

    # Custom made manager
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        index_together = (('id', 'slug'),)

    @classmethod
    def search_by_title(cls,search_term):
        post = cls.objects.filter(title__icontains=search_term)
        return post

    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return reverse('post_detail_view', args=[self.publish.year, self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])

# \\\\\\\\\\\\\\\\\\\\\\\\\Comment////////////////////////////

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)





# ////////////////////////// SHOP ___++==--++__==--__++__+=--

class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

class InstaRecap(models.Model):
    title = models.CharField(max_length=250)
    instaPic = models.ImageField(upload_to='instapics/')
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title



# create a signal to listen for each time you save a post and update the post_id field in Kategory model
def update_post_id_field_in_kategory_model(sender, instance, **kwargs):
    if not instance.id in instance.kategory.post_ids: # to avoid duplicate post ids in kategory.post_id field
        instance.kategory.post_ids.append(instance.id) # add the post id to the kategory.post_id field
        instance.kategory.save() # save the kategory


# connect that signal
post_save.connect( update_post_id_field_in_kategory_model, sender=Post )


