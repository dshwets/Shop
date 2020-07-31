from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from webapp.models import Product
from webapp.forms import ProductForm


def index_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'index.html', context)


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete_product.html', context={'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index_view')


def create_product(request):
    if request.method == 'GET':
        return render(request, 'create_product.html', context={
            'form': ProductForm()
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                price=form.cleaned_data['price']
            )
            return redirect('watch_product', product.pk)
        else:
            return render(request,'create_product.html', context={
                'form': form
            })


def watch_product(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product
    }
    return render(request, 'view_product.html', context)


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'amount': product.amount,
            'price': product.price
            })
        return render(request, 'update_product.html', context={'form': form,
                                                               'product': product})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.amount = form.cleaned_data['amount']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect('watch_product', pk=todo_action.pk)
        else:
            return render(request, 'update_to_do_action.html', context={'form': form,
                                                                        'todo_action': todo_action})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])