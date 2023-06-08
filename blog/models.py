from django.db import models
from django.utils import timezone
# import for creating M-1 relationship
from django.contrib.auth.models import User
from django.urls import reverse

# Model manager for getting published post
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    # blogs require statuses(published/draft)
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    # Link a user with a post - many to one relationship
    author = models.ForeignKey(User,on_delete = models.CASCADE,
                                related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                choices = Status.choices,
                                default= Status.DRAFT)

    
    objects = models.Manager() #the default manager
    published = PublishedManager() #custom manager
    # ordering the post from newest to oldest
    class Meta:
        ordering = ['-publish']
        # adding index to improve on search performances
        indexes = [
            models.Index(fields=['-publish']),
        ]



    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
