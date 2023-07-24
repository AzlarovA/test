from django.shortcuts import render
from .models import Contact, FAQ
from .forms import ContactFormDB
# Create your views here.


def contacts_page(request):
    template_ = 'contacts/contacts_page.html'
    contact = Contact.objects.all()
    faq = FAQ.objects.all()
    message = ''
    if request.method == 'POST':
        form = ContactFormDB(request.POST)
        if form.is_valid():
            form.save()
            message = 'С вами скоро свяжутся'
            form = ContactFormDB()
    else:
        form = ContactFormDB()

    context = {
        "contact": contact,
        "faq": faq,
        "form": form,
        "message": message
    }
    return render(request, template_name=template_, context=context)
