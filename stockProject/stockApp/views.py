from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, FormMixin, UpdateView, DeleteView, CreateView
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login, logout as auth_logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView
from django.db.models import Sum, Count, F
from stockProject import settings
from .models import Product, Brand, User, Store, Category, LogEntry, Orders
from .forms import ProductForm, BrandForm, StoreForm, CategoryForm, OrderForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

# LOGIN
class AdminLogin(LoginView):
    template_name = 'login.html'
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

        return render(request, "index.html")


# LOGOUT
class AdminLogout(RedirectView):
    url = settings.LOGOUT_REDIRECT_URL
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(AdminLogout, self).get(request, *args, **kwargs)


#RESETPASS
class ResetPass(SuccessMessageMixin, PasswordResetView):
    template_name = 'reset-pass.html'
    html_email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    from_email='accounts@inspirationsoft.com'
    success_url = '/login'
    
    # mail = EmailMultiAlternatives(
    #     subject="Your Subject",
    #     body=email_template_name,
    #     from_email="Inspiration Soft <contact@inspirationsoft.com>",
    #     to=["serkankayser@windowslive.com"],
    #     headers={"Reply-To": "support@sendgrid.com"}
    #     )

#DASHBOARD
class Dashboard(ListView):
    template_name = 'index.html'
    context_object_name = 'Dashboard'
    def get(self, request):
        products_by_category=(Product.objects
            .values('category__name')
            .annotate(price_count=Sum(F('price') * F('quantity')), prod_count=Count('id'))
            .order_by()
        )

        products_by_brand=(Product.objects
            .values('brand__brand_name')
            .annotate(price_count=Sum(F('price') * F('quantity')), brand_count=Count('id'))
            .order_by()
        )
        
        context= {
            'products_by_category': products_by_category,
            'products_by_brand': products_by_brand,
        }

        return render(request, self.template_name, context)


#PRODUCTS
class Products(CreateView, ListView):
    
    model = Product
    template_name = 'producttable.html'
    form_class = ProductForm
    initial = {'key': 'value'}
    success_url = '/products'

    def get_context_data(self, **kwargs):
        # EXCLUDE PRODUCTS WITH QTY->0
        context = super().get_context_data(**kwargs)
        context['object_list'] = context.get('object_list').exclude(quantity=0)
        return context


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'product_edit.html'
    form_class = ProductForm
    success_url = '/products'

class ProductRemove(DeleteView):
    model = Product
    success_url = '/products'
    template_name = 'product_delete.html'


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


# CATEGORIES
class Categories(FormMixin, ListView):
    model = Category
    template_name = 'categories.html'
    form_class = CategoryForm
    initial = {'key': 'value'}
    success_url = '/categories'

    def get(self, request):
        all_objects=Category.objects.all()
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


class CategoryUpdate(UpdateView):
    model = Category
    template_name = 'category_edit.html'
    fields= "__all__"
    success_url = '/categories'


class CategoryRemove(DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = '/categories'


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


# STORES
class StoreListView(FormMixin, ListView):
    model = Store
    template_name = 'store_detail.html'
    form_class = StoreForm
    initial = {'key': 'value'}
    success_url = '/stores'

    def get(self, request):
        all_objects=Store.objects.all()
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


class StoreUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'
    model = Store
    template_name = 'store_edit.html'
    fields= "__all__"
    success_url = '/stores'


class StoreRemove(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_staff'
    model = Store
    template_name = 'store_delete.html'
    success_url = '/stores'


# STORES
class OrderListView(FormMixin, ListView):
    model = Orders
    template_name = 'order_detail.html'
    form_class = OrderForm
    initial = {'key': 'value'}
    success_url = '/orders'

    def get(self, request):
        all_objects=Orders.objects.all()
        # all_objects = Orders.objects.exclude(quantity=0)
        form = self.form_class(initial=self.initial)
        context= {
            'object_list': all_objects,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form_qty = int(form.data.get('quantity'))
            form_prod_id = form.data.get('product')
            prod = Product.objects.filter(id=form_prod_id)
            prod_qty = prod[0].quantity
            if prod_qty >= form_qty:
                remaining_qty = prod_qty - form_qty
                Product.objects.filter(id=form_prod_id).update(quantity=remaining_qty)
                
                form.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class OrderUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'
    model = Orders
    template_name = 'order_edit.html'
    fields= "__all__"
    success_url = '/orders'


class OrderRemove(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_staff'
    model = Orders
    template_name = 'order_delete.html'
    success_url = '/orders'


# LOGS
class AuditLogs(ListView):
    model = LogEntry
    template_name = 'audit_logs.html'

    def get(self, request):
        all_objects=LogEntry.objects.all()

        context= {
            'object_list': all_objects,
        }

        return render(request, self.template_name, context)


# MAPS
class Maps(TemplateView):
    template_name = 'maps.html'
    context_object_name = 'Maps'