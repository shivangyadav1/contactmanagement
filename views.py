from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Data
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse

import pandas as pd
# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.models import User

from .models import Data


# from .forms import PositionForm


def getData(request):
    data = {'user': 'user', 'name': 'name', 'companyName': 'companyName', 'product': 'product', 'email': 'email',
            'created': 'created', }
    return render(request, 'test.html', {'dropdown1': data})
    #print(request.session['id'])


def upload(request):
    #print(request.session['id'])
    template = "fileUpload.html"
    prompt = {
        'order': 'Order of the CSV should be name, email, address,    phone, profile',
        # 'profiles': data
    }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    df = pd.read_csv(csv_file)
    for i in df.iterrows():
        a = {}
        if 'name' in i[1]:
            a['name'] = i[1]['name']
        else:
            a['name'] = 'unName'
        if 'company' in i[1]:
            a['companyName'] = i[1]['company']
        else:
            a['companyName'] = 'unName'
        if 'product' in i[1]:
            a['product'] = i[1]['product']
        else:
            a['product'] = 'unName'
        if 'email' in i[1]:
            a['email'] = i[1]['email']
        else:
            a['email'] = 'null@null.com'
        Data.objects.create(user=User.objects.get(id=request.session['id']), name=a['name'], product=a['product'], companyName=a['companyName'], email=a['email'])

    # data_set = csv_file.read().decode('UTF-8')
    # print(data_set, '1322132')
    return redirect('success')



class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)



def dropdown1(request):
    data = {'user':'user','name': 'name','companyName': 'companyName','product': 'product','email': 'email','created': 'created',}
    return render(request, 'test.html', {'dropdown1': data} )

def get_dropdown_value_from_db(request):
    print('-------------------------------> data from dropdown', request.GET.keys())

    return JsonResponse({'Result':'Success'})

# class TaskList(LoginRequiredMixin, ListView):
#     model = Task
#     context_object_name = 'tasks'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tasks'] = context['tasks'].filter(user=self.request.user)
#         context['count'] = context['tasks'].filter(complete=False).count()
#
#         search_input = self.request.GET.get('search-area') or ''
#         if search_input:
#             context['tasks'] = context['tasks'].filter(
#                 title__contains=search_input)
#
#         context['search_input'] = search_input
#
#         return context
#
#
# class TaskDetail(LoginRequiredMixin, DetailView):
#     model = Task
#     context_object_name = 'task'
#     template_name = 'base/task.html'
#
#
# class TaskCreate(LoginRequiredMixin, CreateView):
#     model = Task
#     fields = ['title', 'description', 'complete']
#     success_url = reverse_lazy('tasks')
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(TaskCreate, self).form_valid(form)
#
#
# class TaskUpdate(LoginRequiredMixin, UpdateView):
#     model = Task
#     fields = ['title', 'description', 'complete']
#     success_url = reverse_lazy('tasks')
#
#
# class DeleteView(LoginRequiredMixin, DeleteView):
#     model = Task
#     context_object_name = 'task'
#     success_url = reverse_lazy('tasks')
#     def get_queryset(self):
#         owner = self.request.user
#         return self.model.objects.filter(user=owner)
#
# class TaskReorder(View):
#     def post(self, request):
#         form = PositionForm(request.POST)
#
#         if form.is_valid():
#             positionList = form.cleaned_data["position"].split(',')
#
#             with transaction.atomic():
#                 self.request.user.set_task_order(positionList)
#
#         return redirect(reverse_lazy('tasks'))
