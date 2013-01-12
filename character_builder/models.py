from django.db import models

class Source(models.Model):
    name = models.CharField(max_length = 50)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length = 50)
    space = models.CharField(max_length = 50)
    reach = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

class Race(models.Model):
    name = models.CharField(max_length = 50)
    source = models.ForeignKey(Source)
    average_height_text = models.CharField(max_length = 50)
    average_weight_text = models.CharField(max_length = 50)
    size = models.ForeignKey(Size)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class ClassType(models.Model):
    name = models.CharField(max_length = 100)
    role = models.ForeignKey(Role)
    source = models.ForeignKey(Source)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length = 100)
    class_type = models.ForeignKey(ClassType)
    race = models.ForeignKey(Race)
    level = models.IntegerField()
    
    # Abilities
    strength = models.IntegerField()
    constitution = models.IntegerField()
    dexterity = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()

    # Skills

    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length = 100)
    source = models.ForeignKey(Source)

    def __unicode__(self):
        return self.name
