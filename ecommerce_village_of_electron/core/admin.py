from django.contrib import admin

# from .models import Item, OrderItem, Order, Payment, Coupon, Refund, UserProfile
from .models import Item, OrderItem, Order, UserProfile, CategoryProduct, ProductTags, Tag


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(UserProfile)
admin.site.register(CategoryProduct)
admin.site.register(ProductTags)
admin.site.register(Tag)
