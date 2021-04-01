from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from autos.models import Auto, Make
# from autos.forms import MakeForm

# Create your views here.
# class MainView(LoginRequiredMixin, View):
class MainView(View):
    def get(self, request):
        mc = Make.objects.all().count()
        al = Auto.objects.all()

        ctx = {'make_count': mc, 'auto_list': al}
        return render(request, 'autos/auto_list.html', ctx)


class MakeView(View):
# class MakeView(LoginRequiredMixin, View):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded

class MakeCreate(CreateView):
# class MakeCreate(LoginRequiredMixin, CreateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


# MakeUpdate has code to implement the get/post/validate/store flow
# AutoUpdate (below) is doing the same thing with no code
# and no form by extending UpdateView

class MakeUpdate(UpdateView):
# class MakeUpdate(LoginRequiredMixin, UpdateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class MakeDelete(DeleteView):
# class MakeDelete(LoginRequiredMixin, DeleteView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes

# class Autos(View):
class Autos( LoginRequiredMixin, ListView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos')
    # success_url = reverse_lazy('autos/auto_list')
# class Autos(LoginRequiredMixin, ListView):
#     def get(self, request):
#         mc = Make.objects.all().count()
#         al = Auto.objects.all()

#         ctx = {'make_count': mc, 'auto_list': al}
#         return render(request, 'autos/auto_list.html', ctx)

class AutoList(ListView):
# class AutoList(LoginRequiredMixin, ListView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autolist')

# class AutoCreate(CreateView):
class AutoCreate(LoginRequiredMixin, CreateView):
    # pass
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autocreate')

class AutoDetail(DetailView):
    model = Auto

class AutoUpdate(UpdateView):
# class AutoUpdate(LoginRequiredMixin, UpdateView):
    pass
    # model = Auto
    # fields = '__all__'
    # success_url = reverse_lazy('autos:all')

class AutoDelete(DeleteView):
# class AutoDelete(LoginRequiredMixin, DeleteView):
    pass
    # model = Auto
    # fields = '__all__'
    # success_url = reverse_lazy('autos:all')

# We use reverse_lazy rather than reverse in the class attributes
# because views.py is loaded by urls.py and in urls.py as_view() causes
# the constructor for the view class to run before urls.py has been
# completely loaded and urlpatterns has been processed.

# References
# https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview
