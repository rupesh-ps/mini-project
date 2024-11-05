from django.test import TestCase
from django.urls import reverse
from ..models import Category, Ad, User, Profile

class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.profile = Profile.objects.create(user=cls.user, phone="1234567890", email="testuser@example.com")
        cls.category1 = Category.objects.create(name='Category 1')
        cls.category2 = Category.objects.create(name='Category 2')
        cls.ad1 = Ad.objects.create(title='Ad 1', description='Description 1', category=cls.category1, postal_code=123456, user=cls.profile)
        cls.ad2 = Ad.objects.create(title='Ad 2', description='Description 2', category=cls.category1, postal_code=123456, user=cls.profile)

class HomePageViewTest(BaseTestCase):
    def test_homepage_status_code(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_template_used(self):
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'base.html')

class CategoryListViewTest(BaseTestCase):
    def test_category_list_view(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/category_list.html')
        self.assertQuerySetEqual(response.context['categories'], [self.category1, self.category2], ordered=False)

    def test_category_list_empty(self):
        Category.objects.all().delete()
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No categories available at the moment.")

    def test_category_list_pagination(self):
        for i in range(15):
            Category.objects.create(name=f'Category {i}')
        response = self.client.get(reverse('category-list'))
        self.assertContains(response, 'Next')

    def test_non_existent_category_detail(self):
        response = self.client.get(reverse('category-detail', args=[999]))
        self.assertEqual(response.status_code, 404)

class CategoryDetailViewTest(BaseTestCase):
    def test_category_detail_view(self):
        response = self.client.get(reverse('category-detail', args=[self.category1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/category_detail.html')
        self.assertEqual(response.context['category'], self.category1)
        self.assertQuerySetEqual(response.context['ads'], [self.ad1, self.ad2], ordered=False)

    def test_empty_ads_in_category(self):
        Category.objects.create(name='Empty Category')
        response = self.client.get(reverse('category-detail', args=[self.category2.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No ads available in this category.")

class AdListViewTest(BaseTestCase):
    def test_ad_list_view(self):
        response = self.client.get(reverse('ad-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ad_list.html')
        self.assertQuerySetEqual(response.context['ads'], [self.ad1, self.ad2], ordered=False)

    def test_ad_list_empty(self):
        Ad.objects.all().delete()
        response = self.client.get(reverse('ad-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No ads available.")

    def test_ad_list_search_no_results(self):
        searchTerm = 'Non-existent Ad'
        response = self.client.get(reverse('ad-list'), {'search': searchTerm})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"No ads found for your search: '{searchTerm}'.")

    def test_ad_list_pagination_with_fewer_items(self):
        Ad.objects.all().delete()
        for i in range(5):
            Ad.objects.create(title=f'Ad {i}', description='Description', category=self.category1, postal_code=123456, user=self.profile)
        response = self.client.get(reverse('ad-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Next', 0)

class AdDetailViewTest(BaseTestCase):
    def test_ad_detail_view(self):
        response = self.client.get(reverse('ad-detail', args=[self.ad1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ad_detail.html')
        self.assertEqual(response.context['ad'], self.ad1)

    def test_non_existent_ad_detail(self):
        response = self.client.get(reverse('ad-detail', args=[999]))
        self.assertEqual(response.status_code, 404)


class FeaturedViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.ad3 = Ad.objects.create(title='Ad 3', description='Description 3', category=self.category1, postal_code=123456, user=self.profile, view=5)
        self.ad4 = Ad.objects.create(title='Ad 4', description='Description 4', category=self.category1, postal_code=123456, user=self.profile, view=2)
        self.ad5 = Ad.objects.create(title='Ad 5', description='Description 5', category=self.category1, postal_code=123456, user=self.profile, view=10)

    def test_featured_ads_view(self):
        response = self.client.get(reverse('featured-ads'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/featured_ads.html')
        
        self.assertQuerySetEqual(
            response.context['featured_ads'],
            [self.ad3, self.ad5], 
            ordered=False
        )

    def test_featured_ads_empty(self):
        Ad.objects.all().delete()
        response = self.client.get(reverse('featured-ads'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No featured ads available at the moment.")
