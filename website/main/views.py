from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta
from .models import *
from .filters import BookFilter


from .forms import (
    CustomUserCreationForm,
    BookCreationForm
)

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
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
    paginator = Paginator(users, 6) 
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {'reservations_count': reservations_count, 'users_count': users_count, 'users': users}

    return render(request, 'show_users.html', context)


@login_required
def del_users(request, user_id):
    user = get_object_or_404(User, id=user_id)
    name = user.username
    user.delete()
    messages.success(request, f'Usuário \'{name}\' excluído com sucesso.')
    return redirect('show_users')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Usuário criado com sucesso.")
            return redirect("index")
        else:
            messages.error(request, "Registro falhou. Tente outra vez.")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'index.html')


@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    if request.method == 'POST':
        user = request.user  
        reservation_date = request.POST.get('user_date')
        existing_reservation = book.reservations.filter(reservation_date=reservation_date).first()
        if existing_reservation:
            messages.success(request, "Já existe uma reserva nessa data!")
            return redirect("show_books")

        reservation_date = datetime.strptime(reservation_date, "%Y-%m-%d")
        reservation_date = reservation_date.date()
        if reservation_date >= datetime.now().date():
            reservation = Reservation.objects.create(user=user, book=book, reservation_date=reservation_date)
            book.reservations.add(reservation)
            book.reservas = book.reservations.count()   
            book.status = 'Reservado'
            book.save()         
        else:
            messages.error(request, "Não é possível reservar livros para datas inferiores a data atual!")
        
    return redirect("show_books")


@login_required
def take_book(request, book_id, reservation_id):
    book = get_object_or_404(Books, id=book_id)
    if book.status == 'Reservado':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if reservation.reservation_date == datetime.now().date():
            book.status = 'Retirado'
            reservation.deadline_date = datetime.now().date() + timedelta(days=30)
            book.save()
            reservation.save()
            messages.success(request, "Livro retirado com sucesso!")
            return redirect("index")
        else:
            messages.error(request, "A data de retirada desse livro não é hoje!")
            return redirect("index") 
    else:
        messages.error(request, "Este livro não está com status reservado!")
        return redirect("index") 


@login_required
def return_book(request, book_id, reservation_id):
    book = get_object_or_404(Books, id=book_id)
    if book.status == 'Retirado':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.delete()
        book.status = 'Disponível'
        book.save()
        reservation.save()
        messages.success(request, "Livro devolvido com sucesso!")
        return redirect("index")
    else:
        messages.error(request, "Este livro não está com status retirado!")
        return redirect("index") 


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    book = reservation.book
    book.reservas = models.F('reservas') - 1
    book.save()
    reservation.delete()
    return redirect("index")


@login_required
def show_books(request):
    books = Books.objects.all()
    books_count = Books.objects.count()
    paginator = Paginator(books, 6)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
        
    context = {'books_count': books_count, 'books': books}

    return render(request, 'show_books.html', context)


@login_required
def show_books_filter(request):
    books = Books.objects.all()
    books_count = Books.objects.count()
    paginator = Paginator(books, 6)
    page = request.GET.get('page')

    books_filter = BookFilter(request.GET, queryset=books)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
        
    context = {'books_count': books_count, 'books': books, 'filter': books_filter}

    return render(request, 'show_books.html', context)


@login_required
def add_books(request):
    if request.user.is_superuser:
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
    else:
        messages.error(request, "Apenas usuários administradores podem cadastrar livros.")
        return redirect("index")

    return render(request, "add_books.html", {"form": form})


@login_required
def del_books(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    name = book.name
    author = book.author
    book.delete()
    messages.success(request, f'Livro \'{name}\' de \'{author}\' excluído com sucesso.')
    return redirect('show_books')


def index(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Login falhou, tente outra vez!")
            return render(request, 'index.html', context)
        
        user.save()
        login(request, user)

    elif request.user.is_authenticated:
        reservations = Reservation.objects.filter(user=request.user)
        for reservation in reservations:
            today = datetime.now().date()
            if reservation.deadline_date and reservation.deadline_date > today:
                days_difference = (reservation.deadline_date - today).days
                for _ in range(days_difference + 1):
                    request.user.bill += 0.01
                    request.user.save()
        
        user_reservations = Reservation.objects.filter(user=request.user)
        reservations_count = len(user_reservations)
        paginator = Paginator(user_reservations, 6)
        page = request.GET.get('page')

        try:
            user_reservations = paginator.page(page)
        except PageNotAnInteger:
            user_reservations = paginator.page(1)
        except EmptyPage:
            user_reservations = paginator.page(paginator.num_pages)

        context = {'reservations_count': reservations_count, 'user_reservations':user_reservations}

    return render(request, 'index.html', context)
