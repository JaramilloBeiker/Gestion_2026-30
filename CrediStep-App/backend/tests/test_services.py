from app.services import diagnostic, simulators
from app.services.assistant import answer

BASE = {
    "situacion": "estudiante", "productos": ["cuenta_ahorros"], "gastos": "aveces",
    "ahorro": "poco", "conocimiento": 2, "pagos": "siempre", "meta": "primera_tarjeta",
}


def test_diagnostic_scoring_and_level():
    out = diagnostic.evaluate(BASE)
    assert out.score == 10 + 10 + 7 + 5 + 25
    assert out.level == "En construcción"
    assert "Tienes cuenta bancaria" in out.strengths
    assert "No tienes historial crediticio todavía" in out.improvements
    assert not out.has_credit
    assert out.segment == "universitario"


def test_diagnostic_max_score():
    out = diagnostic.evaluate({**BASE, "productos": ["cuenta_ahorros", "tarjeta_credito"],
                               "gastos": "registro", "ahorro": "si", "conocimiento": 5})
    assert out.score == 100 and out.level == "Listo para avanzar" and out.has_credit


def test_diagnostic_validation():
    assert diagnostic.validate_answers(BASE) == []
    assert diagnostic.validate_answers({**BASE, "conocimiento": 9})
    assert diagnostic.validate_answers({**BASE, "gastos": "x"})
    assert diagnostic.validate_answers({k: v for k, v in BASE.items() if k != "meta"})


def test_monthly_rate_conversion():
    assert abs(simulators.monthly_rate_from_ea(26.824) - 0.02) < 1e-4


def test_loan_cost_matches_lesson_example():
    r = simulators.loan_cost(1_500_000, 28, 12)
    assert 1_690_000 < r["total_paid"] < 1_720_000
    r36 = simulators.loan_cost(1_500_000, 28, 36)
    assert r36["total_paid"] > 2_100_000
    assert r36["schedule"][-1]["balance"] == 0


def test_utilization_bands():
    assert simulators.card_utilization(1_000_000, 200_000)["status"] == "good"
    assert simulators.card_utilization(1_000_000, 500_000)["status"] == "warning"
    assert simulators.card_utilization(1_000_000, 900_000)["status"] == "danger"


def test_late_payment_permanence_capped():
    assert simulators.late_payment(100_000, 90, 28)["negative_record_months"] == 6
    assert simulators.late_payment(100_000, 900, 28)["negative_record_months"] == 48
    assert simulators.late_payment(100_000, 0, 28)["late_interest"] == 0


def test_score_estimate():
    no_history = simulators.estimate_score(100, 0, 0, 0, 0)
    assert no_history["score"] is None
    good = simulators.estimate_score(100, 10, 84, 0, 3)
    bad = simulators.estimate_score(60, 95, 6, 6, 1)
    assert 150 <= bad["score"] < good["score"] <= 950


def test_assistant():
    assert answer("¿Qué pasa si me atraso en un pago?")["lesson"] == "si-me-atraso"
    assert answer("cuanto cupo debo usar de mi tarjeta")["lesson"] == "manejo-del-cupo"
    assert answer("xyz qwerty")["confidence"] == 0
