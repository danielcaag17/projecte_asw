from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect,get_object_or_404
from ..models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def votar_publicacio(request, thread_id):

    publicacio = get_object_or_404(Publicacio, pk=thread_id)
    user = User.objects.get(pk='default_user')
    #user = request.user

    if request.method == 'POST':
            tipus_vot = request.POST.get('vote_type')
        #TODO: COMPROVAR COM EL DANI HA ACABAT FENT ELS USUARIS
 #       if not request.user.is_authenticated and False:
 #           return redirect('login')

  #      else:
            #Mirem si l'usuari ja ha votat
            if Vot.objects.filter(user=user, publicacio=publicacio).exists():
                print("JA EXISTEIX")
                vot = Vot.objects.get(user=user, publicacio=publicacio)

                if tipus_vot == 'positiu':
                    if (vot.positiu): #Si el vot ja era positiu eliminem el vot i actualitzem publicació
                        vot.delete() #Eliminem el vot del sistema
                        publicacio.num_likes -= 1
                        publicacio.save()

                    else: #El vot passa a ser positiu perque abans era negatiu
                        publicacio.num_likes +=1
                        publicacio.num_dislikes -= 1
                        vot.positiu = True
                        vot.save()
                        publicacio.save()

                else:
                    if (not vot.positiu):
                        vot.delete()  # Eliminem el vot del sistema
                        publicacio.num_dislikes -=1
                        publicacio.save()

                    else:  # El vot passa a ser negatiu
                        publicacio.num_dislikes += 1
                        publicacio.num_likes -= 1
                        vot.positiu = False
                        vot.save()
                        publicacio.save()
            else: #Usuari encara no ha votat
                nou_vot = Vot(user=user, publicacio=publicacio, positiu=True)
                if tipus_vot == 'positiu':
                    publicacio.num_likes +=1
                    publicacio.save()
                else:
                    publicacio.num_dislikes +=1
                    nou_vot.positiu = False
                    publicacio.save()
                nou_vot.save()


    return redirect('main')
    # Renderizar la plantilla de la publicación (aquí debes devolver la página donde se encuentra la publicación)
    #return render(request, 'tu_app/plantilla_de_publicacion.html', {'publicacio': publicacio})


