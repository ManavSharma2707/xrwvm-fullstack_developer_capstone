# Submission Guide

**GitHub repo:** https://github.com/ManavSharma2707/xrwvm-fullstack_developer_capstone
**GitHub Actions (green, `main`):** https://github.com/ManavSharma2707/xrwvm-fullstack_developer_capstone/actions/runs/40885761159
**Live deployment URL:** _PENDING: no host chosen yet (see "Still pending")_

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
| 8. `/fetchReviews/dealer/29` | PARTIAL | `task08_fetchReviews_dealer29.txt` |
| 9. `/fetchDealers` | PARTIAL | `task09_fetchDealers.txt` |
| 10. `/fetchDealer/3` | PARTIAL | `task10_fetchDealer3.txt` |
| 11. `/fetchDealers/Kansas` | PARTIAL | `task11_fetchDealers_Kansas.txt` |
| 12. Admin login | PASS | `task12_admin_login_page.png`, `task12_admin_logged_in.png`, `task12-13_admin_login_logout.txt` |
| 13. Admin logout | PASS | `task13_admin_logged_out.png` |
| 14. Car makes | PASS | `task14-15_get_cars.txt` (12 makes) |
| 15. Car models | PASS | `task14-15_get_cars.txt` (CarMake/CarModel pairs), `task15_admin_carmodels.png` |
| 16. Sentiment analyzer | PARTIAL | `task16_sentiment_local.txt`: `/analyze/Fantastic services` → positive (local). **Deployed URL pending.** |
| 17. Dealers, pre-login | PASS | `task17_dealers_anonymous.png` |
| 18. Dealers, post-login | PASS | `task18_dealers_logged_in.png` (username in navbar + Review Dealer column) |
| 19. State filter | PASS | `task19_dealers_filtered_kansas.png` |
| 20. Dealer details | PASS | `task20_dealer_details.png` |
| 21. Add-review form | PASS | `task21_post_review_form.png` |
| 22. Review submitted | PASS | `task22_review_submitted.png` (new review on top, positive icon) |
| 23. GitHub Actions green | PASS | `task23_github_actions.txt` + run URL above (flake8, JSHint, frontend lint+build all green) |
| 24. Deploy | PENDING | needs a host (see below) |
| 25. Live landing page | PENDING | after deploy |
| 26. Live login shows username | PENDING | after deploy (local equivalent: `task26_home_logged_in.png`) |
| 27. Live dealer details | PENDING | after deploy (local equivalent: `task20_dealer_details.png`) |
| 28. Live new review | PENDING | after deploy (local equivalent: `task22_review_submitted.png`) |

## Honest notes on the PARTIAL items

* **Tasks 8-11 (Express API):** the code is complete and each endpoint returns correct data, but I ran the API against an
  **in-memory MongoDB**, not `docker-compose up`, because the Docker daemon was not running and I was not able to start Docker Desktop.
  Once Docker is running, regenerate the evidence the way the course expects:
  ```bash
  cd server/database
  docker-compose up -d --build
  curl localhost:3030/fetchReviews/dealer/29
  curl localhost:3030/fetchDealers
  curl localhost:3030/fetchDealer/3
  curl localhost:3030/fetchDealers/Kansas
  ```
  and screenshot those URLs in your browser if the grader asks for screenshots.
* **Task 16:** the analyzer runs and returns the right answers locally. The task asks for a deployed URL.
* **Docker image (`server/Dockerfile`, `entrypoint.sh`) and `server/database/Dockerfile`:** written but **never built or run** (no Docker daemon).
  What I did verify without Docker: the same steps the entrypoint runs (`migrate`, `collectstatic`, serving the app with `DEBUG=False` and a real
  `SECRET_KEY`) all work, and the React build succeeds in GitHub Actions. Gunicorn itself could not be run on Windows.
* **Kubernetes:** `server/deployment.yaml` is written. `kubectl apply --dry-run=client` needs a cluster to talk to, so it could not run here;
  I validated structure with PyYAML instead (`task_k8s_validation.txt`). Run the real dry run yourself if you have a cluster.

## Still pending (needs you)

1. **Start Docker Desktop**, then run the commands above, plus
   `cd server && docker build -t dealership . && docker run -p 8000:8000 -e SECRET_KEY=<any-long-string> -e DEBUG=False -e ALLOWED_HOSTS=localhost dealership`.
2. **Choose a deployment host** (Render, IBM Cloud Code Engine, Railway, Fly.io...). You do the login/token steps. Three things must be deployed:
   * Django app (`server/`, uses `server/Dockerfile`), env vars: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `backend_url`, `sentiment_analyzer_url`
   * Sentiment analyzer (`server/djangoapp/microservices/`, has its own Dockerfile, honours `$PORT`)
   * Express API (`server/database/`) plus a hosted MongoDB (e.g. a free MongoDB Atlas cluster); set `MONGO_URL` on the API service
   After that, give me the URLs and I will verify Tasks 16 and 24-28 and take the screenshots.
3. **Replace placeholder content** on About/Contact (team names, emails, address) with your own if you want. They are clearly fictional (`example.com`).

## Things worth knowing when you explain the project

* The Django `root` superuser exists only in your local `db.sqlite3` (git-ignored). Its password is not stored anywhere in the repo.
  A deployed instance starts with an empty database, so create a superuser there too if you need admin access.
* `add_review` takes the author's name and user id from the logged-in session (not from the browser) and stamps the time on the server.
* Deviations from the starter: React pages use relative URLs (the starter's `href.indexOf("dealer")` trick breaks on hostnames containing "dealer");
  `CsrfViewMiddleware` was added; the `.env` file is no longer committed (use `server/.env.example`);
  JSHint covers the Express JS only, because JSHint cannot parse JSX, so the React code is checked with ESLint in CI instead.
