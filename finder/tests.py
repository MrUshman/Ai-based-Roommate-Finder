from django.test import TestCase
from datetime import date
from .models import SeekerProfile
from .matching import compatibility

def make(**kw):
    base=dict(name="Test",age=24,gender="male",city="Delhi",preferred_area="Lajpat Nagar",occupation="working",budget_min=8000,budget_max=15000,food_pref="veg",smoking="no",drinking="no",cleanliness=4,sleep_schedule="early_bird",work_schedule="day",guests_freq="rarely",noise_tolerance="medium",pets_ok=True)
    base.update(kw); return SeekerProfile(**base)

class MatchingTests(TestCase):
    def test_identical_high(self):
        a=make(name="A"); b=make(name="B")
        r=compatibility(a,b)
        self.assertGreaterEqual(r["total"],80)
        self.assertEqual(r["level"],"Excellent")
    def test_very_different_low(self):
        a=make()
        b=make(city="Mumbai",preferred_area="Andheri",budget_min=30000,budget_max=40000,food_pref="non-veg",smoking="yes",drinking="yes",cleanliness=1,sleep_schedule="night_owl",guests_freq="often",noise_tolerance="low",pets_ok=False)
        r=compatibility(a,b)
        self.assertLess(r["total"],50)
    def test_no_budget_overlap(self):
        a=make(budget_min=5000,budget_max=8000); b=make(budget_min=20000,budget_max=30000)
        r=compatibility(a,b)
        budget=[x for x in r["breakdown"] if x["factor"]=="Budget Overlap"][0]
        self.assertEqual(budget["score"],0)
    def test_breakdown_sums(self):
        a=make(name="A"); b=make(name="B",cleanliness=3)
        r=compatibility(a,b)
        self.assertEqual(sum(x["score"] for x in r["breakdown"]), r["total"])
        self.assertEqual(sum(x["max"] for x in r["breakdown"]), 100)
    def test_pages(self):
        from django.test import Client
        c = Client()
        for url in ["/", "/profiles/", "/rooms/", "/matches/", "/calculator/", "/interests/", "/login/", "/register/", "/profiles/create/", "/rooms/create/"]:
            self.assertEqual(c.get(url).status_code, 200, url)
