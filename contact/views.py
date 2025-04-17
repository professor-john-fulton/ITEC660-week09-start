from django.shortcuts import render
from .forms import ContactForm
from .models import ContactMessage

from django.db import connection

def contact_view_old(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            # Process the data (e.g., save to a database or send an email)
            cleaned_data = form.cleaned_data
            print(cleaned_data)  # Example processing
            return render(request, 'contact/thank_you.html')  # Redirect to a thank-you page
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

           # Use raw SQL to insert data into the ContactMessage table
            # **IMPORTANT:** Use parameterization to prevent SQL injection!
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO contact_contactmessage (name, email, message, submitted_at) VALUES (%s, %s, %s, datetime('now'))",
                    [name, email, message]  # Pass values as a list or tuple
                )
            # The above assumes your table name is 'contact_contactmessage'.
            # Django creates table names based on the app name and model name.
            # Double-check your actual table name in your database (e.g., using DB Browser for SQLite).
            # You can find the table name in the sqlite database.  It's usually
            # <app_name>_<model_name>.  For example, if your app is named "contact"
            # and your model is named "ContactMessage", the table name will likely be
            # "contact_contactmessage".  You can also check your models.py file.

            print(form.cleaned_data)  # Keep this for debugging
            return render(request, 'contact/thank_you.html')
        else:
            # Form is invalid, re-render the form with errors
            return render(request, 'contact/contact.html', {'form': form})
    else:
        form = ContactForm()  # Instantiate the form for GET requests
    return render(request, 'contact/contact.html', {'form': form})

def home_view(request):
    return render(request, 'contact/home.html') 

