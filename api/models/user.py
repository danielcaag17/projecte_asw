from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    # Podem definir el maxim de caracters de username
    username = models.CharField(max_length=32, primary_key=True)
    description = models.TextField(default="")
    cover = models.ImageField(default="")
    avatar = models.ImageField(default="")

    # TODO: s'ha de veure quins camps respecte el registre s'han de tenir donat que es fa per google
    email = models.EmailField(unique=True)
    # Es pot definir com volem que sigui la contrasenya, quins caràcters especials
    password = models.CharField(max_length=16)
    # Amb auto_now_add es registrara la data i hora en el mateix moemtn que es crei el registre
    #  register_date = models.DateTimeField(auto_now_add=True)

    def set_password(self, password):
        # Guarda la contrasenya de forma segura amb bcrypt
        self.password = make_password(password)

    def check_password(self, password):
        # Verifica si la contrasenya donada coincideix amb el hash guardat
        return check_password(self.password, password)
