from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.urls import reverse_lazy, reverse
from .models import Ad, Comment
from ads.forms import CreateForm, CommentForm
from django.core.files.uploadedfile import InMemoryUploadedFile

class AdListView(OwnerListView):
    model = Ad
    # fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')


class AdCreateView(LoginRequiredMixin, CreateView):
    # model = Ad
    # fields = ['title', 'price', 'text']
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)

class AdDetailView(OwnerDetailView):
    model = Ad
    fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')
    template_name = "ads/ad_detail.html"

    def get(self, request, pk) :
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)
    

class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')

class AdDeleteView(OwnerDeleteView):
    model = Ad
    # success_url = reverse_lazy('ads:ad_list')

# class CommentListView(ListView):
#     model = Comment
#     post_comments = Comment.objects.all(filter_by )

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment 
    success_url = reverse_lazy('ads:all')
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))
   

class CommentDeleteView(OwnerDeleteView):
    model = Comment 
    success_url = reverse_lazy('ads:all')
 
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])
     # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response