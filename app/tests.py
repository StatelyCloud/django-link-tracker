from django.test import TestCase, Client
from django.urls import reverse
from django.utils.text import slugify
from .models import Profile, Link, Analytics
import uuid


class ProfileModelTest(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            name="Test User",
            slug="test-user",
            bio="Test bio",
            profile_image="🌟"
        )
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.name, "Test User")
        self.assertEqual(self.profile.slug, "test-user")
        self.assertEqual(str(self.profile), "Test User")
        self.assertTrue(isinstance(self.profile.id, uuid.UUID))
    
    def test_profile_absolute_url(self):
        expected_url = reverse('profile_detail', kwargs={'slug': self.profile.slug})
        self.assertEqual(self.profile.get_absolute_url(), expected_url)


class LinkModelTest(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            name="Test User",
            slug="test-user"
        )
        self.link = Link.objects.create(
            profile=self.profile,
            title="Test Link",
            url="https://example.com",
            emoji="🔗",
            link_type="website"
        )
    
    def test_link_creation(self):
        self.assertEqual(self.link.title, "Test Link")
        self.assertEqual(self.link.url, "https://example.com")
        self.assertEqual(str(self.link), "🔗 Test Link")
        self.assertEqual(self.link.click_count, 0)
    
    def test_increment_clicks(self):
        initial_count = self.link.click_count
        self.link.increment_clicks()
        self.assertEqual(self.link.click_count, initial_count + 1)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.create(
            name="Test User",
            slug="test-user",
            bio="Test bio"
        )
        self.link = Link.objects.create(
            profile=self.profile,
            title="Test Link",
            url="https://example.com",
            emoji="🔗"
        )
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "LinkTracker")
    
    def test_profile_detail_view(self):
        response = self.client.get(reverse('profile_detail', kwargs={'slug': self.profile.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile.name)
        self.assertContains(response, self.link.title)
    
    def test_profile_edit_view(self):
        response = self.client.get(reverse('profile_edit', kwargs={'slug': self.profile.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Profile")
    
    def test_create_profile_view(self):
        response = self.client.get(reverse('create_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Your Profile")
    
    def test_link_redirect_view(self):
        response = self.client.get(reverse('link_redirect', kwargs={
            'slug': self.profile.slug,
            'link_id': self.link.id
        }))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.link.url)
        
        # Check that click count was incremented
        self.link.refresh_from_db()
        self.assertEqual(self.link.click_count, 1)
    
    def test_add_link_post(self):
        response = self.client.post(reverse('add_link', kwargs={'slug': self.profile.slug}), {
            'title': 'New Link',
            'url': 'https://newlink.com',
            'emoji': '✨',
            'link_type': 'website'
        })
        self.assertEqual(response.status_code, 302)
        
        # Check that link was created
        new_link = Link.objects.filter(title='New Link').first()
        self.assertIsNotNone(new_link)
        self.assertEqual(new_link.profile, self.profile)
    
    def test_profile_creation_post(self):
        response = self.client.post(reverse('create_profile'), {
            'name': 'New Profile'
        })
        self.assertEqual(response.status_code, 302)
        
        # Check that profile was created
        new_profile = Profile.objects.filter(name='New Profile').first()
        self.assertIsNotNone(new_profile)
        self.assertEqual(new_profile.slug, 'new-profile')


class AnalyticsModelTest(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            name="Test User",
            slug="test-user"
        )
        self.link = Link.objects.create(
            profile=self.profile,
            title="Test Link",
            url="https://example.com"
        )
    
    def test_analytics_creation(self):
        analytics = Analytics.objects.create(
            profile=self.profile,
            link=self.link,
            event_type='link_click',
            ip_address='127.0.0.1'
        )
        self.assertEqual(analytics.profile, self.profile)
        self.assertEqual(analytics.link, self.link)
        self.assertEqual(str(analytics), 'link_click - Test Link')
    
    def test_profile_view_analytics(self):
        analytics = Analytics.objects.create(
            profile=self.profile,
            event_type='profile_view'
        )
        self.assertEqual(str(analytics), 'profile_view - Test User')