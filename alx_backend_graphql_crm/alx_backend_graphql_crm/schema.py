# alx_backend_graphql_crm/schema.py
import graphene

#  Define Query class
class Query(graphene.ObjectType):
    hello = graphene.String(description="Simple hello world field")

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

# Create schema object
schema = graphene.Schema(query=Query)
