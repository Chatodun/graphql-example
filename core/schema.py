from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

from core import models

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


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

    def resolve_user(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def resolve_expenses(self, info):
        return models.Expense.objects.all()


schema = graphene.Schema(query=Query)
