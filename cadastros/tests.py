from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from autenticacao.models import CustomUser
from django.contrib.auth import get_user_model



class ViewTests(TestCase):
    def setUp(self):
        # Setup a client and common data
        self.client = Client()
        
        # Create a user with permissions
        self.admin_group = Group.objects.create(name="Admnistrador")
        self.admin_user = CustomUser.objects.create_user(
            username="testecliente", password="adminpass", email="admin@test.com"
        )
        self.admin_user.groups.add(self.admin_group)

        # Create a regular user
        self.regular_user = CustomUser.objects.create_user(
            username="user", password="userpass", email="user@test.com"
        )

    def login_as_admin(self):
        self.client.login(username="admin", password="adminpass")

    def login_as_user(self):
        self.client.login(username="user", password="userpass")

    # Test RegisterView
    def test_register_view_access(self):
        self.login_as_admin()
        response = self.client.get(reverse('register'))  # Assumes 'register' is the URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros/index.html')

    # Test UpdateUserView
    def test_update_user_view(self):
        self.login_as_admin()
        response = self.client.get(reverse('update_user', kwargs={'pk': self.admin_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista/editar-usuario.html')

    # Test DeleteUserView
    def test_delete_user_view(self):
        self.login_as_admin()
        response = self.client.get(reverse('delete_user', kwargs={'pk': self.regular_user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista/excluir-usuario.html')
        post_response = self.client.post(reverse('delete_user', kwargs={'pk': self.regular_user.pk}))
        self.assertRedirects(post_response, reverse('user_list'))
        self.assertFalse(CustomUser.objects.filter(pk=self.regular_user.pk).exists())

    # Test UserListView
    def test_user_list_view(self):
        self.login_as_admin()
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista/usuarios.html')
        self.assertIn(self.admin_user, response.context['users'])

    # Test GroupCreateView
    def test_group_create_view(self):
        self.login_as_admin()
        response = self.client.get(reverse('create_group'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupos/criar_grupos.html')
        post_response = self.client.post(reverse('create_group'), {'name': 'NewGroup'})
        self.assertRedirects(post_response, reverse('group_list'))
        self.assertTrue(Group.objects.filter(name='NewGroup').exists())

    # Test GroupUpdateView
    def test_group_update_view(self):
        self.login_as_admin()
        response = self.client.get(reverse('update_group', kwargs={'pk': self.admin_group.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupos/editar_grupos.html')

    # Test GroupDeleteView
    def test_group_delete_view(self):
        self.login_as_admin()
        response = self.client.get(reverse('delete_group', kwargs={'pk': self.admin_group.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupos/excluir_grupos.html')
        post_response = self.client.post(reverse('delete_group', kwargs={'pk': self.admin_group.pk}))
        self.assertRedirects(post_response, reverse('group_list'))
        self.assertFalse(Group.objects.filter(pk=self.admin_group.pk).exists())

    # Test GroupListView
    def test_group_list_view(self):
        self.login_as_admin()
        response = self.client.get(reverse('group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupos/listar_grupos.html')
        self.assertIn(self.admin_group, response.context['groups'])

    # Test unauthorized access
    def test_unauthorized_access(self):
        self.login_as_user()
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 403)  # Forbidden for non-admin users
