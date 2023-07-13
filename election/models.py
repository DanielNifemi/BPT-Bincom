from django.db import models


class PollingUnit(models.Model):
    ward = models.ForeignKey('ward', on_delete=models.CASCADE)
    lga = models.ForeignKey('lga', on_delete=models.CASCADE)
    state = models.ForeignKey('state', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.announced_pu_results = None

    def __str__(self):
        return self.name


class AnnouncedPUResults(models.Model):
    polling_unit = models.ForeignKey('PollingUnit', on_delete=models.CASCADE)
    party = models.CharField(max_length=255)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.party}: {self.score}"


class Result(models.Model):
    polling_unit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE)
    party = models.CharField(max_length=255)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"Result for Polling Unit: {self.polling_unit} - Party: {self.party}"
