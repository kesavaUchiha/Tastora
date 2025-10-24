from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from recipe_management.models import Recipe

class AddRecipeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('recipe_management:add_recipe')  # adjust to your URL name

    def test_add_recipe_success(self):
        # Create a simple image file
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x00\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x02\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B',
            content_type='image/jpeg'
        )

        data = {
            'title': 'Test Recipe',
            'category': '0',  # Veg
            'cuisine': 'Italian',
            'difficulty': '0',  # Easy
            'servings': 2,
            'prep_time': 10,
            'total_time': 20,
            'instructions': 'Mix ingredients and cook.',
            'featured': True,
            'calories': 300,
            'protein': 10,
            'fat': 5,
            'sugar': 8,
            'fiber': 4,
            'carbohydrates': 40,
            'ingredient_name[]': ['Tomato', 'Cheese'],
            'ingredient_quantity[]': ['100', '50'],
            'ingredient_unit[]': ['0', '0'],  # grams
            'ingredient_optional[]': ['True', 'False'],
        }

        response = self.client.post(self.url, data, follow=True, files={'image': image})

        # Check for success message
        self.assertContains(response, "🎉 Recipe created successfully!")

        # Check that the recipe was actually created
        self.assertTrue(Recipe.objects.filter(title='Test Recipe').exists())
