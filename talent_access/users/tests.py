from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(TestCase):
    def test_diplome_signup(self):
        response = self.client.post(
            reverse('diplome_signup'),
            {
                'email': 'dip@example.com',
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'password1': 'Passw0rd!123',
                'password2': 'Passw0rd!123',
            },
            follow=True,
        )
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.statut, User.Statut.DIPLOME)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('diplome_dashboard'))

    def test_pme_signup(self):
        response = self.client.post(
            reverse('pme_signup'),
            {
                'email': 'pme@example.com',
                'company_name': 'MyComp',
                'sector': 'Tech',
                'password1': 'Passw0rd!123',
                'password2': 'Passw0rd!123',
            },
            follow=True,
        )
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.statut, User.Statut.PME)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('pme_dashboard'))

    def test_diplome_login(self):
        user = User.objects.create_user(
            username='dip@example.com',
            email='dip@example.com',
            password='Passw0rd!123',
            statut=User.Statut.DIPLOME,
        )
        response = self.client.post(
            reverse('diplome_login'),
            {'username': 'dip@example.com', 'password': 'Passw0rd!123'},
            follow=True,
        )
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('diplome_dashboard'))

    def test_pme_login(self):
        user = User.objects.create_user(
            username='pme@example.com',
            email='pme@example.com',
            password='Passw0rd!123',
            statut=User.Statut.PME,
        )
        response = self.client.post(
            reverse('pme_login'),
            {'username': 'pme@example.com', 'password': 'Passw0rd!123'},
            follow=True,
        )
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('pme_dashboard'))

    def test_wrong_password(self):
        User.objects.create_user(
            username='dip@example.com',
            email='dip@example.com',
            password='Passw0rd!123',
            statut=User.Statut.DIPLOME,
        )
        response = self.client.post(
            reverse('diplome_login'),
            {'username': 'dip@example.com', 'password': 'badpass'},
            follow=True,
        )
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertFalse(response.context['form'].is_valid())

    def test_email_already_taken(self):
        User.objects.create_user(
            username='dup@example.com',
            email='dup@example.com',
            password='Passw0rd!123',
            statut=User.Statut.DIPLOME,
        )
        response = self.client.post(
            reverse('diplome_signup'),
            {
                'email': 'dup@example.com',
                'first_name': 'Jean',
                'last_name': 'Dup',
                'password1': 'Passw0rd!123',
                'password2': 'Passw0rd!123',
            },
        )
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(User.objects.count(), 1)

