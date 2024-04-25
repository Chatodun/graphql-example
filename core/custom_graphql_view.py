from graphene_django.views import GraphQLView


class CustomGraphQLView(GraphQLView):
    def execute_graphql_request(
        self, request, data, query, variables, operation_name, show_graphiql=False
    ):
        result = super().execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql
        )
        if result.data:
            if "user" in result.data and request.user.has_perm("auth.view_user") is False:
                result.data["user"] = {'message': 'Cannot query field "user" on type "Query"'}
            elif 'type' in result.data and request.user.has_perm("auth.view_user") is False:
                if 'fields' in result.data['type']:
                    result.data['type']['fields'] = [d for d in result.data['type']['fields'] if d['name'] != 'user']
        return result
