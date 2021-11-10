from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm, JoinForm, ProfileForm, EditForm
from django.contrib import auth
from .models import Profile

# main page
def main_page(request):
    return render(request, 'main.html', {})

# login page
def login_page(request):
    login_data = LoginForm()
    return render(request, 'login_page.html', {'login_data':login_data})

# Login Validation
def login_validate(request):
    login_data = LoginForm(request.POST)

    if login_data.is_valid():
        user = auth.authenticate(username=request.POST['id'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')

        error_message= 'You entered an incorrect user ID or password.'
        return render(request, 'login_page.html', {'login_data':login_data,'login_errors':error_message})
    error_message= 'The login form is strange. Please contact the developer.'
    return render(request, 'login_page.html', {'login_data':login_data,'login_errors':error_message})

# Log out  
def logout(request):
    auth.logout(request)
    return redirect('/')

# Membership page       
def join_page(request):
    if request.method =='POST':
        form_data = JoinForm(request.POST)
        profile_data = ProfileForm(request.POST)
        if form_data.is_valid() and profile_data.is_valid():
            # get_user_model helper Reference model classes through functions
            User = auth.get_user_model()

            username = form_data.cleaned_data['id']
            password = form_data.cleaned_data['password1']
              
            User.objects.create_user(username=username, password=password)

            email_address = form_data.cleaned_data['email_address']
            phone_number = profile_data.cleaned_data['phone_number']

            # email, phone_number Enrollment
            user_info = get_object_or_404(User, username=username)
            user_info.email = email_address
            user_info.profile.phone_number = phone_number

            user_info.save()
            
            return redirect('/')
        else :
            return render(request, 'join_page.html', {'join_data':form_data, 'profile_data':profile_data})

            
    else :
        form_data = JoinForm()
        profile_data = ProfileForm()

    return render(request, 'join_page.html', {'join_data':form_data, 'profile_data':profile_data})

# Personal information edit page
def edit_user_info(request):
    # User import model class
    User = auth.get_user_model()
    
    # Get logged in user information
    user_info = get_object_or_404(User, username = request.user.username)    

    if request.method =='POST':
        form_data = EditForm(request.POST,instance = user_info)
        profile_data = ProfileForm(request.POST, instance = user_info.profile)

        if form_data.is_valid() and profile_data.is_valid():
            password = form_data.cleaned_data['password1']
            print(password)
            email_address = form_data.cleaned_data['email_address']
            phone_number = profile_data.cleaned_data['phone_number']

            user_info.set_password(password)
            user_info.email = email_address
            user_info.profile.phone_number = phone_number

            user_info.save()

            user = auth.authenticate(username=request.user.username, password=password)
            auth.login(request, user)

            return redirect('/')
        else : 
            return render(request, 'edit_user.html', {'form_data':form_data, 'profile_data':profile_data})

    form_data = EditForm(instance = user_info)
    profile_data = ProfileForm(instance = user_info.profile)

    return render(request, 'edit_user.html', {'form_data':form_data, 'profile_data':profile_data})