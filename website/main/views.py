from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from datetime import datetime

from .forms import (
    CustomUserCreationForm,
    BookCreationForm
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)


@login_required
def show_users(request):
    users = User.objects.all()
    users_count = User.objects.count()
    reservations_count = Reservation.objects.count()

    context = {
        'reservations_count': reservations_count,
        'users_count': users_count,
        'users': users,
    }

    paginator = Paginator(users, 6) 
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'usersDisplay.html', context)


@login_required
def del_users(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('show_users')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro bem sucedido.")
            return redirect("index")
        else:
            messages.error(request, "Registro falhou.")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'index.html')


def reserve_book(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    
    if request.method == 'POST':
        user = request.user  
        reservation_date = request.POST.get('user_date')
        existing_reservation = book.reservations.filter(reservation_date=reservation_date).first()
        if existing_reservation:
            messages.success(request, "Já existe uma reserva nessa data!")
            return redirect("show_books")
    
        reservation = Reservation.objects.create(
            user=user,
            book=book,
            reservation_date=reservation_date
        )
        
        book.reservations.add(reservation)
        book.reservas = book.reservations.count()   
        book.status = 'Reservado'
        book.save()
        return redirect("show_books")
        
    return redirect("show_books")


@login_required
def take_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Books, id=book_id)
        if book.reservations.exists():
            if book.status == 'Reservado':
                user_reservation = book.reservations.filter(user=request.user).first()
                if user_reservation:
                    if user_reservation.reservation_date == datetime.now().date():
                        book.status = 'Retirado'
                        book.save()
                        messages.success(request, "Livro retirado com sucesso!")
                        return redirect("show_my_reservations")
                    else:
                        messages.error(request, "Data de retirada não é hoje!")
                        return redirect("show_my_reservations") 
            else:
                messages.error(request, "Este livro não está reservado!")
                return redirect("show_my_reservations") 
        else:
            messages.error(request, "Este livro não tem reservas!")
            return redirect("show_my_reservations")  

    return redirect("show_my_reservasions")


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect("show_my_reservasions")


@login_required
def show_my_reservasions(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    reservations_count = Reservation.objects.count()
    context = {'reservations_count': reservations_count, 'user_reservations':user_reservations}
    paginator = Paginator(user_reservations, 6)
    page = request.GET.get('page')
    try:
        user_reservations = paginator.page(page)
    except PageNotAnInteger:
        user_reservations = paginator.page(1)
    except EmptyPage:
        user_reservations = paginator.page(paginator.num_pages)

    return render(request, 'myReservations.html', context)


@login_required
def show_books(request):    
    books = Books.objects.all()
    books_count = Books.objects.count()

    context = {
        'books_count': books_count,
        'books': books,
    }

    paginator = Paginator(books, 6)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'booksDisplay.html', context)


@login_required
def add_books(request):
    if request.method == "POST":
        form = BookCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro cadastrado.")
            return redirect("index")
        else:
            messages.error(request, "Não foi possível cadastrar livro.")
    else:
        form = BookCreationForm()
    return render(request, "registeBook.html", {"form": form})


@login_required
def del_books(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    book.delete()
    return redirect('show_books')


def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            messages.error(request, "Login falhou, tente outra vez!")
    else:
        return render(request, 'index.html')
    return render(request, 'index.html')
