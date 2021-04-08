from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
# from django.views.generic import ListView, TemplateView, DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.urls import reverse_lazy

from .models import Ad
# from .forms import AdForm


class AdListView(OwnerListView):
    model = Ad
    # fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')

class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')

class AdDetailView(OwnerDetailView):
    model = Ad
    fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')

class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')

class AdDeleteView(OwnerDeleteView):
    model = Ad
    # success_url = reverse_lazy('ads:ad_list')


class CommentCreateView(CreateView):
    model = Comment 
    success_url = reverse_lazy('ads:all')


class CommentDeleteView(CreateView):
    model = Comment 
    success_url = reverse_lazy('ads:all')