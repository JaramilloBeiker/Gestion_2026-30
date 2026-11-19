from datetime import date, timedelta

from .conftest import auth_headers

ANSWERS = {
    "situacion": "primer_empleo", "productos": ["ninguno"], "gastos": "no",
    "ahorro": "no", "conocimiento": 1, "pagos": "na", "meta": "primera_tarjeta",
}


def test_health(client):
    assert client.get("/api/health").json()["status"] == "ok"


def test_spa_fallback(client):
    r = client.get("/mi-plan")
    assert r.status_code == 200 and "<div id=\"app\"" in r.text
    assert client.get("/api/no-existe").status_code == 404


def test_auth_flow(client):
    r = client.post("/api/auth/register", json={"name": "Ana", "email": "ANA@Test.co", "password": "12345678"})
    assert r.status_code == 201
    assert r.json()["user"]["email"] == "ana@test.co"
    assert client.post("/api/auth/register", json={"name": "Ana", "email": "ana@test.co", "password": "12345678"}).status_code == 409
    assert client.post("/api/auth/login", json={"email": "ana@test.co", "password": "malaclave"}).status_code == 401
    token = client.post("/api/auth/login", json={"email": "ana@test.co", "password": "12345678"}).json()["token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).json()
    assert me["name"] == "Ana" and not me["is_premium"]
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer basura"}).status_code == 401


def test_institution_code_grants_plus(client):
    h = auth_headers(client, email="inst@test.co", institution_code="javeriana2026")
    me = client.get("/api/auth/me", headers=h).json()
    assert me["is_premium"] and me["premium_plan"] == "institucional"
    assert me["institution"] == "Pontificia Universidad Javeriana"
    bad = client.post("/api/auth/register", json={"name": "Xavi", "email": "x@test.co", "password": "12345678", "institution_code": "NOPE"})
    assert bad.status_code == 400


def test_diagnostic_and_personalized_plan(client, headers):
    assert client.get("/api/diagnostic/latest", headers=headers).status_code == 404
    assert len(client.get("/api/diagnostic/questions").json()) == 7
    r = client.post("/api/diagnostic", json={"answers": ANSWERS}, headers=headers)
    assert r.status_code == 201 and r.json()["level"] == "Primeros pasos"
    plan = client.get("/api/plan", headers=headers).json()
    assert len(plan["steps"]) == 5 and plan["completed"] == 0
    titles = [t["title"] for s in plan["steps"] for t in s["tasks"]]
    assert "Aprende a empezar tu historial desde cero" in titles
    assert "Domina el cupo de tu tarjeta" not in titles
    assert plan["next_task"]["title"] == "Registra tus gastos durante una semana"

    # Usuario con crédito ve tareas distintas y algunas autocompletadas
    h2 = auth_headers(client, email="concredito@test.co")
    client.post("/api/diagnostic", json={"answers": {**ANSWERS, "productos": ["cuenta_ahorros", "tarjeta_credito"], "gastos": "registro"}}, headers=h2)
    plan2 = client.get("/api/plan", headers=h2).json()
    titles2 = [t["title"] for s in plan2["steps"] for t in s["tasks"]]
    assert "Domina el cupo de tu tarjeta" in titles2
    assert plan2["completed"] == 2  # gastos registrados + cuenta de ahorros


def test_complete_task_and_lesson_tasks_protected(client, headers):
    client.post("/api/diagnostic", json={"answers": ANSWERS}, headers=headers)
    plan = client.get("/api/plan", headers=headers).json()
    manual = next(t for s in plan["steps"] for t in s["tasks"] if not t["lesson_slug"])
    lesson_task = next(t for s in plan["steps"] for t in s["tasks"] if t["lesson_slug"])
    after = client.post(f"/api/plan/tasks/{manual['id']}/complete", headers=headers).json()
    assert after["completed"] == 1
    assert client.post(f"/api/plan/tasks/{lesson_task['id']}/complete", headers=headers).status_code == 400
    again = client.delete(f"/api/plan/tasks/{manual['id']}/complete", headers=headers).json()
    assert again["completed"] == 0


def test_lesson_quiz_completes_plan_task(client, headers):
    client.post("/api/diagnostic", json={"answers": ANSWERS}, headers=headers)
    modules = client.get("/api/learning/modules", headers=headers).json()
    assert len(modules) == 4
    lesson = client.get("/api/learning/lessons/presupuesto-50-30-20", headers=headers).json()
    wrong = client.post("/api/learning/lessons/presupuesto-50-30-20/quiz", json={"answers": [0]}, headers=headers).json()
    assert not wrong["passed"] and wrong["xp_earned"] == 0
    ok = client.post("/api/learning/lessons/presupuesto-50-30-20/quiz", json={"answers": [2]}, headers=headers).json()
    assert ok["passed"] and ok["xp_earned"] == lesson["xp"] + 10
    plan = client.get("/api/plan", headers=headers).json()
    task = next(t for s in plan["steps"] for t in s["tasks"] if t["lesson_slug"] == "presupuesto-50-30-20")
    assert task["done"]
    # repetir no da XP otra vez
    assert client.post("/api/learning/lessons/presupuesto-50-30-20/quiz", json={"answers": [2]}, headers=headers).json()["xp_earned"] == 0


def test_premium_gating_and_activation(client, headers):
    assert client.get("/api/learning/lessons/estrategia-6-meses", headers=headers).status_code == 402
    score_in = {"on_time_pct": 100, "utilization_pct": 20, "history_months": 12, "inquiries_12m": 1, "product_types": 1}
    assert client.post("/api/simulators/score", json=score_in, headers=headers).status_code == 402
    loan = client.post("/api/simulators/loan", json={"amount": 1000000, "ea_rate": 28, "months": 12}, headers=headers).json()
    assert loan["schedule_truncated"] and len(loan["schedule"]) == 3
    assert client.post("/api/premium/activate", json={"plan": "mensual"}, headers=headers).status_code == 200
    assert client.post("/api/simulators/score", json=score_in, headers=headers).json()["score"] > 150
    loan = client.post("/api/simulators/loan", json={"amount": 1000000, "ea_rate": 28, "months": 12}, headers=headers).json()
    assert len(loan["schedule"]) == 12
    client.post("/api/premium/cancel", headers=headers)
    assert not client.get("/api/auth/me", headers=headers).json()["is_premium"]


def test_goals_limit_and_contributions(client, headers):
    g = client.post("/api/goals", json={"title": "Emergencia", "category": "emergencia", "target_amount": 500000}, headers=headers)
    assert g.status_code == 201
    gid = g.json()["id"]
    client.post("/api/goals", json={"title": "Viaje", "category": "viaje", "target_amount": 1000000}, headers=headers)
    assert client.post("/api/goals", json={"title": "Otra", "target_amount": 10}, headers=headers).status_code == 402
    r = client.post(f"/api/goals/{gid}/contribute", json={"amount": 250000}, headers=headers).json()
    assert r["pct"] == 50 and r["remaining"] == 250000
    other = auth_headers(client, email="otro@test.co")
    assert client.post(f"/api/goals/{gid}/contribute", json={"amount": 1}, headers=other).status_code == 404
    assert client.delete(f"/api/goals/{gid}", headers=headers).status_code == 204


def test_recurring_reminder_rolls_over(client, headers):
    due = date.today() + timedelta(days=2)
    r = client.post("/api/reminders", json={"title": "Pagar celular", "kind": "pago", "due_date": due.isoformat(), "recurrence": "monthly"}, headers=headers).json()
    assert r["status"] == "soon"
    t = client.post(f"/api/reminders/{r['id']}/toggle", headers=headers).json()
    assert t["reminder"]["done"] and t["next"]["due_date"] > due.isoformat()
    assert len(client.get("/api/reminders", headers=headers).json()) == 2


def test_dashboard(client, headers):
    client.post("/api/diagnostic", json={"answers": ANSWERS}, headers=headers)
    d = client.get("/api/dashboard", headers=headers).json()
    assert 0 <= d["readiness"]["index"] <= 100
    assert d["recommended"]["title"] and d["streak"] >= 1 and len(d["week"]) == 7


def test_demo_user_and_admin(client):
    demo = client.post("/api/auth/login", json={"email": "demo@credistep.co", "password": "CrediStep2026"})
    assert demo.status_code == 200
    h = {"Authorization": f"Bearer {demo.json()['token']}"}
    assert client.get("/api/admin/overview", headers=h).status_code == 403
    admin = client.post("/api/auth/login", json={"email": "admin@javeriana.edu.co", "password": "CrediStep2026"}).json()
    o = client.get("/api/admin/overview", headers={"Authorization": f"Bearer {admin['token']}"}).json()
    assert o["students"] >= 25 and len(o["modules"]) == 4 and len(o["signups"]) == 8


def test_assistant_endpoint(client, headers):
    r = client.post("/api/assistant/ask", json={"question": "¿Cómo se calcula mi puntaje?"}, headers=headers).json()
    assert r["lesson"] == "como-funciona-puntaje"
    assert len(client.get("/api/glossary").json()) >= 15
