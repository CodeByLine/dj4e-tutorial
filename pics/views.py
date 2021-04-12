from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from pics.models import Pic
from .forms import PicCreateForm


class PicListView(OwnerListView):
    model = Pic
    template_name = "pics/pic_list.html"


class PicDetailView(OwnerDetailView):
    model = Pic
    template_name = "pics/pic_detail.html"


class PicCreateView(LoginRequiredMixin, View):
    template_name = 'pics/pic_form.html'
    success_url = reverse_lazy('pics:all')

    def get(self, request, pk=None):
        form = PicCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = PicCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)


class PicUpdateView(LoginRequiredMixin, View):
    template_name = 'pics/pic_form.html'
    success_url = reverse_lazy('pics:all')

    def get(self, request, pk):
        pic = get_object_or_404(Pic, id=pk, owner=self.request.user)
        form = PicCreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Pic, id=pk, owner=self.request.user)
        form = PicCreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)


class PicDeleteView(OwnerDeleteView):
    model = Pic
    template_name = "pics/pic_confirm_delete.html"


def stream_file(request, pk):
    pic = get_object_or_404(Pic, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response
