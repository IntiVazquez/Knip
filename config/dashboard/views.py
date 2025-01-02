from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from config.shorter.forms import URLForm
from config.shorter.models import URL

class DashboardView(LoginRequiredMixin, ListView):
    model = URL
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'urls_created'
    ordering = '-creation_date'

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(user=self.request.user)

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(raw_url__icontains=search_query) | Q(short_url__icontains=search_query)
            )

        return queryset

def editURL(request, url_id):
    url = get_object_or_404(URL, id=url_id)
    if request.method == "POST":
        tempSU = url.short_url
        form = URLForm(request.POST, instance=url)
        if form.is_valid():
            if not form.cleaned_data.get('short_url'):
                form = form.save(commit=False)
                form.short_url = tempSU
            form.save()
            return HttpResponse(
                status=204,
                                headers={
                    'HX-Trigger': 'urlListChanged'
                    })
    else:
        form = URLForm(instance=url)
    return render(request, 'dashboard/editURL.html', {
        'form' : form,
        'url' : url,
    })
    

    
class DeleteURLView(LoginRequiredMixin, DeleteView):
    model = URL
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'dashboard/confirm_delete.html'

    def get_object(self, queryset=None):
        url_id = self.kwargs.get('url_id')
        return get_object_or_404(URL, id=url_id, user=self.request.user)