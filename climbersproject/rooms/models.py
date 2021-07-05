from django.db import models

User = get_user_model()

class Room(models.model):
    name    = models.CharField(verbose_name='room_name',
        max_length=32)
    owner   = models.ManyToManyField(User, on_delete=models.DO_NOTHING,
                                     through='Membership')

    """To do: on_delete => custom function
    to set the oldest member as a new owner"""

class Membership(models.model):
    account     = models.ForeignKey(User, on_delete=models.CASCADE)
    room        = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True, editable=False)
