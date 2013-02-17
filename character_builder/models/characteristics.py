from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50)
    flavor = models.TextField(blank=True)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Alignment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Level(models.Model):
    number = models.IntegerField()
    xp_required = models.IntegerField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return "%s: %s xp required" % (self.number, self.xp_required)


class Deity(models.Model):
    name = models.CharField(max_length=100)
    alignment = models.ForeignKey(Alignment)
    description = models.TextField()

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50)
    space = models.CharField(max_length=50)
    reach = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50)
    script = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name


class Vision(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'character_builder'

    def __unicode__(self):
        return self.name
