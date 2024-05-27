from django.shortcuts import render
from .models import *

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

def index(request):
    """view function for home page of site."""
    
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    #The 'all()' is implied by default.
    num_authors = Author.objects.all().count()
    
    num_genres =Genre.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }
    
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related books to the context
        context['books'] = self.object.book_set.all()   # 'book_set' is the default related name
        return context

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    context_object_name = 'bookinstance_list'

    def get_queryset(self):
        queryset = (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
        return queryset

class LoanedBooksForLibrariansListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to all users to see for the Librarians."""
    model = BookInstance
    permission_required = ('catalog.can_mark_returned', 'catalog.change_book')
    template_name = 'catalog/books_on_loan.html'
    paginate_by = 10
    context_object_name = 'bookinstance_list'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')