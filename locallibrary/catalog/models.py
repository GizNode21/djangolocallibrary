from django.db import models

from django.urls import reverse # used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

import uuid # Required for unique book instances

# Create your models here.
class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre (e.g. Science Fiction, French Poetry, etc.)")
    
    def __str__(self):
        """String for representing the Model object"""
        return self.name
    
    def get_absolute_url():
        """Returns the url to express a single genre instance."""
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Genre already exists (case insensitive match)"
            ),
        ]

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    # Foreign key used because books only can have one author but authors can have multiple books
    # Author as a string rather than an object because it hasn't been declared yet in the file
    
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                        '">ISBN number</a>')
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we specify the object above.
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def __get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          help_text="Unique ID for this particular book across whole library.")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availabilty',
    )
    
    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        """String for representing the model object."""
        return f'{self.id}, ({self.book_title})'
    
    
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance"""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object"""
        return f'{self.last_name}, {self.first_name}'
    