from django.db import models
"""
# Create your models here.
class Player(models.Model):
    player_id = models.CharField(primary_key=True, db_column='player_id')
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=10)
    team = models.CharField(max_length=10)
    # draft_position = models.IntegerField(null=True, blank=True)
    # ffcald_id = models.CharField(max_length=10, null=True, blank=True) # creating blank column to add the ff calc and adp info 
    # bye_week = models.IntegerField()
    # adp = models.FloatField()
    # draft_position = models.IntegerField() # need to add this for sorting from index of list

    class Meta:
        db_table = 'all_players'

    def __str__(self):
        return self.full_name
    """
class Adp(models.Model):
    player_id = models.CharField(primary_key=True, db_column='player_id')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=10)
    team = models.CharField(max_length=10)
    adp = models.FloatField(null=True)  # Add this field to match the "adp" key in the JSON
    bye = models.IntegerField()  # Add this field to match the "bye" key in the JSON
    draft_position = models.IntegerField()  # Add this field to match the "draft_position" key in the JSON
    ffcalc_id = models.CharField(max_length=10)  # Add this field to match the "ffcalc_id" key in the JSON,
    adp_formatted = models.FloatField()
    times_drafted = models.IntegerField()
    high = models.FloatField()
    low = models.FloatField() 
    stdev = models.FloatField()

    class Meta:
        db_table = 'adp'

    def __str__(self):
        return self.name