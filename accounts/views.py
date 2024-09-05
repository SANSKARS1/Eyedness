from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
# add auth_login
from django.contrib.auth import login as auth_login

from datetime import datetime, timedelta


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user credentials (username and password)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            profile = Profile.objects.get(user=user)
            
            if profile.is_verified:
                # Generate a new 2FA code for the user
                profile.generate_verification_code()
                
                # Send 2FA code to user's email
                subject = 'Your 2FA Verification Code'
                message = f'Your verification code is {profile.verification_code}. It is valid for 10 minutes.'
                recipient_list = [user.email]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
                
                messages.success(request, f'2FA code has been sent to your email: {user.email}.')
                
                # Forward the user to the 2FA code verification step
                return redirect('verify_2fa_code')
            else:
                messages.error(request, 'Please verify your email before logging in.')
                return redirect('verify_code')  # Redirect to email verification if not verified
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


# Step 2: Handle 2FA code submission
def verify_2fa_code(request):
    email=User.objects.get(email)
    profile = Profile.objects.get(id=)

    if request.method == 'POST':
        submitted_code = request.POST.get('code')

        # Check if the code is valid and within the time limit
        if profile.verification_code == submitted_code:
            if profile.is_code_valid():
                # Reset the verification code and login the user
                profile.verification_code = None  # Clear the code after successful 2FA
                profile.save()
                
                login(request, user)  # Log the user in after successful 2FA
                messages.success(request, 'Login successful.')
                return redirect('home')
            else:
                messages.error(request, 'The verification code has expired. Please request a new one.')
                return redirect('login')  # Or re-generate a new 2FA code
        else:
            messages.error(request, 'Invalid verification code.')
    
    return render(request, 'accounts/verify_2fa_code.html')
# Registration View
def register(request):
    if request.method == 'POST':
        # Getting data from the registration form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        biometric = 'biometric' in request.POST
        
        # Validation
        errors = []
        if not username or not email or not password or not password2:
            errors.append('All fields are required.')
        if password != password2:
            errors.append('Passwords do not match.')
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            errors.append('Invalid email address.')
        if User.objects.filter(username=username).exists():
            errors.append('Username already taken.')
        if User.objects.filter(email=email).exists():
            errors.append('Email already registered.')
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[@$!%*?&#]', password):
           errors.append('Password must be at least 8 characters long, include a special character, and contain alphanumeric characters.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/register.html')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, 'Registration successful! Please verify your email.')
        return redirect('verify_code')  # Redirect to verify code page after registration
        
    return render(request, 'accounts/register.html')


# Signal to send verification email after user is created
@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.generate_verification_code()
        
        # Send the email with verification code
        subject = 'Verify your account'
        message = f'Your verification code is {profile.verification_code}. Please enter this code to verify your account.'
        recipient_list = [instance.email]
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


# Verification Code View

from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def verify_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')

        # Retrieve the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return render(request, 'accounts/verify_code.html')

        # Get the user's profile
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            messages.error(request, 'Profile does not exist for this user.')
            return render(request, 'accounts/verify_code.html')

        # Check if the user is already verified
        if profile.is_verified:
            messages.info(request, 'This account is already verified.')
            return redirect('login')

        # Check if the user has exceeded the maximum attempts
        if profile.verification_attempts >= 3:
            messages.error(request, 'You have exceeded the maximum number of verification attempts. Please contact support.')
            return render(request, 'accounts/verify_code.html')

        # Verify the code
        if profile.verification_code == code:
            profile.is_verified = True
            profile.verification_attempts = 0  # Reset attempts on successful verification
            profile.save()
            messages.success(request, 'Your account has been verified. You can now log in.')
            return redirect('login')
        else:
            # Increment the verification attempts
            profile.verification_attempts += 1
            profile.save()

            # Check if the user has reached the limit of attempts
            if profile.verification_attempts >= 3:
                messages.error(request, 'You have exceeded the maximum number of verification attempts. Please contact support.')
            else:
                messages.error(request, f'Invalid verification code. You have {3 - profile.verification_attempts} attempts left.')
    
    return render(request, 'accounts/verify_code.html')

# Logout View
def logoutuser(request):
    logout(request)
    return redirect('home')
