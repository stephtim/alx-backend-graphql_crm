import graphene
from crm.schema import Mutation

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

schema = graphene.Schema(query=Query, mutation=Mutation)
