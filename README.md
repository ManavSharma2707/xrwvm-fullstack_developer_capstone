# Dealerships Review Portal

A national car-dealership review portal. Visitors browse dealerships by state,
read customer reviews (each tagged with an automatic sentiment), and registered
users can post their own reviews.

Built as the IBM Full-Stack Developer capstone: **Django + React + Express/MongoDB + a Flask sentiment microservice**, with CI on GitHub Actions and Docker/Kubernetes packaging.

## Tech stack

| Layer | Technology |
|---|---|
| Web app / auth / admin | Django, SQLite (dev), Gunicorn, WhiteNoise |
| Front end | React 18, React Router 6, Bootstrap 5 |
| Dealer & review data | Node.js, Express, Mongoose, MongoDB (Docker Compose) |
| Sentiment analysis | Flask + NLTK VADER (separate microservice) |
| CI | GitHub Actions: flake8 (Python), JSHint (JavaScript) |
| Packaging | Docker, Kubernetes (`deployment.yaml`) |

## Architecture

```
 Browser ──► Django :8000 ──┬──► Express API :3030 ──► MongoDB   (dealers, reviews)
 (React SPA   (auth, admin, │
  served by    proxy views, └──► Flask sentiment :5050            (VADER)
  Django)      CarMake/CarModel)
```

* **Django** (`server/`): authentication (login/logout/register), the admin
  site, `CarMake`/`CarModel` models, proxy views that call the other services,
  and it serves the compiled React app plus the static About/Contact pages.
* **React** (`server/frontend`): Login, Register, Dealers, Dealer, PostReview.
* **Express + MongoDB** (`server/database`): REST API over `dealerships.json`
  and `reviews.json`, seeded on start-up.
* **Sentiment analyzer** (`server/djangoapp/microservices`): `GET /analyze/<text>`
  returns `{"sentiment": "positive|neutral|negative"}`.

## Repository layout

```
server/
  djangoproj/            Django settings, root URLs
  djangoapp/             models, views, urls, restapis.py, populate.py
    microservices/       Flask sentiment analyzer (+ Dockerfile)
  frontend/              React source (src/) and static pages (static/)
  database/              Express + Mongoose API (+ Dockerfile, docker-compose.yml)
  Dockerfile, entrypoint.sh, deployment.yaml
.github/workflows/main.yml   lint CI
evidence/                    grading evidence and SUBMISSION_GUIDE.md
```

## Local setup

Prerequisites: Python 3.10+, Node 18+, Docker (for MongoDB).

```bash
# 1. Python environment
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r server/requirements.txt
cp server/.env.example server/.env  # then edit values

# 2. Database
cd server
python manage.py migrate
python manage.py createsuperuser    # use your own username/password
python manage.py shell -c "from djangoapp.populate import initiate; initiate()"

# 3. Front end
cd frontend && npm install && npm run build && cd ..

# 4. Express + MongoDB (needs Docker running)
cd database
docker build . -t nodeapp
docker-compose up -d
cd ..

# 5. Sentiment analyzer (see server/djangoapp/microservices/sentiment/readme.md for NLTK data)
cd djangoapp/microservices && pip install -r requirements.txt && flask --app app run --port 5050 &
cd ../..

# 6. Django
python manage.py runserver          # http://localhost:8000
```

### Environment variables (`server/.env`)

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key (required in production) |
| `DEBUG` | `True` for local dev, **`False` in deployment** |
| `ALLOWED_HOSTS` | comma-separated hostnames |
| `CSRF_TRUSTED_ORIGINS` | comma-separated origins, e.g. `https://my-app.example.com` |
| `backend_url` | Express API base URL |
| `sentiment_analyzer_url` | sentiment service base URL (trailing `/`) |

## Endpoints

**Pages:** `/` · `/about` · `/contact` · `/login/` · `/register/` · `/dealers/` · `/dealer/<id>` · `/postreview/<id>` · `/admin/`

**Django API (`/djangoapp/...`):**

| Method | Path | Description |
|---|---|---|
| POST | `login` | `{"userName","password"}` → `{"userName","status":"Authenticated"}` |
| GET | `logout` | ends session → `{"userName":""}` |
| POST | `register` | create user and log in |
| GET | `get_cars` | `{"CarModels":[{"CarModel","CarMake"}]}` |
| GET | `get_dealers`, `get_dealers/<state>` | list / filter dealers |
| GET | `dealer/<id>` | one dealer |
| GET | `reviews/dealer/<id>` | reviews with `sentiment` |
| POST | `add_review` | login required |

**Express API (port 3030):** `GET /fetchDealers` · `/fetchDealers/<state>` · `/fetchDealer/<id>` · `/fetchReviews` · `/fetchReviews/dealer/<id>` · `POST /insert_review`

**Sentiment (port 5050):** `GET /analyze/<text>`

## Continuous integration

`.github/workflows/main.yml` runs on every push / PR to `main`: **flake8** over
`server/` and **JSHint** over the Express and React JavaScript.

## Docker & Kubernetes

```bash
cd server
docker build -t <registry>/<user>/dealership:latest .
docker push  <registry>/<user>/dealership:latest
# edit the image name in deployment.yaml, then:
kubectl apply -f deployment.yaml
```

The image's entrypoint runs `migrate`, `collectstatic`, then Gunicorn on port 8000.

## Deployment notes

Set these environment variables on the host: `SECRET_KEY`, `DEBUG=False`,
`ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `backend_url`, `sentiment_analyzer_url`.
The Express/Mongo API and the sentiment analyzer are deployed as separate
services and referenced by URL.

## Screenshots

Screenshots are collected in [`evidence/`](evidence/).
