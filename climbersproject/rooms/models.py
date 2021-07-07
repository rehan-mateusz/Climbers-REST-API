from django.db import models

from climbersproject import settings

class Room(models.Model):
    name        = models.CharField(verbose_name='room_name',
        max_length=32)
    members     = models.ManyToManyField(settings.AUTH_USER_MODEL,
                    through = 'Membership')
    description = models.CharField(max_length=256)
    date        = models.DateTimeField()

    def get_owner(self):
        owner = self.members.through.objects.order_by('date_joined').first()
        return owner

    def __str__(self):
        return self.name

class Membership(models.Model):
    account     = models.ForeignKey(settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,)
    room        = models.ForeignKey(Room, on_delete=models.CASCADE,)
    date_joined = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['account', 'room'], name='unique_joining')]
