from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from cats.models import Cat, Breed
# from cats.forms import MakeForm

class CatList(LoginRequiredMixin, ListView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cat_list')

    def get(self, request):
        cc = Cat.objects.all().count()
        cl = Cat.objects.all()

        ctx = {'cat_count': cc, 'cat_list': cl}
        return render(request, 'cats/cat_list.html', ctx)

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cat_list')


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cat_list')


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:cat_list')



##
class BreedList(LoginRequiredMixin, ListView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_list')

    def get(self, request):
        bc = Breed.objects.all().count()
        bl = Breed.objects.all()

        ctx = {'breed_count': bc, 'breed_list': bl}
        return render(request, 'cats/breed_list.html', ctx)

class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_list')


class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_list')


class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:breed_list')