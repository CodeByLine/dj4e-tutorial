from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.urls import reverse_lazy, reverse
from .models import Ad, Comment, Fav
from ads.forms import AdCreateForm, CommentForm
from pics.models import Pic
from pics.views import PicCreateView, PicDetailView, PicDeleteView
# from .forms import AdForm
# from .forms import AdCreateForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.db import connection
from ads.utils import dump_queries
from django.db.models import Q

class AdListView(OwnerListView):
    model = Ad
    # fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')
    template_name = "ads/ad_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval) 
            query.add(Q(text__icontains=strval), Q.OR)
            ad_listings = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :
            ad_listings = Ad.objects.all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in ad_listings:
            obj.natural_updated = naturaltime(obj.updated_at)


### FAV ###
        ad_list = Ad.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'ad_list' : ad_listings, 'search': strval,  'favorites': favorites}
        return render(request, self.template_name, ctx)

        dump_queries()
        return retval;


class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
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
    fields = ['title', 'price', 'text', 'pic']
    # success_url = reverse_lazy('ads:ad_list')
    template_name = "ads/ad_detail.html"

    def get(self, request, pk) :
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        # (ad=x): 'ad': field in the model; 'x': variable in the view
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)
    

class AdUpdateView(UpdateView):
    model = Ad
    fields = ['title', 'price', 'text']
    # success_url = reverse_lazy('ads:ad_list')

class AdDeleteView(DeleteView):
    model = Ad
    # success_url = reverse_lazy('ads:ad_list')

# class CommentListView(ListView):
#     model = Comment
#     post_comments = Comment.objects.all(filter_by )

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment 
    # success_url = reverse_lazy('ads:all')
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))


class CommentUpdateView(OwnerUpdateView):
    model = Comment
    fields = ['text']
    template_name = "ads/ad_comment_update.html"
    # success_url = reverse_lazy('ads:all')
    def get_success_url(self):
        ad = self.object.ad

    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[ad.id]))   

class CommentDeleteView(OwnerDeleteView):
    model = Comment 
    template_name = "ads/ad_comment_confirm_delete.html"
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


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()





# class PicListView(OwnerListView):
#     model = Pic
#     template_name = "pic/pic_list.html"

# class PicDetailView(OwnerDetailView):
#     model = Pic
#     template_name = "pic/pic_detail.html"

# class PicCreateView(OwnerCreateView):
#     model = Pic
#     template_name = "pic/pic_form.html"
#     success_url = reverse_lazy('pics:all')

#     def get(self, request, pk=None) :
#         form = pics/PicCreateForm()
#         ctx = { 'form' : form }
#         return render(request, self.template, ctx)

#     def post(self, request, pk=None) :
#         form = pics/PicCreateForm(request.POST, request.FILES or none)

#         if not form.is_valid() :
#             ctx = { 'form' : form }
#             return render(request, self.template, ctx)
        
#         pic = form.save(commit=False)
#         pic.owner = self.request.user