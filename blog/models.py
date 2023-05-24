from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from phone_field import PhoneField


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name='Category title')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Post Title')
    content = models.TextField(verbose_name='Post Content')
    photo = models.ImageField(upload_to='photos/', verbose_name='Photography', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Changed date')
    publish = models.BooleanField(default=True, verbose_name='Post status')
    views = models.IntegerField(default=0, verbose_name='Number of views')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    author = models.CharField(max_length=30, verbose_name='Author')
    post = models.CharField(max_length=500)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return "https://thumbs.dreamstime.com/b/news-concept-globe-d-illustration-39286319.jpg"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Developer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40, verbose_name='Developer`s name')
    job = models.CharField(max_length=30, verbose_name='Job')
    bio = models.TextField(verbose_name='About me')
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    phone = PhoneField(blank=True, null=True, help_text='Contact phone number')
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Address')

    def get_photo(self):
        if self.photo:

            return self.photo.url
        else:
            return "https://wordpress-s3websitefiles-qe2pg7xcae3.s3.us-east-2.amazonaws.com/wordpress/wp-content/uploads/2019/11/26160520/Male.jpg"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Developer'


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Commentator')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             verbose_name='Comment')
    text = models.TextField(verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}- {self.post.title}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             verbose_name='Comment')
    like = models.BooleanField(default=False, verbose_name='Like')
    dislike = models.BooleanField(default=False, verbose_name='Dislike')

    def __str__(self):
        return f"{self.user.username}-" \
               f" {self.post.title}-" \
               f"{self.like}-" \
               f"{self.dislike}"

    class Meta:
        verbose_name = 'Like and Dislike'
        verbose_name_plural = 'Likes and Dislikes'
