from user.models import Profile
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile, related_name='projects', on_delete=models.SET_NULL, null=True, blank=True)
    desciption = models.TextField(max_length=3000, null=True, blank=True)
    demo_link = models.CharField(max_length=400, null=True, blank=True)
    source_link = models.CharField(max_length=400, null=True, blank=True)
    featured_image = models.ImageField(upload_to="projects", null=True, default='default.png')
    tags = models.ManyToManyField("Tag", related_name='projects')

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

        
    @property
    def up_votes(self):
        return self.reviews.filter(value='up')

    @property
    def down_votes(self):
        return self.reviews.filter(value='down')
    
    @property
    def vote_ratio(self):
        return 0 if not self.reviews.count() else (self.up_votes.count() / self.reviews.count()) * 100

    @property
    def reviewers(self):
        return self.reviews.all().values_list('owner__id', flat=True)


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )

    owner = models.ForeignKey(Profile, related_name='reviews', on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    body = models.TextField(max_length=3000, blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return f"({self.project.title}): {self.owner.full_name}-{self.value}"


class Tag(models.Model):
    name = models.CharField(max_length=200)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

