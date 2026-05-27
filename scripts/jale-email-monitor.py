"""
Jale Email Monitor — GitHub ve onemli mailleri takip eder.
IMAP ile okur, kategorize eder, Telegram bildirimi gonderir.
"""
import imaplib
import email
import json
import os
import re
import urllib.request
from datetime import datetime, timedelta
from email.header import decode_header

IMAP_SERVER = os.environ.get("IMAP_SERVER", "")
IMAP_PORT = int(os.environ.get("IMAP_PORT", "993"))
IMAP_USER = os.environ.get("IMAP_USER", "")
IMAP_PASS = os.environ.get("IMAP_PASS", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_ALLOWED_USERS", "")
REPORT_FILE = os.environ.get("HERMES_HOME", "/opt/data") + "/email-report.json"

CATEGORIES = {
    "github_pr": ["pull request", "review requested", "merged"],
    "github_issue": ["assigned", "issue opened", "closed"],
    "github_ci": ["build succeeded", "build failed", "deployment", "ci/"],
    "github_security": ["security alert", "vulnerability", "dependabot"],
    "github_general": ["github.com", "github.comnoreply"],
}

PRIORITY_KEYWORDS = {
    "acil": ["security alert", "vulnerability", "build failed", "critical"],
    "bugun": ["review requested", "assigned", "pull request"],
    "bilgi": ["merged", "build succeeded", "deployment successful"],
}


def decode_str(s):
    if s is None:
        return ""
    decoded = decode_header(s)
    result = []
    for part, charset in decoded:
        if isinstance(part, bytes):
            result.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def categorize_email(subject, from_addr):
    subject_lower = subject.lower()
    from_lower = from_addr.lower()
    text = subject_lower + " " + from_lower

    for cat, keywords in CATEGORIES.items():
        if any(kw in text for kw in keywords):
            return cat
    return "other"


def get_priority(subject):
    subject_lower = subject.lower()
    for priority, keywords in PRIORITY_KEYWORDS.items():
        if any(kw in subject_lower for kw in keywords):
            return priority
    return "bilgi"


def check_emails(hours=24):
    if not all([IMAP_SERVER, IMAP_USER, IMAP_PASS]):
        return {"error": "IMAP bilgileri eksik", "emails": [], "summary": {}}

    mails = []
    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(IMAP_USER, IMAP_PASS)
        imap.select("INBOX")

        since = (datetime.now() - timedelta(hours=hours)).strftime("%d-%b-%Y")
        _, msg_ids = imap.search(None, f'(SINCE "{since}")')

        for msg_id in msg_ids[0].split()[-50:]:
            _, msg_data = imap.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
            for part in msg_data:
                if isinstance(part, tuple):
                    msg = email.message_from_bytes(part[1])
                    subject = decode_str(msg.get("Subject"))
                    from_addr = decode_str(msg.get("From"))
                    category = categorize_email(subject, from_addr)
                    priority = get_priority(subject)

                    mails.append({
                        "subject": subject,
                        "from": from_addr,
                        "date": msg.get("Date", ""),
                        "category": category,
                        "priority": priority,
                    })

        imap.logout()
    except Exception as e:
        return {"error": str(e), "emails": [], "summary": {}}

    github_mails = [m for m in mails if m["category"].startswith("github_")]
    summary = {
        "total": len(mails),
        "github": len(github_mails),
        "acil": len([m for m in mails if m["priority"] == "acil"]),
        "bugun": len([m for m in mails if m["priority"] == "bugun"]),
        "bilgi": len([m for m in mails if m["priority"] == "bilgi"]),
        "categories": {},
    }
    for m in mails:
        cat = m["category"]
        summary["categories"][cat] = summary["categories"].get(cat, 0) + 1

    return {"emails": mails, "summary": summary, "timestamp": datetime.now().isoformat()}


def send_telegram(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    chat_ids = TELEGRAM_CHAT_ID.split(",")
    for chat_id in chat_ids:
        url = (
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            f"?chat_id={chat_id}&text={urllib.parse.quote(text)}&parse_mode=HTML"
        )
        try:
            urllib.request.urlopen(url, timeout=10)
        except Exception:
            pass


def format_report(result):
    if "error" in result:
        return f"Email HATA: {result['error']}"

    s = result["summary"]
    lines = [
        f"<b>Jale Email Raporu</b>",
        f"Toplam: {s['total']} | GitHub: {s['github']}",
        f"Acil: {s['acil']} | Bugun: {s['bugun']} | Bilgi: {s['bilgi']}",
        "",
    ]

    acil_mails = [m for m in result["emails"] if m["priority"] == "acil"]
    if acil_mails:
        lines.append("<b>ACIL:</b>")
        for m in acil_mails[:5]:
            lines.append(f"- {m['subject'][:60]}")

    bugun_mails = [m for m in result["emails"] if m["priority"] == "bugun"]
    if bugun_mails:
        lines.append("<b>BUGUN:</b>")
        for m in bugun_mails[:5]:
            lines.append(f"- {m['subject'][:60]}")

    return "\n".join(lines)


def main():
    result = check_emails(hours=24)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    if "error" not in result and result["summary"]["github"] > 0:
        report = format_report(result)
        send_telegram(report)
        print(f"Email raporu gonderildi: {result['summary']['github']} GitHub maili")
    elif "error" in result:
        print(f"HATA: {result['error']}")
    else:
        print("GitHub maili yok, bildirim atlandi")


if __name__ == "__main__":
    import urllib.parse
    main()
