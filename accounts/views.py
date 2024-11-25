from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from accounts.forms import RegistrationForms
from django.contrib.auth.decorators import login_required



# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method =='POST':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            # Redirect to a success page.
                return redirect('home_view')
            else:
                return render(request, 'registration/login.html', {})

        else:
            # Return an 'invalid login' error message.
            return render(request, 'registration/login.html', {} )
    else:
        return redirect('home_view')
    

def logout_view(request):
    logout(request)
# Redirect to a success page.
    return redirect('home_view')


def register_view(request):
    if request.method == 'POST':
        user_form = RegistrationForms(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('home_view')
        else:
            return render(request, 'registration/register.html', {'user_form': user_form })
    else:
        user_form = RegistrationForms()
        return render(request, 'registration/register.html', {'user_form': user_form})



def profile_view(request):
    return render(request, 'profile/profile.html')

# def settings_view(request):
#     return render(request, 'profile/settings.html')
