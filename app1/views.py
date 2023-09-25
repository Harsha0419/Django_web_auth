from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import FileUploadForm  # Import the FileUploadForm
from .models import UploadedFile  # Import the UploadedFile model

@login_required(login_url='login')
def HomePage(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            new_upload = UploadedFile(user=request.user, file=uploaded_file)
            new_upload.save()
            # Add any additional logic you need for file handling here
    else:
        form = FileUploadForm()
    
    # Query and display user's uploaded files on the home page
    uploaded_files = UploadedFile.objects.filter(user=request.user)
    
    context = {
        'form': form,
        'uploaded_files': uploaded_files,
    }
    return render(request, 'home.html', context)

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username and Password are not correct")

    return render(request, 'login.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Password and Confirm Password are not correct")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()

            return redirect('login')

    return render(request, 'signup.html')

def Logout(request):
    logout(request)
    return redirect('login')
