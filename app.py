import os
from datetime import date, timedelta
from flask import Flask, jsonify, send_from_directory
from flask_httpauth import HTTPBasicAuth
import hmac
from garmin_personal_api import GarminPersonalApiClient, PersonalApiAuthenticator, resolve_api_key

app = Flask(__name__, static_folder="static", static_url_path="/static")
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    expected_user = os.environ.get("DASHBOARD_USER", "garmin")
    expected_password = os.environ.get("DASHBOARD_PASSWORD", "")
    if not expected_password:
        return None
    if hmac.compare_digest(username or "", expected_user) and hmac.compare_digest(password or "", expected_password):
        return username
    return None

def get_client():
    key = os.environ.get("GARMIN_PERSONAL_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GARMIN_PERSONAL_API_KEY ist auf dem Server noch nicht gesetzt.")
    auth = PersonalApiAuthenticator()
    token = auth.obtain_token(key)
    # The API client uses the short-lived token for this request.
    return auth, GarminPersonalApiClient(token.access_token)

def safe_call(client, name, *args, **kwargs):
    try:
        return getattr(client, name)(*args, **kwargs)
    except Exception as exc:
        return {"_error": f"{name}: {type(exc).__name__}: {str(exc)[:220]}"}

@app.get("/")
@auth.login_required
def home():
    return send_from_directory("static", "index.html")

@app.get("/manifest.json")
@auth.login_required
def manifest():
    return send_from_directory("static", "manifest.json")

@app.get("/sw.js")
@auth.login_required
def service_worker():
    return send_from_directory("static", "sw.js")

@app.get("/api/health")
@auth.login_required
def health():
    return jsonify({"ok": True, "api_key_configured": bool(os.environ.get("GARMIN_PERSONAL_API_KEY", "").strip())})

@app.get("/api/dashboard")
@auth.login_required
def dashboard():
    start = (date.today() - timedelta(days=30)).isoformat()
    end = date.today().isoformat()
    try:
        auth, client = get_client()
        result = {
            "generated_at": date.today().isoformat(),
            "period": {"start": start, "end": end},
            "daily_summaries": safe_call(client, "get_daily_summaries", start, end),
            "steps": safe_call(client, "get_daily_steps", start, end),
            "weight": safe_call(client, "get_weight_measurements", start, end),
            "sleep": safe_call(client, "get_daily_sleep_summaries", start, end),
            "hrv": safe_call(client, "get_daily_hrv_summaries", start, end),
            "activities": safe_call(client, "search_activities", start_date=start, end_date=end, limit=20),
            "body_battery": safe_call(client, "get_daily_body_battery", start, end),
        }
        try:
            client.close()
        except Exception:
            pass
        try:
            auth.close()
        except Exception:
            pass
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": f"{type(exc).__name__}: {str(exc)[:300]}"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
