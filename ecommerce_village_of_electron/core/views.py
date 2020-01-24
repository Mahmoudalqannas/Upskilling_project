from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.utils import timezone
from django.db.models import Q
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, UserProfile, CategoryProduct, CheckoutModel


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(CreateView):

    model = CheckoutModel
    template_name = 'checkout.html'
    success_url = reverse_lazy('core:thanks')
    fields = ('address', 'city', 'phone_number')

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        order = Order.objects.get(user=self.request.user, ordered=False)
        context['order'] = order
        return context


# class CheckoutView(View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.filter(user=self.request.user, ordered=False)
#             form = CheckoutForm()
#             context = {
#                 'order': order,
#                 'form': form
#             }
#             return render(self.request, "checkout.html", context)

#         except ObjectDoesNotExist:
#             messages.info(self.request, "You do not have an active order")
#             return redirect("core:checkout")

#     def post(self, *args, **kwargs):
#         form = CheckoutForm(self.request.POST or None)
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             if form.is_valid():
#                 order.update(ordered=True)
#                 order.save()
#                 return redirect('core:thanks')

#         except ObjectDoesNotExist:
#             messages.info(self.request, "You do not have an active order")
#             return redirect("core:home")


class HomeView(ListView):
    model = Item
    paginate_by = 12
    template_name = "home.html"


class SearchView(ListView):
    model = Item
    template_name = "search.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(title__contains=query)

        return object_list


class ProductByCategory(ListView):

    context_object_name = 'category_list'
    template_name = "category.html"

    def get_queryset(self):
        self.category = get_object_or_404(
            CategoryProduct, category_product=self.kwargs['category'])
        return Item.objects.filter(category=self.category)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def product_category_list(request, pk):
    context = {}
    product_category = CategoryProduct.objects.get(pk=pk)
    context["products"] = Item.objects.filter(category=product_category)
    return render(request, "category.html", context=context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def thank_veiw(request):
    return render(request, "thank_you.html")
