import graphene
from crm.schema import Mutation
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

schema = graphene.Schema(query=Query, mutation=Mutation)

# Combine queries from crm
class Query(CRMQuery, graphene.ObjectType):
    pass

# Combine mutations from crm
class Mutation(CRMMutation, graphene.ObjectType):
    pass

# Create main schema
schema = graphene.Schema(query=Query, mutation=Mutation)