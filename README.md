# AI-Based Roommate Finder

## Overview
A complete, runnable Django project that helps people find compatible roommates using an **explainable AI matching engine**. Users can browse seeker profiles and room listings, explore ranked matches, calculate compatibility between any two people, and send / accept interests to connect.

## Features
- Dashboard with stats (total seekers, total rooms, cities, average rent), seekers-by-city and average-rent-by-city charts (CSS bars + Chart.js CDN available), top compatible matches, recent rooms
- Roommate profiles with lifestyle details (food, habits, cleanliness, sleep, work, guests, noise, pets)
- Room listings with filters
- Explainable AI matching (0-100 score with per-factor breakdown and reasons)
- Match Explorer — ranked matches for a chosen profile
- Compatibility Calculator — detailed breakdown for any two profiles
- Profiles & Rooms pages with filters
- Interest / Connect system (pending / accepted / rejected); contact details shown only after interest is accepted
- Create Profile & Create Room forms
- Login / Logout / Register, Django Admin
- Seed data: 18 diverse profiles across 6 cities, 10 rooms, sample interests

## Tech Stack
- Python, Django 5.1, SQLite, Bootstrap 5 (CDN), HTML/CSS
- No external API keys needed. Works offline after `pip install` (Bootstrap/Chart.js CDN needs internet for styling, app logic works offline).

## How AI Scoring Works (Explainable, Rule-Based)
| Factor | Max |
|---|---|
| Budget Overlap | 20 |
| City / Area | 15 |
| Food Preference | 10 |
| Smoking + Drinking Habits | 15 |
| Cleanliness | 15 |
| Sleep Schedule | 10 |
| Guests + Noise | 10 |
| Pets | 5 |
| **Total** | **100** |

Levels: >=80 Excellent, >=65 Good, >=50 Moderate, else Low. Each factor returns a score + a human-readable reason.

## Run in VS Code (Steps)
```bash
# 1. Open this folder in VS Code, open terminal
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 2. Install
pip install -r requirements.txt

# 3. Setup database + demo data
python manage.py migrate
python manage.py seed_data

# 4. Run
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Demo Login
- Username: `admin`
- Password: `admin123`
- Admin panel: http://127.0.0.1:8000/admin/

## Pages
- `/` Dashboard
- `/profiles/` Profiles (filters: city, gender, max budget, food)
- `/profiles/create/` Create Profile
- `/profiles/<id>/` Profile Detail + best matches + send interest
- `/rooms/` Rooms (filters: city, max rent, room type)
- `/rooms/create/` Create Room
- `/rooms/<id>/` Room Detail
- `/matches/` Match Explorer
- `/calculator/` Compatibility Calculator
- `/interests/` Interests (send, accept, reject)
- `/login/`, `/register/`, `/admin/`

## Tests
```bash
python manage.py test
```

## Future Scope — What is NOT Included
- No real trained ML model — scoring is an explainable rule-based AI engine, not trained ML
- No live chat / messaging system
- No payments
- No maps API / location maps
- No identity verification (Aadhaar / ID check)
- No live external APIs

These can be added later as future scope.
