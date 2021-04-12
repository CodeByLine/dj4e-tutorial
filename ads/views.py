from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.urls import reverse_lazy
from .models import Ad, Comment
from pics.models import Pic
# from .forms import AdForm
from .forms import AdCreateForm


class AdListView(OwnerListView):
    model = Ad
    # fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_create.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = AdCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = AdCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)

# class AdCreateView(OwnerCreateView):
#     model = Ad
#     fields = ['title', 'price', 'text']
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