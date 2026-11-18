"""Explainable AI matching engine - rule-based, pure python.
Total 100: Budget 20, City/Area 15, Food 10, Habits 15, Cleanliness 15, Sleep 10, Guests+Noise 10, Pets 5
"""
def _habit_score(a,b):
    if a==b: return 1.0
    if "occasionally" in (a,b): return 0.6
    return 0.0

def compatibility(a,b):
    breakdown=[]
    # Budget 20
    overlap=max(0, min(a.budget_max,b.budget_max)-max(a.budget_min,b.budget_min))
    union=max(a.budget_max,b.budget_max)-min(a.budget_min,b.budget_min)
    if overlap>0:
        ratio=overlap/union if union else 1
        s=round(20*max(0.4, ratio))
        reason=f"Budget overlap hai Rs {overlap} - dono ke budget me common range hai."
    else:
        s=0
        reason="Budget overlap nahi hai - rent range match nahi karta."
    breakdown.append({"factor":"Budget Overlap","score":s,"max":20,"reason":reason})
    # City/Area 15
    if a.city.lower()==b.city.lower():
        if a.preferred_area and b.preferred_area and a.preferred_area.lower()==b.preferred_area.lower():
            s=15; reason=f"Same city ({a.city}) aur same preferred area ({a.preferred_area}). Perfect location match!"
        else:
            s=12; reason=f"Same city ({a.city}), area thoda alag ho sakta hai."
    else:
        s=0; reason=f"Cities alag hai: {a.city} vs {b.city}."
    breakdown.append({"factor":"City / Area","score":s,"max":15,"reason":reason})
    # Food 10
    if a.food_pref=="any" or b.food_pref=="any" or a.food_pref==b.food_pref:
        s=10; reason=f"Food preference compatible hai ({a.get_food_pref_display()} / {b.get_food_pref_display()})."
    elif {a.food_pref,b.food_pref}=={"veg","eggetarian"}:
        s=6; reason="Veg aur eggetarian usually saath comfortable rehte hai."
    else:
        s=2; reason="Food preference alag hai - kitchen sharing me adjustment lagega."
    breakdown.append({"factor":"Food Preference","score":s,"max":10,"reason":reason})
    # Habits 15
    hs=(_habit_score(a.smoking,b.smoking)+_habit_score(a.drinking,b.drinking))/2
    s=round(15*hs)
    reason=f"Smoking ({a.smoking}/{b.smoking}) aur drinking ({a.drinking}/{b.drinking}) habits score {s}/15."
    if hs>=0.9: reason+=" Habits bilkul match karte hai."
    elif hs==0: reason+=" Habits bilkul alag hai."
    breakdown.append({"factor":"Smoking + Drinking Habits","score":s,"max":15,"reason":reason})
    # Cleanliness 15
    diff=abs(a.cleanliness-b.cleanliness)
    s={0:15,1:11,2:7,3:3,4:0}.get(diff,0)
    reason=f"Cleanliness level {a.cleanliness}/5 vs {b.cleanliness}/5 - " + ("bilkul same standard hai." if diff==0 else "thoda difference hai." if diff<=2 else "bahut difference hai, dikkat ho sakti hai.")
    breakdown.append({"factor":"Cleanliness","score":s,"max":15,"reason":reason})
    # Sleep 10
    if a.sleep_schedule==b.sleep_schedule or "flexible" in (a.sleep_schedule,b.sleep_schedule):
        s=10; reason=f"Sleep schedule compatible hai ({a.get_sleep_schedule_display()} / {b.get_sleep_schedule_display()})."
    else:
        s=2; reason="Ek early bird hai, dusra night owl - sleep timing alag hai."
    breakdown.append({"factor":"Sleep Schedule","score":s,"max":10,"reason":reason})
    # Guests+Noise 10
    order={"never":0,"rarely":1,"sometimes":2,"often":3}
    gd=abs(order.get(a.guests_freq,1)-order.get(b.guests_freq,1))
    gs={0:5,1:4,2:2,3:0}.get(gd,2)
    norder={"low":0,"medium":1,"high":2}
    nd=abs(norder.get(a.noise_tolerance,1)-norder.get(b.noise_tolerance,1))
    ns={0:5,1:3,2:1}.get(nd,3)
    s=gs+ns
    reason=f"Guests frequency aur noise tolerance combined score {s}/10."
    breakdown.append({"factor":"Guests + Noise","score":s,"max":10,"reason":reason})
    # Pets 5
    if a.pets_ok==b.pets_ok:
        s=5; reason="Dono ki pets preference same hai."
    else:
        s=1; reason="Ek ko pets ok hai, dusre ko nahi - pehle discuss karna hoga."
    breakdown.append({"factor":"Pets","score":s,"max":5,"reason":reason})

    total=sum(x["score"] for x in breakdown)
    if total>=80: level="Excellent"
    elif total>=65: level="Good"
    elif total>=50: level="Moderate"
    else: level="Low"
    return {"total":total,"level":level,"breakdown":breakdown}

def compatibility_score(a,b):
    return compatibility(a,b)["total"]
