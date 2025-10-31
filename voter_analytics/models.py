# File: models.py
# Author: Dawson Maska (dawsonwm@bu.edu), 10/28/2025
# Description: models file for voter_analytics application.  
# Creates the classes that define the data models for the application.

from django.db import models

# Create your models here.
class Voter(models.Model):
    name = models.TextField(blank=True)
    address = models.TextField(blank=True)
    dob = models.DateField(blank=True)
    registration_date = models.DateField(blank=True)
    party = models.TextField(blank=True)
    precint = models.TextField(blank=True)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """Return a human-readable representation of the model instance."""
        return f"Name: {self.name} Address: {self.address} Party: {self.party}"
    
    def get_voting_history(self):
        """Return a list of elections the voter has participated in."""
        history = []
        if self.v20state:
            history.append("2020 State Election")
        if self.v21town:
            history.append("2021 Town Election")
        if self.v21primary:
            history.append("2021 Primary Election")
        if self.v22general:
            history.append("2022 General Election")
        if self.v23town:
            history.append("2023 Town Election")
        return history
    
    def get_election_history(self):
        """Return a list of elections as string the voter has participated in to make graph easy to make."""
        history = []
        if self.v20state:
            history.append("v20state")
        if self.v21town:
            history.append("v21town")
        if self.v21primary:
            history.append("v21primary")
        if self.v22general:
            history.append("v22general")
        if self.v23town:
            history.append("v23town")
        return history
    
def load_data():
    """Load the cvs data into the database."""

    # very dangerous!
    Voter.objects.all().delete()

    filename = "C:/Users/dawso/Downloads/newton_voters.csv"
    f = open(filename, "r") # open the file for reading

    line = f.readline() #remove header

    # 0 = id
    # 1 = last name
    # 2 = first name
    # 3 = street number
    # 4 = street name
    # 5 = apartment number
    # 6 = zip code
    # 7 = dob
    # 8 = registration date
    # 9 = party
    # 10 = precint
    # 11 = v20state
    # 12 = v21town
    # 13 = v21primary
    # 14 = v22general
    # 15 = v23town
    # 16 = voter score
    for line in f:
        try:
            fields = line.strip().split(",")

            v = Voter()
            v.name = fields[2] + " " + fields[1]
            # I LOVE ONE LINE IF STATEMENTS
            apartment = "Apt " + fields[5] + ', ' if fields[5] != "" else ""
            v.address = fields[3] + ' ' + fields[4] + ', ' + apartment + fields[6]
            v.dob = fields[7]
            v.registration_date = fields[8]
            v.party = fields[9]
            v.precint = fields[10]
            v.v20state = fields[11] == "TRUE"
            v.v21town = fields[12] == 'TRUE'
            v.v21primary = fields[13] == 'TRUE'
            v.v22general = fields[14] == 'TRUE'
            v.v23town = fields[15] == 'TRUE'
            v.voter_score = int(fields[16])

            v.save()
        except Exception as e:
            print(f"Could not process line: {line}")
            print(e)

    print(f"Done. Created {len(Voter.objects.all())} Results")
    f.close()
