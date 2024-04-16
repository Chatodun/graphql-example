from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

from core import models

User = get_user_model()


class AuthorizationError(Exception):
    """Authorization failed."""


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


def check_permission(permission_name: str):
    def check_permission_decorator(func):
        def wrapper(self, info, *args, **kwargs):
            if not info.context.user.has_perm(permission_name):
                raise AuthorizationError(
                    'Cannot query field "user" on type "Query" error for the same query and is not able to execute it'
                )
            return func(self, info, *args, **kwargs)
        return wrapper
    return check_permission_decorator


class Expense(DjangoObjectType):
    class Meta:
        model = models.Expense


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        id=graphene.Int(required=True),
        description='Gets single User by ID'
    )
    expenses = graphene.List(Expense)

    @check_permission(permission_name='auth.view_user')
    def resolve_user(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def resolve_expenses(self, info):
        return models.Expense.objects.all()


schema = graphene.Schema(query=Query)
