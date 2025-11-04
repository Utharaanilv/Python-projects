from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm
from .models import UserProfile
from django.contrib.auth import get_user_model


#  User Registration
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

#  User Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

#  User Logout
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def user_home_view(request):
    return render(request, 'accounts/user_home.html')




@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def user_home(request):
    return render(request, 'accounts/user_home.html')

User = get_user_model()

@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile  # ✅ correct relation

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        confirm_username = request.POST.get('confirm_username', '').strip()
        phone = request.POST.get('phone', '').strip()
        confirm_phone = request.POST.get('confirm_phone', '').strip()

        # Validation
        if username != confirm_username:
            messages.error(request, "Usernames do not match.")
            return redirect('edit_profile')

        if phone != confirm_phone:
            messages.error(request, "Phone numbers do not match.")
            return redirect('edit_profile')

        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Please enter a valid 10-digit phone number.")
            return redirect('edit_profile')

        # Check if username is already taken
        if User.objects.exclude(pk=user.pk).filter(username=username).exists():
            messages.error(request, "This username is already taken.")
            return redirect('edit_profile')

        #  Update User and UserProfile
        user.username = username
        user.save()

        profile.phone = phone
        profile.save()

        #  Refresh session so new username shows up immediately
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, user)

        messages.success(request, "Your profile has been updated successfully.")
        return redirect('user_home')  # Redirect to user home page

    # Pre-fill form with existing data
    context = {
        'username': user.username,
        'phone': profile.phone or ''
    }
    return render(request, 'accounts/edit_profile.html', context)