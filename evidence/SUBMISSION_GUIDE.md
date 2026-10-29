# Submission Guide

**GitHub repo:** https://github.com/ManavSharma2707/xrwvm-fullstack_developer_capstone
**GitHub Actions (green, `main`):** https://github.com/ManavSharma2707/xrwvm-fullstack_developer_capstone/actions/runs/40885761159
**Live deployment URL:** https://dealership-web-ffu4.onrender.com (Render free tier, first request after idle takes ~50s)

Other live services: API https://dealership-api-5tog.onrender.com , sentiment https://dealership-sentiment-qca6.onrender.com

Status key: PASS = run and observed working. PARTIAL = works but not in the exact setup the task asks for. PENDING = not done, needs you.

All screenshots in this folder were taken from a real run of the site in headless Edge
(full journey log: `e2e_run.txt`, 0 browser console errors). The local site runs at `http://localhost:8000`.

| Task | Status | Evidence / what to show |
|---|---|---|
| 1. README | PASS | `README.md` in the repo root |
| 2. runserver OK | PASS | `task02_runserver.txt` (migrate, check, runserver, HTTP 200s) |
| 3. About page | PASS | `task03_about.png` (URL `/about`; banner, nav, 4 team members) |
| 4. Contact page | PASS | `task04_contact.png` (URL `/contact`; banner, details, branch table) |
| 5. login endpoint | PASS | `task05_login_endpoint.txt` → `{"userName": "root", "status": "Authenticated"}` (password redacted) |
| 6. logout endpoint | PASS | `task06_logout_endpoint.txt` → `{"userName": ""}` |
| 7. Register.jsx | PASS | `task07_register_form.png` + code `server/frontend/src/components/Register/Register.jsx` |
| 8. `/fetchReviews/dealer/29` | PASS | `task08_fetchReviews_dealer29.txt` (run against the docker-compose stack) |
| 9. `/fetchDealers` | PASS | `task09_fetchDealers.txt` (run against the docker-compose stack) |
| 10. `/fetchDealer/3` | PASS | `task10_fetchDealer3.txt` (run against the docker-compose stack) |
| 11. `/fetchDealers/Kansas` | PASS | `task11_fetchDealers_Kansas.txt` (run against the docker-compose stack) |
| 12. Admin login | PASS | `task12_admin_login_page.png`, `task12_admin_logged_in.png`, `task12-13_admin_login_logout.txt` |
| 13. Admin logout | PASS | `task13_admin_logged_out.png` |
| 14. Car makes | PASS | `task14-15_get_cars.txt` (12 makes) |
| 15. Car models | PASS | `task14-15_get_cars.txt` (CarMake/CarModel pairs), `task15_admin_carmodels.png` |
| 16. Sentiment analyzer | PASS | `task16_sentiment_docker.txt` (Docker) and `task_live_checks.txt`: live `/analyze/Fantastic services` -> positive |
| 17. Dealers, pre-login | PASS | `task17_dealers_anonymous.png` |
| 18. Dealers, post-login | PASS | `task18_dealers_logged_in.png` (username in navbar + Review Dealer column) |
| 19. State filter | PASS | `task19_dealers_filtered_kansas.png` |
| 20. Dealer details | PASS | `task20_dealer_details.png` |
| 21. Add-review form | PASS | `task21_post_review_form.png` |
| 22. Review submitted | PASS | `task22_review_submitted.png` (new review on top, positive icon) |
| 23. GitHub Actions green | PASS | `task23_github_actions.txt` + run URL above (flake8, JSHint, frontend lint+build all green) |
| 24. Deploy | PASS | Render Blueprint (`render.yaml`), 3 services + MongoDB Atlas; `task_live_checks.txt` |
| 25. Live landing page | PASS | `live_run/task03_about.png`, `task_live_checks.txt` (about/landing load on the live URL) |
| 26. Live login shows username | PASS | `live_run/task26_home_logged_in.png` |
| 27. Live dealer details | PASS | `live_run/task20_dealer_details.png` |
| 28. Live new review | PASS | `live_run/task22_review_submitted.png` (sentiment icon positive) |

## What was verified in Docker

Docker Desktop was started and these were built and run for real (`task_docker_containers.txt`, `docker_run/` screenshots):

* `server/database`: `docker-compose up -d --build` runs the Express API + MongoDB 7.0. Tasks 8-11 evidence comes from this stack.
* `server/Dockerfile` (Django + React, multi-stage) built and ran with `DEBUG=False`; `entrypoint.sh` ran migrate, collectstatic and gunicorn.
* `server/djangoapp/microservices/Dockerfile` (sentiment analyzer) built and ran.
* The full browser journey (register, login, filter, dealer page, post review, admin login/logout) passed against these containers
  with 0 console errors: screenshots and log in `evidence/docker_run/`.

Bugs the Docker run found and fixed:
* On this Windows machine, git checks `entrypoint.sh` out with CRLF line endings (`core.autocrlf=true`), so an image built from the working
  tree could not start. (The blob stored in git was already LF, so builds from GitHub were not affected.) Fixed with `.gitattributes` (LF for
  `*.sh`, Dockerfiles, YAML) plus a `sed` guard in the Dockerfile.
* `POST /insert_review` hung when sent with `curl -d` (form content type). Fixed; invalid bodies now return HTTP 400.
* `mongo:latest` was pinned to `mongo:7.0` for reproducibility.

## Still partial / pending

* **Task 16 deployed URL and Tasks 24-28:** need a hosting choice (see below).
* **Kubernetes:** `server/deployment.yaml` is written and structurally validated (`task_k8s_validation.txt`), but `kubectl apply --dry-run=client`
  needs a reachable cluster. Enable Kubernetes in Docker Desktop (needs several GB of disk and RAM) and run it if you want that evidence.

## Still needs you

1. **Choose a deployment host** (Render, IBM Cloud Code Engine, Railway, Fly.io...). You do the login/token steps. Three things must be deployed:
   * Django app (`server/`, uses `server/Dockerfile`), env vars: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `backend_url`, `sentiment_analyzer_url`
   * Sentiment analyzer (`server/djangoapp/microservices/`, has its own Dockerfile, honours `$PORT`)
   * Express API (`server/database/`) plus a hosted MongoDB (e.g. a free MongoDB Atlas cluster); set `MONGO_URL` on the API service
   After that, give me the URLs and I will verify Tasks 16 and 24-28 and take the screenshots.
2. **Replace placeholder content** on About/Contact (team names, emails, address) with your own if you want. They are clearly fictional (`example.com`).

## Things worth knowing when you explain the project

* The Django `root` superuser exists only in your local `db.sqlite3` (git-ignored). Its password is not stored anywhere in the repo.
  A deployed instance starts with an empty database, so create a superuser there too if you need admin access.
* `add_review` takes the author's name and user id from the logged-in session (not from the browser) and stamps the time on the server.
* Deviations from the starter: React pages use relative URLs (the starter's `href.indexOf("dealer")` trick breaks on hostnames containing "dealer");
  `CsrfViewMiddleware` was added; the `.env` file is no longer committed (use `server/.env.example`);
  JSHint covers the Express JS only, because JSHint cannot parse JSX, so the React code is checked with ESLint in CI instead.
