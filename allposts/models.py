from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# Create your models here.

class Address(models.Model):
    city=models.CharField(max_length=50)
    pincode=models.IntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)])

    def __str__(self):
        return f"{self.city} {self.pincode}"

class Author(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    address=models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date=models.DateField()
    image=models.ImageField(upload_to="image")
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    slug=models.SlugField()

    def __str__(self):
        return f"{self.title} {self.author}"
    
    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])
    
class Comment(models.Model):
    user_name=models.CharField(max_length=20)
    email=models.EmailField()
    content=models.TextField(null=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_name}"
