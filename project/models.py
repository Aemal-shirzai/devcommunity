from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)
    desciption = models.TextField(max_length=3000, null=True, blank=True)
    demo_link = models.CharField(max_length=400, null=True, blank=True)
    source_link = models.CharField(max_length=400, null=True, blank=True)
    featured_image = models.ImageField(upload_to="projects", null=True, default='default.png')
    tags = models.ManyToManyField("Tag", related_name='projects')

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )

    project = models.ForeignKey(Project(), on_delete=models.CASCADE, related_name='reviews')
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    body = models.TextField(max_length=3000, blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

