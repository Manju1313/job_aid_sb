from django.db import models

# Create your models here.
class BaseContent(models.Model):
    # ---------comments-----------------------------------------------------#
    # BaseContent is the abstract base model for all
    # the models in the project
    # This contains created and modified to track the
    # history of a row in any table
    # This also contains switch method to deactivate one row if it is active
    # and vice versa
    # ------------------------ends here---------------------------------------------#

    ACTIVE_CHOICES = ((0, 'Deleted'), (2, 'Active'),(3,"Inactive"))
    active = models.PositiveIntegerField(choices=ACTIVE_CHOICES,
                                         default=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # objects = ActiveQuerySet.as_manager()

    #                                        BaseContent
    class Meta:
        #-----------------------------------------#
        # Don't create a table in database
        # This table is abstract
        #--------------------ends here--------------------#
        abstract = True

class BoundaryLevel(BaseContent):
    name = models.CharField('Name', max_length=100)
    code = models.PositiveIntegerField(null=True,blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        """Return Name."""
        return str(self.name)

# class BoundaryLevel(BaseContent):
#     name = models.CharField('Name', max_length=100)
#     code = models.PositiveIntegerField(**OPTIONAL)
#     parent = models.ForeignKey('self', on_delete=models.DO_NOTHING,**OPTIONAL)

#     def __str__(self):
#         """Return Name."""
#         return str(self.name)

class Boundary(BaseContent):
    """Table to Save DIfferent Locations based on Level."""
    name = models.CharField('Name', max_length=100)
    code = models.CharField('Code', max_length=100, null=True,blank=True)
    boundary_level = models.ForeignKey(BoundaryLevel, null=True,blank=True,on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.DO_NOTHING)
    latitude = models.CharField(max_length=100, null=True,blank=True)
    longitude = models.CharField(max_length=100, null=True,blank=True)
    sacep     = models.ManyToManyField('self', blank=True)
    is_sacep  = models.BooleanField(default=False)
    operational  = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True,blank=True)
    art_center_email = models.EmailField(max_length=100, null=True,blank=True)
    
    def __str__(self):
        """Return Name."""
        return self.name


class MasterLookUp(BaseContent):
    name = models.CharField(max_length=400)
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING, null=True,blank=True)
    slug = models.SlugField(("Slug"), blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)





class Sacepconfig(BaseContent):
    art_center  = models.ForeignKey(Boundary,on_delete=models.DO_NOTHING,related_name="art_center_tagged")
    sacep       = models.ForeignKey(Boundary,on_delete=models.DO_NOTHING,related_name="sacep_tagged")
    deactivation_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.art_center.name +" - " +self.sacep.name


