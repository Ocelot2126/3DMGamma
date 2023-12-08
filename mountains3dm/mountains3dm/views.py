from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.core.mail import send_mail

import gpxpy



def saludo(request):
    
    return HttpResponse("Hola")


from django.shortcuts import render, redirect


from django.shortcuts import render, redirect
from django.template.loader import get_template

def index(request, user_email=" "):
    if request.method == 'POST':
        user_email_form = request.POST.get('user', None)
        if user_email_form:
            request.session['user_email'] = user_email_form
            request.session.save()
            return redirect('main')  # Cambiar 'main' a tu vista principal

    contexto = {'user_email': user_email}
    return render(request, 'index.html', contexto)



def main(request):
    user_email = request.session.get('user_email', None)
    return render(request, 'index2.html', {'user_email': user_email})


def coordenadas(request):
    print("La vista de coordenadas se está ejecutando.")

    user_email = request.session.get('user_email', None)

    if request.method == 'POST':
        # Si es una solicitud POST, obtén los datos enviados
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')

        # Asegurarse de que latitud y longitud tengan 10 caracteres
        latitud = formatear_coordenada(latitud)
        longitud = formatear_coordenada(longitud)

        # Resto del código de la vista...

        mensaje = f"Posicion enviada por la App\n\nVer la ubicación o responder a 3DM-App:\nhttps://us0.explore.garmin.com/textmessage/txtmsg?extId=08db07a1-bfb5-e964-000d-3aa7440a0000&adr=paumlopez_1127%40hotmail.com\n\n3DM-App ha enviado este mensaje desde:  Lat {latitud} Lon {longitud}\n\nNo respondas directamente a este mensaje.\n\nEste mensaje se te ha enviado utilizando el dispositivo de comunicación bidireccional por satélite inReach con GPS. Para obtener más información, visita http://explore.garmin.com/inreach."
        # no cambiar nunca 3DM-App, el soft en arduino lo necesita para mostrar bien el texto en el display LCD

        send_mail(
            "3DM App Coordinates",
            mensaje,          
            "aconcagua2126@gmail.com",
            [user_email],
            fail_silently=False,
        )

        # Renderizar la plantilla con los datos POST
        return render(request, 'coordenadasenviadas.html', {'latitud': latitud, 'longitud': longitud})

    # Si es una solicitud GET, simplemente renderiza la plantilla
    return render(request, 'enviocoordenadas.html')

def formatear_coordenada(coordenada):
    # Convertir la coordenada a un número decimal y luego formatearla con 10 caracteres y ceros adicionales si es necesario
    try:
        valor = float(coordenada)
        return f"{valor:.6f}"
    except ValueError:
        return coordenada



from django.shortcuts import render
from django.http import HttpResponse
import gpxpy


def cargaarchivo(request):
    user_email = request.session.get('user_email', None)
    if request.method == 'POST' and request.FILES['archivo_gpx']:
        archivo_gpx = request.FILES['archivo_gpx']
        gpx = gpxpy.parse(archivo_gpx)

        # Listas para almacenar las coordenadas
        lista_latitud = []
        lista_longitud = []

        # Número máximo de puntos que deseas extraer
        max_puntos = 50

        for track in gpx.tracks:
            for segment in track.segments:
                total_puntos = len(segment.points)
                paso = max(1, total_puntos // max_puntos)  # Asegura que haya al menos un punto por cada 'max_puntos'

                for i, point in enumerate(segment.points):
                    if i % paso == 0:
                        lista_latitud.append(point.latitude)
                        lista_longitud.append(point.longitude)

                        if len(lista_latitud) >= max_puntos:
                            break

                if len(lista_latitud) >= max_puntos:
                    break

        # Puedes realizar operaciones adicionales con las listas según tus necesidades

        # Ejemplo: Imprimir las listas
        print("Lista de latitudes:", lista_latitud)
        print("Lista de longitudes:", lista_longitud)

        lista_latitud = lista_latitud + [11.111111] * (50 - len(lista_latitud))
        lista_longitud = lista_longitud + [11.111111] * (50 - len(lista_longitud))

        codigogpx = "GPX 1234"
        mensaje = f"{codigogpx}\n" + "\n".join([f"{lat:.6f} {lon:.6f}" for lat, lon in zip(lista_latitud, lista_longitud)])

        send_mail(
            "3DM App GPX file",
            mensaje,          
            "aconcagua2126@gmail.com",
            [user_email],
            fail_silently=False,
        )

       # Renderizar una respuesta
        return render(request, 'archivocargado.html')

    return render(request, 'cargaarchivo.html')



def archivocargado(request):

    doc_externo=get_template('archivocargado.html')

    documento=doc_externo.render()

    return HttpResponse(documento)


def gracias(request):

    doc_externo=get_template('gracias.html')

    documento=doc_externo.render()

    return HttpResponse(documento)


def coordenadasenviadas(request):

    doc_externo=get_template('coordenadasenviadas.html')

    documento=doc_externo.render()

    return HttpResponse(documento)



def cambio3d(request):
    user_email = request.session.get('user_email', None)

    if request.method == 'POST':
        # Obtener el valor seleccionado en el menú desplegable
        modelo_3d = request.POST.get('modelo_3d')
        print("Modelo 3D seleccionado:", modelo_3d)

        if modelo_3d == "Everest":
            nombre = "Monte Everest"
            altura = "8848"
            latitudes = "27.9881 28.1234"
            longitudes = "86.9254, 87.2345"
            escalalongitud = "1.2"
            escalalatitud = "0.8"
            escalamm = "100"
            cumbre = "27.789865 87.561245"

        if modelo_3d == "K2":
            nombre = "K2"
            altura = "8611"
            latitudes = "27.9881 28.1234"
            longitudes = "86.9254, 87.2345"
            escalalongitud = "1.2"
            escalalatitud = "0.8"
            escalamm = "100"
            cumbre = "27.789865 87.561245"

        if modelo_3d != "Everest" and modelo_3d != "K2" : 
            nombre = "0"
            altura = "0"
            latitudes = "0"
            longitudes = "0"
            escalalongitud = "0"
            escalalatitud = "0"
            escalamm = "0"
            cumbre = "0"        

        mensaje = f"calibracion 1234\n{nombre}\n{altura}\n{latitudes}\n{longitudes}\n{escalalongitud}\n{escalalatitud}\n{escalamm}\n{cumbre}"

        send_mail(
            "3DM App 3D-Model Change",
            mensaje,
            "aconcagua2126@gmail.com",
            [user_email],
            fail_silently=False,
        )

        # Renderizar la plantilla con los datos POST
        return render(request, 'cambio3denviado.html', {'modelo_3d': modelo_3d, 'user_email': user_email})

    # Si es una solicitud GET, simplemente renderiza la plantilla
    return render(request, 'cambio3d.html', {'user_email': user_email})


def cambio3denviado(request):

    doc_externo=get_template('cambio3denviado.html')

    documento=doc_externo.render()

    return HttpResponse(documento)





    
    
