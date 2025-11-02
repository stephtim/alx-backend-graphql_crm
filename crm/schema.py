import graphene
from graphene_django import DjangoObjectType
from crm.models import Product, Customer, Order  # Ensure this line exists and includes Product

# --- Example: Mutation definition ---

class UpdateLowStockProducts(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(graphene.String)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(f"{product.name} (new stock: {product.stock})")

        if updated_products:
            return UpdateLowStockProducts(
                success=True,
                message="Low-stock products updated successfully.",
                updated_products=updated_products
            )
        else:
            return UpdateLowStockProducts(
                success=False,
                message="No low-stock products found.",
                updated_products=[]
            )
