from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, FormMixin, UpdateView, DeleteView
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login, logout as auth_logout, get_user_model
from django.contrib.auth.views import LoginView
from stockProject import settings
from .models import Product, Brand, User
from .forms import ProductForm, BrandForm

class AdminLogin(LoginView):
    template_name = 'login.html'
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

        return render(request, "index.html")


class AdminLogout(RedirectView):
    url = settings.LOGOUT_REDIRECT_URL
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(AdminLogout, self).get(request, *args, **kwargs)


class ResetPass(LoginView):
    template_name = 'reset-pass.html'


class Dashboard(TemplateView):
    template_name = 'index.html'
    context_object_name = 'Dashboard'


class Products(FormMixin, ListView):
    
    model = Product
    template_name = 'producttable.html'
    form_class = ProductForm
    initial = {'key': 'value'}
    success_url = '/products'

    def get(self, request):
        all_objects=Product.objects.all()
        form = self.form_class(initial=self.initial)
        for x in all_objects:
            if x.is_discount:
                x.price=x.discount
        context= {
            'object_list': all_objects,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'product_edit.html'
    fields= "__all__"
    success_url = '/products'


class ProductRemove(DeleteView):
    model = Product
    success_url = '/products'
    template_name = 'product_delete.html'


class Barchart(TemplateView):
    template_name = 'barchart.html'


# BRANDS
class Brands(FormMixin, ListView):
    
    model = Brand
    template_name = 'brands.html'
    form_class = BrandForm
    initial = {'key': 'value'}
    success_url = '/brands'

    def get(self, request):
        all_objects=Brand.objects.all()
        form = self.form_class(initial=self.initial)
        context= {
            'object_list': all_objects,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class BrandUpdate(UpdateView):
    model = Brand
    template_name = 'brand_edit.html'
    fields= "__all__"
    success_url = '/brands'


class BrandRemove(DeleteView):
    model = Brand
    template_name = 'brand_delete.html'
    success_url = '/brands'


# USERS
class UserListView(ListView):
    model = User
    template_name = "user_detail.html"


class UserUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'
    model = User
    template_name = 'user_edit.html'
    fields= "__all__"
    success_url = '/users'


class UserRemove(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_staff'
    model = User
    template_name = 'user_delete.html'
    success_url = '/users'