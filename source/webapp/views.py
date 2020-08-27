from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from webapp.models import Product
from webapp.forms import ProductForm,SimpleSeachForm
from webapp.contextprocessors import search_form


class SearchView(ListView):
    search_form_class = SimpleSeachForm
    search_form_field = 'search'
    search_fields = []

    def get(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value(self.search_form)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = self.search_form
        context['search_value'] = self.search_value
        return context

    def get_queryset(self):
        data = super().get_queryset()
        query = self.get_query(self.search_value)
        data = data.filter(query)
        data = data.filter(amount__gt=0)
        return data

    def get_search_form(self):
        return self.search_form_class(data=self.request.GET)

    def get_search_value(self, form):
        search_value = None
        if form.is_valid():
            search_value = form.cleaned_data.get(self.search_form_field, None)
        return search_value

    def get_query(self, search_value):
        query = Q()
        if search_value:
            for field in self.search_fields:
                kwargs = {field: search_value}
                query = query | Q(**kwargs)

        return query


class IndexView(SearchView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 1
    search_fields = ['name__icontains', 'description__icontains']
    ordering = ['category', 'name']


class CreateProduct(CreateView):
    model = Product
    template_name = 'product_create.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('watch_product', kwargs={'pk': self.object.pk})


class DeleteProductView(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('index')


class WatchProductView(DetailView):
    model = Product
    template_name = 'product_view.html'


class UpdateProductView(UpdateView):
    model = Product
    template_name = 'product_update.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('watch_product', kwargs={'pk':self.object.pk})
