from flask import Flask, render_template, request, redirect, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread, Event
from datetime import datetime
import pandas as pd
import random, time, os, csv, json, math

# ================= CONFIG =================
CHROMEDRIVER_PATH = r"C:\Windows\chromedriver.exe"
USER_DATA_DIR = r"E:\Business client project\Whatsapp excel bulk project Web base\WhatsappWebApp\whatsapp_selenium_profile"

STATE_FILE = "state.json"
LOG_FILE = "send_report.csv"

app = Flask(__name__)
pause_event = Event()
pause_event.set()

driver = None
wait = None

# ================= STATE =================
def default_state():
    return {
        "total": 0,
        "sent": 0,
        "failed": 0,
        "current": 0,
        "status": "Idle"
    }

def load_state():
    if not os.path.exists(STATE_FILE):
        return default_state()
    with open(STATE_FILE) as f:
        return json.load(f)

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)

state = load_state()

# ================= UTIL =================
def rdelay(a, b):
    time.sleep(random.uniform(a, b))

def log_csv(number, message, status, reason=""):
    exists = os.path.exists(LOG_FILE)
    now = datetime.now()
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["date","time","number","message","status","reason"])
        w.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            number, message, status, reason
        ])

# ================= BROWSER =================
def start_browser():
    global driver, wait
    if driver is None:
        opt = Options()
        opt.add_argument(f"--user-data-dir={USER_DATA_DIR}")
        opt.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=Service(CHROMEDRIVER_PATH),
            options=opt
        )
        wait = WebDriverWait(driver, 60)

# ================= SEND MESSAGE =================
def send_message(number, message, delays):
    try:
        driver.get(f"https://web.whatsapp.com/send?phone=91{number}")
        rdelay(*delays["open"])

        if "Phone number shared via url is invalid" in driver.page_source:
            raise Exception("Invalid WhatsApp number")

        box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
        ))

        for ch in message:
            box.send_keys(ch)
            time.sleep(random.uniform(0.03, 0.08))

        rdelay(*delays["type"])
        box.send_keys(Keys.ENTER)
        rdelay(*delays["send"])

        state["sent"] += 1
        log_csv(number, message, "SUCCESS")

    except Exception as e:
        state["failed"] += 1
        log_csv(number, message, "FAILED", str(e))

    state["current"] += 1
    save_state(state)

# ================= WORKER =================
def bulk_worker(df, fallback_msgs, delays, batch_size):
    state.clear()
    state.update(default_state())
    state["total"] = len(df)
    state["status"] = "Running"
    save_state(state)

    if df.empty:
        state["status"] = "Aborted: No data"
        save_state(state)
        return

    has_excel_msg = "message" in df.columns and df["message"].notna().any()
    if not has_excel_msg and not fallback_msgs:
        state["status"] = "Aborted: No messages"
        save_state(state)
        return

    msg_i = 0
    batches = math.ceil(len(df) / batch_size)

    for b in range(batches):
        batch_df = df.iloc[b*batch_size:(b+1)*batch_size]

        for _, row in batch_df.iterrows():
            pause_event.wait()

            number = str(row["number"]).strip()
            name = str(row.get("name","")).strip()

            if has_excel_msg and str(row.get("message","")).strip():
                msg = str(row["message"])
            else:
                msg = fallback_msgs[msg_i]
                msg_i = (msg_i + 1) % len(fallback_msgs)

            msg = msg.replace("{name}", name)
            send_message(number, msg, delays)
            rdelay(*delays["next"])

        if b < batches - 1:
            rdelay(*delays["batch"])

    state["status"] = "Completed"
    save_state(state)

# ================= ROUTES =================
@app.route("/")
def home():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", s=load_state())

@app.route("/progress")
def progress():
    return jsonify(load_state())

@app.route("/pause")
def pause():
    pause_event.clear()
    state["status"] = "Paused"
    save_state(state)
    return "paused"

@app.route("/resume")
def resume():
    pause_event.set()
    state["status"] = "Running"
    save_state(state)
    return "resumed"

@app.route("/excel-info", methods=["POST"])
def excel_info():
    df = pd.read_excel(request.files["excel"])
    return jsonify({"rows": len(df)})

@app.route("/bulk", methods=["GET","POST"])
def bulk():
    if request.method == "POST":
        df = pd.read_excel(request.files["excel"])
        df.columns = df.columns.str.lower().str.strip()

        start = int(request.form.get("start_row", 1)) - 1
        end_raw = request.form.get("end_row")
        end = int(end_raw) if end_raw else None
        df = df.iloc[start:end]

        batch_size = int(request.form.get("batch_size", 30))

        fallback_msgs = [
            request.form.get(f"msg{i}","").strip()
            for i in range(1,6)
            if request.form.get(f"msg{i}","").strip()
        ]

        delays = {
            "open": (int(request.form["open_min"]), int(request.form["open_max"])),
            "type": (int(request.form["type_min"]), int(request.form["type_max"])),
            "send": (int(request.form["send_min"]), int(request.form["send_max"])),
            "next": (int(request.form["next_min"]), int(request.form["next_max"])),
            "batch": (int(request.form["batch_min"]), int(request.form["batch_max"]))
        }

        Thread(
            target=bulk_worker,
            args=(df, fallback_msgs, delays, batch_size),
            daemon=True
        ).start()

    return render_template("bulk.html")

@app.route("/history")
def history():
    rows = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            rows = list(csv.reader(f))[1:]
    return render_template("history.html", rows=rows)

# ================= START =================
if __name__ == "__main__":
    start_browser()
    app.run(debug=False, use_reloader=False)
