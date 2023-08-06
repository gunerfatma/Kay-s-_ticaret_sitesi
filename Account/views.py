from django.shortcuts import get_object_or_404, redirect, render
from Account.models import Accounts, UserProfile
from kartlar.models import Kart, KartItem
from kartlar.views import _kart_id
from siparis.models import Siparis, SiparisUrun
from .forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from  django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
import requests



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Accounts.objects.create_user(first_name=first_name,last_name=last_name,email=email, username=username, password= password)
            user.phone_number = phone_number
            user.save()

            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('Account/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/Account/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'Account/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email =email, password=password)

        if user is not None:
            try:
                kart = Kart.objects.get(kart_id= _kart_id(request))
                is_kart_item_exists = KartItem.objects.filter(kart=kart).exists()
                if is_kart_item_exists:
                    kart_item = KartItem.objects.filter(kart=kart)

                    urun_variation = []
                    for item in kart_item:
                        variation = item.variations.all()
                        urun_variation.append(list(variation))
                    
                    kart_item = KartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in kart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    

                    for pr in urun_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = KartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            kart_item = KartItem.objects.filter(kart=kart)
                            for item in kart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)     
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query

                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Geçersiz giriş bilgileri')
            return redirect('login')
    return render(request, 'Account/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out')
    return redirect('login')
    

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
    

@login_required(login_url = 'login')
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        userprofile = None

    orders = Siparis.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()


    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
        
    }
    return render(request, 'Account/dashboard.html', context)

    
def unuttumPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Accounts.objects.filter(email=email).exists():
            user = Accounts.objects.get(email__exact=email)

               
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('Account/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
                messages.error(request, 'Account does not exist!')
                return redirect('unuttumPassword')
    return render(request, 'Account/unuttumPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
    
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Accounts.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'Account/resetPassword.html')

@login_required(login_url='login')
def my_siparis(request):
    orders = Siparis.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'Account/my_siparis.html', context)



@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'Account/edit_profile.html', context)



@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Accounts.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'Account/change_password.html')



@login_required(login_url='login')
def siparis_detail(request, order_id):
    siparis_detail = SiparisUrun.objects.filter(order__order_number=order_id)
    siparis = Siparis.objects.get(order_number=order_id)
    subtotal = 0
    for i in siparis_detail:
        subtotal += i.urun_price * i.quantity

    context = {
        'siparis_detail': siparis_detail,
        'siparis': siparis,
        'subtotal': subtotal,
    }
    return render(request, 'Acoount/siparis_detail.html', context)