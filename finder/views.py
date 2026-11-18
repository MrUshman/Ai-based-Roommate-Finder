from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import SeekerProfile, Room, Interest
from .forms import SeekerProfileForm, RoomForm, InterestForm, RegisterForm
from .matching import compatibility

def home(request):
    seekers=SeekerProfile.objects.all()
    rooms=Room.objects.all()
    stats={"total_seekers":seekers.count(),"total_rooms":rooms.count(),"cities":seekers.values("city").distinct().count(),"avg_rent":round(rooms.aggregate(Avg("rent"))["rent__avg"] or 0)}
    by_city=list(seekers.values("city").annotate(c=Count("id")).order_by("-c"))
    max_c=max([x["c"] for x in by_city], default=1)
    for x in by_city: x["pct"]=int(x["c"]/max_c*100)
    rent_by_city=list(rooms.values("city").annotate(avg=Avg("rent")).order_by("city"))
    max_r=max([float(x["avg"] or 0) for x in rent_by_city], default=1)
    for x in rent_by_city: x["avg"]=round(x["avg"] or 0); x["pct"]=int(x["avg"]/max_r*100)
    # top matches preview: compute best pairs
    pairs=[]
    lst=list(seekers[:12])
    for i in range(len(lst)):
        for j in range(i+1,len(lst)):
            r=compatibility(lst[i],lst[j])
            pairs.append({"a":lst[i],"b":lst[j],"total":r["total"],"level":r["level"]})
    pairs=sorted(pairs,key=lambda x:-x["total"])[:6]
    return render(request,"finder/home.html",{"stats":stats,"by_city":by_city,"rent_by_city":rent_by_city,"top_matches":pairs,"recent_rooms":rooms.order_by("-created_at")[:6],"seekers":seekers[:6]})

def profile_list(request):
    qs=SeekerProfile.objects.all()
    city=request.GET.get("city",""); gender=request.GET.get("gender",""); max_budget=request.GET.get("max_budget",""); food=request.GET.get("food_pref","")
    if city: qs=qs.filter(city__iexact=city)
    if gender: qs=qs.filter(gender=gender)
    if max_budget:
        try: qs=qs.filter(budget_max__lte=int(max_budget))
        except: pass
    if food: qs=qs.filter(food_pref=food)
    cities=SeekerProfile.objects.values_list("city",flat=True).distinct().order_by("city")
    return render(request,"finder/profiles.html",{"profiles":qs,"cities":cities,"filters":request.GET})

def profile_detail(request,pk):
    p=get_object_or_404(SeekerProfile,pk=pk)
    others=SeekerProfile.objects.exclude(pk=pk)
    matches=[]
    for o in others:
        r=compatibility(p,o); matches.append({"profile":o,"total":r["total"],"level":r["level"]})
    matches=sorted(matches,key=lambda x:-x["total"])[:5]
    accepted=Interest.objects.filter(to_profile=p,status="accepted")
    show_contact=accepted.exists()
    return render(request,"finder/profile_detail.html",{"profile":p,"matches":matches,"all_profiles":others,"show_contact":show_contact})

def profile_create(request):
    form=SeekerProfileForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        obj=form.save(); messages.success(request,"Profile created!"); return redirect("profile_detail",pk=obj.pk)
    return render(request,"finder/form.html",{"form":form,"title":"Create Seeker Profile"})

def room_list(request):
    qs=Room.objects.all()
    city=request.GET.get("city",""); max_rent=request.GET.get("max_rent",""); rtype=request.GET.get("room_type","")
    if city: qs=qs.filter(city__iexact=city)
    if max_rent:
        try: qs=qs.filter(rent__lte=int(max_rent))
        except: pass
    if rtype: qs=qs.filter(room_type=rtype)
    cities=Room.objects.values_list("city",flat=True).distinct().order_by("city")
    return render(request,"finder/rooms.html",{"rooms":qs,"cities":cities,"filters":request.GET})

def room_detail(request,pk):
    room=get_object_or_404(Room,pk=pk)
    return render(request,"finder/room_detail.html",{"room":room})

def room_create(request):
    form=RoomForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        obj=form.save(); messages.success(request,"Room listed!"); return redirect("room_detail",pk=obj.pk)
    return render(request,"finder/form.html",{"form":form,"title":"Create Room Listing"})

def matches(request):
    profiles=SeekerProfile.objects.all()
    selected=None; results=[]
    pid=request.GET.get("profile") or request.POST.get("profile")
    if pid:
        selected=get_object_or_404(SeekerProfile,pk=pid)
        for o in profiles.exclude(pk=selected.pk):
            r=compatibility(selected,o); results.append({"profile":o,"total":r["total"],"level":r["level"],"breakdown":r["breakdown"]})
        results=sorted(results,key=lambda x:-x["total"])
    return render(request,"finder/matches.html",{"profiles":profiles,"selected":selected,"results":results})

def calculator(request):
    profiles = SeekerProfile.objects.all()
    result = None
    a = b = None
    aid = request.POST.get("a") or request.GET.get("a")
    bid = request.POST.get("b") or request.GET.get("b")
    if aid:
        try:
            a = SeekerProfile.objects.get(pk=aid)
        except SeekerProfile.DoesNotExist:
            pass
    if bid:
        try:
            b = SeekerProfile.objects.get(pk=bid)
        except SeekerProfile.DoesNotExist:
            pass
    if a and b and a.pk != b.pk:
        result = compatibility(a, b)
    elif a and b and a.pk == b.pk:
        messages.warning(request, "Please choose two different profiles.")
    return render(request, "finder/calculator.html", {"profiles": profiles, "result": result, "a": a, "b": b})

def interest_list(request):
    interests=Interest.objects.select_related("from_profile","to_profile").all()
    if request.method=="POST":
        iid=request.POST.get("interest_id"); action=request.POST.get("action")
        obj=get_object_or_404(Interest,pk=iid)
        if action in ("accepted","rejected"): obj.status=action; obj.save(); messages.success(request,f"Interest {action}.")
        return redirect("interests")
    profiles=SeekerProfile.objects.all()
    return render(request,"finder/interests.html",{"interests":interests,"profiles":profiles})

def send_interest(request):
    if request.method=="POST":
        form=InterestForm(request.POST)
        if form.is_valid():
            try:
                form.save(); messages.success(request,"Interest sent!")
            except Exception as e:
                messages.warning(request,"Interest already exists or invalid.")
        else:
            messages.warning(request,"Please fill the form correctly - profiles must be different.")
    return redirect("interests")

def register(request):
    form=RegisterForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=form.save(); login(request,user); messages.success(request,"Account created!"); return redirect("home")
    return render(request,"finder/register.html",{"form":form})
