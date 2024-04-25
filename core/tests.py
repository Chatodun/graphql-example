import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import Client

from graphene_django.utils.testing import GraphQLTestCase

User = get_user_model()


class GraphQLFieldVisibilityTestCase(GraphQLTestCase):
    def _create_user(self, username: str, password: str, email: str):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        if 'admin' in username:
            group = Group.objects.get(name='admin')
            group.user_set.add(user)
        return user

    def setUp(self):
        content_type = ContentType.objects.get(app_label='auth', model='user')
        admin_group, _ = Group.objects.get_or_create(name='admin')
        permission, _ = Permission.objects.get_or_create(
            codename='view_user',
            content_type=content_type
        )
        admin_group.permissions.add(permission)

        self.test_user = User.objects.create(pk=1000, username='test_user', email='test_email')
        self.admin = self._create_user('admin', 'admin', 'test@mail.com')
        self.user = self._create_user('user', 'user', 'user@mail.com')
        self.client = Client()
        self.user_query = '''
            query UserQuery {
                user(id: 1000) {
                    username
                    email
                }
            }
        '''
        self.introspection_query = '''
        query QueryIntrospection {
            type: __type(name: "Query") {
                fields {
                    name
                    description
                }
            }
        }
        '''

    def test_user_field_visibility_with_authorize_user(self):
        self.client.force_login(self.admin)
        response = self.query(
            self.user_query,
            operation_name='UserQuery',
            headers={'COOKIE': f'sessionid={self.client.session.session_key}'}
        )

        content = json.loads(response.content)

        self.assertEqual(
            content['data']['user'],
            {
                'username': self.test_user.username,
                'email': self.test_user.email
            }
        )

    def test_type_field_visibility_with_user_without_permission(self):
        self.client.force_login(self.user)
        response = self.query(
            self.user_query,
            operation_name='UserQuery',
            headers={'COOKIE': f'sessionid={self.client.session.session_key}'}
        )

        content = json.loads(response.content)

        self.assertEqual(
            content['data']['user'],
            {'message': 'Cannot query field "user" on type "Query"'}
        )

    def test_type_field_visibility_with_anonymous_user(self):
        response = self.query(
            self.user_query,
            operation_name='UserQuery',
        )

        content = json.loads(response.content)

        self.assertEqual(
            content['data']['user'],
            {'message': 'Cannot query field "user" on type "Query"'}
        )

    def test_schema_introspection_for_admin(self):
        self.client.force_login(self.admin)
        response = self.query(
            self.introspection_query,
            operation_name='QueryIntrospection',
            headers={'COOKIE': f'sessionid={self.client.session.session_key}'}
        )

        content = json.loads(response.content)

        self.assertEqual(
            content['data']['type']['fields'],
            [
                {
                    'name': 'user',
                    'description': 'Gets single User by ID'
                },
                {
                    'name': 'expenses',
                    'description': None
                }
            ]
        )

    def test_schema_introspection_for_user_without_permission(self):
        self.client.force_login(self.user)
        response = self.query(
            self.introspection_query,
            operation_name='QueryIntrospection',
            headers={'COOKIE': f'sessionid={self.client.session.session_key}'}
        )

        content = json.loads(response.content)

        self.assertEqual(
            content['data']['type']['fields'],
            [
                {
                    'name': 'expenses',
                    'description': None
                }
            ]
        )

    def test_schema_introspection_for_anonymous_user(self):
        response = self.query(
            self.introspection_query,
            operation_name='QueryIntrospection',
            headers={'COOKIE': f'sessionid={self.client.session.session_key}'}
        )

        content = json.loads(response.content)

        self.assertEqual(
            content['data']['type']['fields'],
            [
                {
                    'name': 'expenses',
                    'description': None
                }
            ]
        )