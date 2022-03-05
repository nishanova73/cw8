from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from webapp.forms import ReviewForm
from webapp.models import Product, Review


class ProductList(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'product_list'


class ProductView(DetailView):
    model = Product
    template_name = 'product_view.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mid_grade'] = 0
        print('pk:', self.kwargs['pk'])
        reviews = Review.objects.filter(product_id=self.kwargs['pk'])
        for i in reviews:
            context['mid_grade'] += i.mark
        if len(reviews):
            context['mid_grade'] = '{:.2f}'.format(context['mid_grade'] / len(reviews))
        return context


class ProductEdit(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_update.html'
    fields = ['image', 'name', 'category', 'description']
    success_url = reverse_lazy('webapp:main_page')
    permission_required = 'webapp:change_product'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('webapp:main_page')
    permission_required = 'webapp:delete_product'


class ProductCreate(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product_create.html'
    fields = ['image', 'name', 'category', 'description']
    success_url = reverse_lazy('webapp:main_page')
    permission_required = 'webapp:add_product'


class ReviewEdit(View):
    def get(self, *args, **kwargs):
        review = Review.objects.get(pk=self.kwargs['pk'])
        if self.request.user == review.author or self.request.user.has_perm('webapp.change_review'):
            form = ReviewForm(instance=review)
            return render(self.request, 'review_edit.html', {'pk': self.kwargs['pk'], 'form': form})
        else:
            raise PermissionDenied()

    def post(self, *args, **kwargs):
        form = ReviewForm(self.request.POST)
        if form.is_valid():
            review = Review.objects.get(pk=self.kwargs['pk'])
            review.review_text = form.cleaned_data.get('review_text')
            review.grade = form.cleaned_data.get('grade')
            review.save()
            return redirect(reverse('webapp:product_view', args=(review.product_id,)))
        else:
            return render(self.request, 'review_create.html', {'form': form, 'pk': self.kwargs['pk']})


class ReviewCreate(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def get(self, *args, **kwargs):
        return render(self.request, 'review_create.html', {'form': ReviewForm(), 'pk': self.kwargs['pk']})

    def post(self, *args, **kwargs):
        form = ReviewForm(self.request.POST)
        if form.is_valid():
            review = Review()
            review.author = self.request.user
            review.product_id = self.kwargs['pk']
            review.review_text = form.cleaned_data.get('review_text')
            review.grade = form.cleaned_data.get('grade')
            review.save()
            return redirect(reverse('webapp:product_view', args=(self.kwargs['pk'],)))
        else:
            return render(self.request, 'review_create.html', {'form': form, 'pk': self.kwargs['pk']})


class ReviewDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('accounts:login')
    model = Review
    template_name = 'product_delete.html'

    def get(self, *args, **kwargs):
        if self.request.user == Review.objects.get(pk=self.kwargs['pk']).author or self.request.user.has_perm(
                'webapp:delete_review'):
            return super().get(*args, **kwargs)
        else:
            raise PermissionDenied()

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.kwargs['id']})
