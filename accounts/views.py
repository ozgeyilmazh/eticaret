from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
"""
def signUpUser(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')

		newUser = User(username = username, email = email)
		newUser.set_password(password)

		newUser.save()
		login(request, newUser)
		messages.success(request, 'Registration Successful')

		return redirect('/')
	context = {
		'form': form
	}
	return render(request, 'registration/signup.html', context)
"""


def signUpUser(request):
    context = dict()
    url = request.META.get('HTTP_REFERER')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password == confirm:
            if User.objects.filter(username=username).exists():
                print("Username taken ")
                context['username'] = "Bu kullanıcı Adı daha önce alınmış."
                messages.warning(request, "Bu kullanıcı Adı daha önce alınmış")

                return redirect(url, context)

            elif User.objects.filter(email=email).exists():
                print("Email taken ")
                context['email'] = "Bu email daha önce kullanılmış."
                messages.warning(request, "Bu email daha önce kullanılmış.")

                return redirect(url, context)
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                print("user created ")
                messages.warning(request, "Başarılı bir şekilde kayıt oldunuz.")

                return redirect('/')
        else:
            print('Password not matching.. ')
    else:

        context['form'] = form

        return render(request, 'registration/register.html', context)


def loginUser(request):
    context = dict()

    form = LoginForm(request.POST or None)
    print(form)
    context['form'] = form

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        print(email)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None:
            messages.info(request, 'Username or Password Wrong ')
            return render(request, 'registration/login.html', context)

        messages.success(request, 'Login Successful')
        login(request, user)
        return redirect('/')

    return render(request, 'registration/login.html', context)


def logoutUser(request):
    context = dict()

    logout(request)
    message = messages.success(request, 'Exit Successful')

    context['form'] = message

    return redirect('/', context)

