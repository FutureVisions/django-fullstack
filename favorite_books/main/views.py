from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt

def home(request):
    return render(request, "log_reg.html")

def home_create(request):
    errors = User.objects.basic_validator(request.POST)
    user= User.objects.filter(email=request.POST['email'])
    if user:
        messages.error(request, "Email is already taken!")
        return redirect('/')
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    new_user=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=pw_hash
        )
    request.session['log_user_id'] = new_user.id
    return redirect('/dashboard')

def log_user(request):
    user= User.objects.filter(email=request.POST['email'])
    if user:
        logged_user= user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['log_user_id'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid Email or Password!', extra_tags='invalid')
            return redirect('/')
    messages.error(request, "Email or Password does not exist", extra_tags='not_found')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'all_books': Book.objects.all()
    }
    return render(request, 'dashboard.html', context)

def add_book(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/dashboard')
    this_user= User.objects.get(id=request.session['log_user_id'])
    create_book=Book.objects.create(
        title=request.POST['title'],
        desc=request.POST['desc'],
        uploaded_by= User.objects.get(id=request.session['log_user_id'])
    )
    create_book.users_who_like.add(this_user)
    return redirect('/dashboard')

def favorite(request, book_id):
    this_book= Book.objects.get(id=book_id)
    this_user= User.objects.get(id=request.session['log_user_id'])
    this_book.users_who_like.add(this_user)
    return redirect('/dashboard')

def unfavorite(request, book_id):
    this_book= Book.objects.get(id=book_id)
    this_user= User.objects.get(id=request.session['log_user_id'])
    this_book.users_who_like.remove(this_user)
    return redirect('/dashboard')

def show(request, book_id):
    context = {
        'this_user': User.objects.get(id=request.session['log_user_id']),
        'this_book': Book.objects.get(id=book_id),
        'all_users': Book.objects.get(id=book_id).users_who_like.all()
    }
    return render(request, 'show_book.html', context)

def update(request, book_id):
    book_to_update= Book.objects.get(id=book_id)
    book_to_update.title= request.POST['book_title']
    book_to_update.desc= request.POST['book_desc']
    book_to_update.save()
    # messages.success(request, 'Your book has been updated!')
    return redirect(f'/show_book/{book_id}')

def delete(request, book_id):
    book_delete= Book.objects.get(id=book_id)
    book_delete.delete()
    return redirect('/dashboard')
# Create your views here.
