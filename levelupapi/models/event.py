from django.db import models


class Event(models.Model):
    description = models.CharField(max_length=55)
    date = models.DateField()
    time = models.TimeField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="events_hosted")
    attendees = models.ManyToManyField("Gamer", related_name="attending")

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value