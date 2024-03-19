from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginForm, AddRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
def home(request):
    return render(request, 'webapp/index.html')

#register user

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'webapp/register.html', context=context)

#login
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'form':form}
    return render(request, 'webapp/login.html', context=context)

#dashboard
@login_required(login_url='login')
def dashboard(request):
    records = Record.objects.all()
    context = {'records':records}
    return render(request, 'webapp/dashboard.html', context=context)

#add record
@login_required(login_url='login')
def add_record(request):
    form = AddRecordForm()
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/add-record.html', context=context)

#update record
@login_required(login_url='login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form':form}
    return render(request, 'webapp/update-record.html', context=context)

#read or view record
@login_required(login_url='login')
def single_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request, 'webapp/view-record.html', context=context)

#delete record
@login_required(login_url='login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    return redirect('dashboard')

#logout
def logout(request):
    auth.logout(request)
    return redirect('login')
