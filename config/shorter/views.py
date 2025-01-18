from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import URL
from .forms import URLForm


def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            raw_url = form.cleaned_data['raw_url']
            short_url = form.cleaned_data['short_url']

            if not short_url:
                short_url = URL.random_url()

                while URL.objects.filter(short_url=short_url).exists():
                    short_url = URL.random_url()

            # Verificar si el short_url ya existe
            if URL.objects.filter(short_url=short_url).exists():
                messages.error(request, 'El URL personalizado ya existe, ingrese otro distinto')
            else:
                if request.user.is_authenticated:
                    URL.objects.create(raw_url=raw_url, short_url=short_url, user=request.user)
                else:
                    URL.objects.create(raw_url=raw_url, short_url=short_url)
                messages.success(request, short_url, extra_tags="url_success")
                
                return redirect('shorter:home')

        else:
            # Mostrar mensajes de error
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    else:
        form = URLForm()

    return render(request, "shorter/home.html", {'form': form})



def redirectURL(request, short_url):
    # Evita conecciones a Neon inecesarios
    if short_url == '':
        return redirect('shorter:home')
    
    try:
        url_data = URL.objects.get(short_url = short_url)
        url_data.used()
        return redirect(url_data.raw_url)

    except URL.DoesNotExist:
        messages.error(request, 'El URL ingresado no existe')
        return redirect('shorter:home')
    

