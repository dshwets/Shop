from django.db import models
from django.db.models import Q, ExpressionWrapper, F, Sum
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, View
from django.core.exceptions import ObjectDoesNotExist

from webapp.models import Product, Cart, Orders, ProductOrder
from webapp.forms import ProductForm, SimpleSeachForm, CartForm, InformationForm


class WatchCart(ListView):

    model = Cart
    template_name = 'Cart/cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(total=ExpressionWrapper(F('qty')*F('good__price'), output_field=models.DecimalField(max_digits=7, decimal_places=2)))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['total_summ'] = context['cart'].aggregate(tota=Sum('total'))
        context['form'] = InformationForm
        return context


class AddProductToCart(View):
    def post(self, request, *args, **kwargs):
        form = CartForm(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        try:
            new_product = Cart.objects.get(good=product)
            if product.amount >= (form.cleaned_data['qty'] + new_product.qty):
                new_product.qty += form.cleaned_data['qty']
                new_product.save()
        except ObjectDoesNotExist:
            if product.amount >= form.cleaned_data['qty']:
                Cart.objects.create(good=product, qty=form.cleaned_data['qty'])
        return redirect('index')

    def form_invalid(self, form):
        context = {'form': form}
        return render(self.request, 'Products/index.html', context)


class DeleteCart(DeleteView):
    model = Cart
    success_url='Products/index.html'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('index')


class CreateOrder(CreateView):
    model = Orders
    form_class = InformationForm

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        super().form_valid(form)               ## Это нужно для того, что бы получить pk Ордера
        for product in Cart.objects.all():      ##Возможно наговнокодил, но вроде пашет норм )
            ProductOrder.objects.create(order=self.object, qty=product.qty, product=product)
            edited_product = Product.objects.get(pk=product.good.pk)
            edited_product.amount -= product.qty
            edited_product.save()
            product.delete()
        return super().form_valid(form)