from django.contrib import admin
from .models import Customer, Product, Investment

# Custom admin for Product to avoid foreign key issues
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
# Custom admin for Investment with proper foreign key handling
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'investment_amount')
    list_filter = ('product',)

# Register models for admin interface
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Investment, InvestmentAdmin)
