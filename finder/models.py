from django.db import models
from django.contrib.auth.models import User

class SeekerProfile(models.Model):
    GENDER=[("male","Male"),("female","Female"),("other","Other")]
    OCCUPATION=[("student","Student"),("working","Working Professional"),("other","Other")]
    FOOD=[("veg","Veg"),("non-veg","Non-Veg"),("eggetarian","Eggetarian"),("any","Any")]
    HABIT=[("yes","Yes"),("no","No"),("occasionally","Occasionally")]
    SLEEP=[("early_bird","Early Bird"),("night_owl","Night Owl"),("flexible","Flexible")]
    WORK=[("day","Day Shift"),("night","Night Shift"),("wfh","Work From Home"),("flexible","Flexible")]
    GUESTS=[("never","Never"),("rarely","Rarely"),("sometimes","Sometimes"),("often","Often")]
    NOISE=[("low","Low"),("medium","Medium"),("high","High")]
    name=models.CharField(max_length=100)
    age=models.PositiveIntegerField(default=24)
    gender=models.CharField(max_length=10,choices=GENDER,default="other")
    city=models.CharField(max_length=80)
    preferred_area=models.CharField(max_length=100,blank=True)
    occupation=models.CharField(max_length=20,choices=OCCUPATION,default="working")
    budget_min=models.PositiveIntegerField(default=5000)
    budget_max=models.PositiveIntegerField(default=12000)
    move_in_date=models.DateField(null=True,blank=True)
    food_pref=models.CharField(max_length=20,choices=FOOD,default="any")
    smoking=models.CharField(max_length=15,choices=HABIT,default="no")
    drinking=models.CharField(max_length=15,choices=HABIT,default="no")
    cleanliness=models.IntegerField(default=3,help_text="1-5")
    sleep_schedule=models.CharField(max_length=20,choices=SLEEP,default="flexible")
    work_schedule=models.CharField(max_length=20,choices=WORK,default="day")
    guests_freq=models.CharField(max_length=20,choices=GUESTS,default="rarely")
    noise_tolerance=models.CharField(max_length=10,choices=NOISE,default="medium")
    pets_ok=models.BooleanField(default=False)
    bio=models.TextField(blank=True)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=20,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=["name"]
    def __str__(self): return f"{self.name} ({self.city})"

class Room(models.Model):
    ROOM_TYPE=[("single","Single"),("shared","Shared"),("master","Master")]
    FURNISHED=[("fully","Fully Furnished"),("semi","Semi Furnished"),("unfurnished","Unfurnished")]
    GENDER=[("male","Male"),("female","Female"),("any","Any")]
    title=models.CharField(max_length=150)
    city=models.CharField(max_length=80)
    area=models.CharField(max_length=100)
    rent=models.PositiveIntegerField()
    room_type=models.CharField(max_length=20,choices=ROOM_TYPE,default="single")
    available_from=models.DateField(null=True,blank=True)
    furnished=models.CharField(max_length=20,choices=FURNISHED,default="semi")
    amenities=models.TextField(blank=True)
    looking_for_gender=models.CharField(max_length=10,choices=GENDER,default="any")
    description=models.TextField(blank=True)
    owner=models.ForeignKey(SeekerProfile,on_delete=models.SET_NULL,null=True,blank=True,related_name="rooms")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=["rent"]
    def __str__(self): return f"{self.title} - {self.city}"

class Interest(models.Model):
    STATUS=[("pending","Pending"),("accepted","Accepted"),("rejected","Rejected")]
    from_profile=models.ForeignKey(SeekerProfile,on_delete=models.CASCADE,related_name="sent_interests")
    to_profile=models.ForeignKey(SeekerProfile,on_delete=models.CASCADE,related_name="received_interests")
    status=models.CharField(max_length=20,choices=STATUS,default="pending")
    message=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=["-created_at"]
        unique_together=["from_profile","to_profile"]
    def __str__(self): return f"{self.from_profile} -> {self.to_profile} ({self.status})"
