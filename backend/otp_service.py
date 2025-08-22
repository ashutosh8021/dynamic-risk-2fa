import random
import time
import os
from smtplib import SMTP

OTP_STORE = {}  # in-memory store for demo {username: {'otp': '123456', 'ts': 1234567890}}


def gen_otp():
    return '{:06d}'.format(random.randint(0, 999999))


def send_email_otp(email, otp):
    """
    Demo: if SMTP_HOST is configured, try to send via SMTP.
    Otherwise print OTP to console (development fallback).
    """
    smtp_host = os.environ.get('SMTP_HOST')
    smtp_port = int(os.environ.get('SMTP_PORT', 25))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')

    if smtp_host:
        try:
            with SMTP(smtp_host, smtp_port) as smtp:
                # optional TLS/login if creds provided
                if smtp_user and smtp_pass:
                    try:
                        smtp.starttls()
                        smtp.login(smtp_user, smtp_pass)
                    except Exception:
                        pass
                msg = f"Subject: Your OTP\n\nYour OTP is {otp}"
                smtp.sendmail('noreply@example.com', email, msg)
        except Exception as e:
            # fallback to console printing but log the error in dev
            print(f"SMTP send failed ({e}), falling back to console display. OTP: {otp}")
    else:
        # dev fallback: print OTP to backend console
        print(f"DEBUG: OTP for {email}: {otp}")


def create_and_send_otp(username, email):
    otp = gen_otp()
    OTP_STORE[username] = {'otp': otp, 'ts': time.time()}
    if email:
        send_email_otp(email, otp)
    return otp


def verify_otp(username, otp, expiry_seconds=300):
    rec = OTP_STORE.get(username)
    if not rec:
        return False
    if time.time() - rec['ts'] > expiry_seconds:
        del OTP_STORE[username]
        return False
    ok = rec['otp'] == str(otp)
    if ok:
        del OTP_STORE[username]
    return ok
