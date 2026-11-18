from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from finder.models import SeekerProfile, Room, Interest

PROFILES=[
 ("Aarav Sharma",24,"male","Delhi","Lajpat Nagar","working",8000,15000,"veg","no","no",5,"early_bird","day","rarely","low",False),
 ("Priya Patel",23,"female","Mumbai","Andheri West","working",12000,22000,"veg","no","occasionally",4,"night_owl","day","sometimes","medium",True),
 ("Rohan Mehta",26,"male","Bengaluru","Koramangala","working",10000,18000,"non-veg","occasionally","occasionally",3,"night_owl","wfh","sometimes","high",True),
 ("Sneha Kulkarni",22,"female","Pune","Kothrud","student",6000,11000,"veg","no","no",5,"early_bird","day","rarely","low",False),
 ("Arjun Singh",25,"male","Delhi","Lajpat Nagar","working",9000,16000,"eggetarian","no","no",4,"early_bird","day","rarely","medium",False),
 ("Kavya Reddy",24,"female","Hyderabad","Gachibowli","working",11000,20000,"non-veg","no","occasionally",4,"flexible","wfh","sometimes","medium",True),
 ("Vikram Das",27,"male","Guwahati","Ganeshguri","working",5000,10000,"non-veg","occasionally","yes",3,"night_owl","flexible","often","high",True),
 ("Ananya Das",23,"female","Guwahati","Ganeshguri","student",5000,9000,"veg","no","no",5,"early_bird","day","never","low",False),
 ("Rahul Verma",28,"male","Mumbai","Powai","working",15000,25000,"any","yes","yes",2,"night_owl","night","often","high",True),
 ("Ishita Bose",25,"female","Bengaluru","Koramangala","working",10000,17000,"veg","no","no",4,"flexible","wfh","rarely","medium",True),
 ("Karan Malhotra",26,"male","Pune","Hinjewadi","working",9000,15000,"any","occasionally","occasionally",3,"flexible","day","sometimes","medium",False),
 ("Meera Nair",24,"female","Hyderabad","Madhapur","student",7000,13000,"veg","no","no",5,"early_bird","day","rarely","low",False),
 ("Aditya Rao",29,"male","Bengaluru","HSR Layout","working",13000,22000,"eggetarian","no","no",4,"early_bird","day","sometimes","medium",False),
 ("Divya Iyer",26,"female","Delhi","Saket","working",12000,20000,"any","no","occasionally",4,"night_owl","flexible","sometimes","high",True),
 ("Nikhil Joshi",23,"male","Pune","Kothrud","student",6000,10000,"veg","no","no",4,"early_bird","day","never","low",False),
 ("Simran Kaur",25,"female","Mumbai","Andheri West","working",13000,23000,"veg","no","no",5,"early_bird","day","rarely","low",False),
 ("Imran Hussain",27,"male","Hyderabad","Gachibowli","working",10000,18000,"non-veg","no","no",3,"night_owl","night","sometimes","medium",True),
 ("Pooja Choudhury",24,"female","Guwahati","Beltola","working",6000,11000,"any","no","no",4,"flexible","day","rarely","medium",False),
]
ROOMS=[
 ("Sunny Single Room in Lajpat Nagar","Delhi","Lajpat Nagar",12000,"single","fully","WiFi, AC, Attached washroom","any"),
 ("Shared Room near Andheri Metro","Mumbai","Andheri West",15000,"shared","fully","WiFi, AC, Gym, Power backup","female"),
 ("Master Bedroom in Koramangala","Bengaluru","Koramangala",18000,"master","fully","WiFi, AC, Balcony, Parking","any"),
 ("Budget Room in Kothrud","Pune","Kothrud",8000,"single","semi","WiFi, Fan, Common kitchen","any"),
 ("Room in Gachibowli IT Area","Hyderabad","Gachibowli",14000,"single","fully","WiFi, AC, Food available","male"),
 ("Shared Room in Ganeshguri","Guwahati","Ganeshguri",7000,"shared","semi","WiFi, Fan","any"),
 ("Premium Room in Powai","Mumbai","Powai",22000,"master","fully","WiFi, AC, Gym, Pool","any"),
 ("Cozy Room in Saket","Delhi","Saket",16000,"single","semi","WiFi, Cooler","female"),
 ("Room near Hinjewadi Phase 1","Pune","Hinjewadi",11000,"shared","fully","WiFi, AC, Mess","male"),
 ("HSR Layout Master Room","Bengaluru","HSR Layout",20000,"master","fully","WiFi, AC, Parking, Balcony","any"),
]
class Command(BaseCommand):
    help="Seed demo data (idempotent - clears and recreates)"
    def handle(self,*args,**kwargs):
        Interest.objects.all().delete(); Room.objects.all().delete(); SeekerProfile.objects.all().delete()
        objs=[]
        for i,(name,age,gender,city,area,occ,bmin,bmax,food,smoke,drink,clean,sleep,work,guests,noise,pets) in enumerate(PROFILES):
            p=SeekerProfile.objects.create(name=name,age=age,gender=gender,city=city,preferred_area=area,occupation=occ,budget_min=bmin,budget_max=bmax,move_in_date=date.today()+timedelta(days=15),food_pref=food,smoking=smoke,drinking=drink,cleanliness=clean,sleep_schedule=sleep,work_schedule=work,guests_freq=guests,noise_tolerance=noise,pets_ok=pets,bio=f"Hi, I am {name}. Looking for a compatible roommate in {city} ({area}).",email=f"{name.split()[0].lower()}@example.com",phone=f"98{i:08d}")
            objs.append(p)
        for i,(title,city,area,rent,rtype,furn,amen,gender) in enumerate(ROOMS):
            Room.objects.create(title=title,city=city,area=area,rent=rent,room_type=rtype,available_from=date.today()+timedelta(days=7),furnished=furn,amenities=amen,looking_for_gender=gender,description=f"{title}. Great location, ready to move.",owner=objs[i % len(objs)])
        Interest.objects.create(from_profile=objs[0],to_profile=objs[4],message="Hi! Our budgets and area match, lets connect.",status="accepted")
        Interest.objects.create(from_profile=objs[1],to_profile=objs[15],message="Same area in Mumbai, interested!",status="pending")
        Interest.objects.create(from_profile=objs[2],to_profile=objs[9],message="Koramangala match!",status="pending")
        Interest.objects.create(from_profile=objs[6],to_profile=objs[7],message="Guwahati roommate search.",status="accepted")
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin","admin@example.com","admin123")
        else:
            u=User.objects.get(username="admin"); u.set_password("admin123"); u.is_staff=True; u.is_superuser=True; u.save()
        self.stdout.write(self.style.SUCCESS(f"Seeded {SeekerProfile.objects.count()} profiles, {Room.objects.count()} rooms, {Interest.objects.count()} interests. Admin: admin/admin123"))
