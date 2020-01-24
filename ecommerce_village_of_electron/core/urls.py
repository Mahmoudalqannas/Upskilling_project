from django.urls import path

from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    SearchView,
    product_category_list,
    ProductByCategory,
    thank_veiw

)
#    path('books/<publisher>/', PublisherBookList.as_view()),

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('thanks', thank_veiw, name='thanks'),
    path('search/', SearchView.as_view(), name='search'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('category-product/<category>/',
         ProductByCategory.as_view(), name='category'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
]
