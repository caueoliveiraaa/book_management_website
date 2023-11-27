from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta
from .models import *
from .filters import BookFilter
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode

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


def show_users(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        paginator = Paginator(users, 5) 
        page = request.GET.get('page')
        reservations = Reservation.objects.filter(user=request.user)

        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=request.user, bill=0.0)

        bill = 0.0
        user_profile.bill = bill
        for reservation in reservations:
            today = datetime.now().date()
            if reservation.deadline_date and reservation.deadline_date > today:
                days_difference = (reservation.deadline_date - today).days
                for _ in range(days_difference + 1):
                    user_profile.bill += 0.01
                    user_profile.bill = round(user_profile.bill, 2)
                    bill = user_profile.bill
                    user_profile.save()

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)


        context = {'bill': bill, 'users': users, 'user_id': request.user.id}

        return render(request, 'show_users.html', context)

    return redirect('index')


def del_users(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=user_id)
        name = user.username
        user.delete()
        messages.success(request, f'Usuário \'{name}\' excluído com sucesso.')
        return redirect('show_users')

    return redirect('index')


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


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        
    return render(request, 'index.html')


def reserve_book(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Books, id=book_id)
        name_param = request.POST.get('name', '')
        status_param = request.POST.get('status', '')
        url_params = urlencode({'name': name_param, 'status': status_param})

        if request.method == 'POST':
            try:
                user = request.user  
                reservation_date = request.POST.get('user_date')

                if reservation_date is not None:
                    existing_reservation = book.reservations.filter(reservation_date=reservation_date).first()
                    if existing_reservation:
                        messages.success(request, "Já existe uma reserva nessa data!")
                        return HttpResponseRedirect(f'{reverse("show_books_filter")}?{url_params}')

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
                else:
                    messages.error(request, "É preciso informar uma data!")
            except Exception as e:
                print(f'Ocorreu um erro ao extrair data: {e}')

        return HttpResponseRedirect(f'{reverse("show_books_filter")}?{url_params}')
    
    return redirect('index')


def take_book(request, book_id, reservation_id):
    if request.user.is_authenticated:
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


def return_book(request, book_id, reservation_id):
    if request.user.is_authenticated:    
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


def cancel_reservation(request, reservation_id):
    if request.user.is_authenticated:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        book = reservation.book
        book.reservas = models.F('reservas') - 1
        book.save()
        reservation.delete()

    return redirect("index")


def show_books_filter(request):
    if request.user.is_authenticated:
        books = Books.objects.all() 
        books_filter = BookFilter(request.GET, queryset=books)
        paginator = Paginator(books_filter.qs, 5)
        page = request.GET.get('page')

        try:
            books_data = paginator.page(page)
        except PageNotAnInteger:
            books_data = paginator.page(1)
        except EmptyPage:
            books_data = paginator.page(paginator.num_pages)

        return render(request, 'show_books_filters.html', {'books_data': books_data, 'form': books_filter})
    
    return redirect('index')


def update_book_status(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Books, id=book_id)
        name_param = request.POST.get('name', '')
        status_param = request.POST.get('status', '')
        url_params = urlencode({'name': name_param, 'status': status_param})

        if request.method == 'POST' and request.user.is_superuser:
            new_status = request.POST.get('new_status')
            print(f'new_status{new_status}')
            if new_status in ['Disponível', 'Reservado', 'Retirado']:
                book.status = new_status
                book.save()
            else:
                messages.error(request, 'Selecione uma opção válida.')
        else:
            messages.error(request, 'Apenas usuários administradores podem alterar status.')

        return HttpResponseRedirect(f'{reverse("show_books_filter")}?{url_params}')

    return redirect('index')



def add_books(request):
    if request.user.is_authenticated and request.user.is_superuser:
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


def del_books(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Books, id=book_id)
        name = book.name
        author = book.author
        book.delete()
        messages.success(request, f'Livro \'{name}\' de \'{author}\' excluído com sucesso.')
        return redirect('show_books_filter')
    
    return redirect('index')


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

    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(user=request.user)

        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=request.user, bill=0.0)

        bill = 0.0
        for reservation in reservations:
            today = datetime.now().date()
            if reservation.deadline_date and reservation.deadline_date > today:
                days_difference = (reservation.deadline_date - today).days
                for _ in range(days_difference + 1):
                    user_profile.bill += 0.01
                    user_profile.bill = round(user_profile.bill, 2)
                    bill = user_profile.bill
                    user_profile.save()
                    print(user_profile.bill)

        user_reservations = Reservation.objects.filter(user=request.user)
        reservations_count = len(user_reservations)
        paginator = Paginator(user_reservations, 5)
        page = request.GET.get('page')

        try:
            user_reservations = paginator.page(page)
        except PageNotAnInteger:
            user_reservations = paginator.page(1)
        except EmptyPage:
            user_reservations = paginator.page(paginator.num_pages)

        context = {'bill': bill, 'reservations_count': reservations_count, 'user_reservations':user_reservations}

    return render(request, 'index.html', context)
