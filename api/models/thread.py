from django.db import models
from .user import User
from django.utils import timezone


class Publicacio(models.Model):
    num_likes = models.PositiveIntegerField(default=0)
    num_dislikes = models.PositiveIntegerField(default=0)
    # En cas que l'author associat s'elimini, tots el threads seus s'elimines
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='default_user')
    title = models.TextField(max_length=255, default='')
    body = models.TextField(max_length=35000, null=True)
    creation_data = models.DateTimeField(default=timezone.now)
    num_coments = models.PositiveIntegerField(default=0)
    num_boosts = models.PositiveIntegerField(default=0)

    # TODO: CAL FER ALGO SIMILAR PER AL CAS EN EL QUE S'HAGI EDITAT EL THREAD/LINK
    def temps_desde_creacio(self):
        temps = timezone.now()
        diff = temps - self.creation_data
        anys = diff.days // 365
        if anys > 0:
            return "fa {} anys".format(anys)
        mesos = diff.days // 30
        if mesos > 0:
            if mesos == 1: return "fa 1 mes"
            return "fa {} mesos".format(mesos)
        setmanes = diff.days // 7
        if setmanes > 0:
            if setmanes == 1: return "fa 1 setmana"
            return "fa {} setmanes".format(setmanes)
        dies = diff.days % 7
        if dies > 0:
            if dies == 1: return "fa 1 dia"
            return "fa {} dies".format(dies)
        hores = diff.seconds // 3600
        if hores > 0:
            if hores == 1: return "fa 1 hora"
            return "fa {} hores".format(hores)
        minuts = (diff.seconds % 3600) // 60
        if minuts > 0:
            if minuts == 1: return "fa 1 minut"
            return "fa {} minuts".format(minuts)

        return "Just ara"


class Thread(Publicacio):
    pass

class Link(Publicacio):
    url = models.TextField(max_length=35000,default='')