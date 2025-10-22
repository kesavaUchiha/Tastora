from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/',blank=True,null=True)
    bio = models.CharField(max_length=1000,blank=True)
    location = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'
    
class Recipe(models.Model):

    CATEGORIES_CHOICES=[
        ('veg','Veg'),
        ('vegan','Vegan'),
        ('non-veg','Non-Veg')
    ]

    DIFFICULTY=[
        ('easy','Easy'),
        ('medium','Medium'),
        ('hard','Hard')
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='recipes')
    category = models.CharField(max_length=10,choices=CATEGORIES_CHOICES,default='veg')
    cuisine =  models.CharField(max_length=50)
    difficulty = models.CharField(max_length=10,choices=DIFFICULTY,default='easy')
    servings = models.IntegerField(default=1,help_text="Number of people the recipe serves")
    prep_time = models.IntegerField(help_text="Time required to prepare ingredients")
    total_time = models.IntegerField(help_text="Preparation time + Cooking Time")
    calories = models.IntegerField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_img')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at","title")
        unique_together = ('title', 'author')

    def __str__(self):
        return f'{self.title}'

class Ingredient(models.Model):

    UNIT_CHOICES = [
        ('g', 'grams'),
        ('kg', 'kilograms'),
        ('tsp', 'teaspoon'),
        ('tbsp', 'tablespoon'),
        ('cup', 'cup'),
        ('pcs', 'pieces'),
    ]
    recipe=models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='ingredients')
    name=models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10,choices=UNIT_CHOICES)
    optional = models.BooleanField(default=True)

class Collection(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at','title')
        unique_together = ('title', 'owner')

    def __str__(self):
        return f'{self.title}'