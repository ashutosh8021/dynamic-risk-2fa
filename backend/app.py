from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from risk_engine import compute_features_for_user, map_score_to_level, RiskEngine
from otp_service import create_and_send_otp, verify_otp
from db import SimpleUserDB

app = FastAPI()
user_db = SimpleUserDB()

# Using rules-only by default. Change to use_ml=True after training and saving risk_clf.joblib.
engine = RiskEngine(use_ml=False)


class LoginAttempt(BaseModel):
    username: str
    password: str
    ip: str
    user_agent: str
    lat: float
    lon: float
    timestamp: float


@app.post('/login')
def login(attempt: LoginAttempt):
    # 1) verify user credentials (demo)
    user = user_db.get_user(attempt.username)
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')
    if attempt.password != user['password']:
        user_db.increment_failed(attempt.username)
        raise HTTPException(status_code=401, detail='bad credentials')

    # 2) compute features from attempt + user history
    features = compute_features_for_user(user, attempt)

    # 3) compute risk score and reasons
    score, reasons = engine.score(features)
    level = map_score_to_level(score)

    # Low risk => success and mark known IP/device
    if level == 'low':
        # add IP/device to known lists (cap growth in production)
        known_ips = user.get('known_ips', [])
        if attempt.ip not in known_ips:
            known_ips.append(attempt.ip)
            user['known_ips'] = known_ips
        known_devices = user.get('known_devices', [])
        if attempt.user_agent not in known_devices:
            known_devices.append(attempt.user_agent)
            user['known_devices'] = known_devices
        user_db.reset_failed(attempt.username)
        user_db.save()
        return {
            'risk_level': 'low',
            'next_action': 'success',
            'explain': {'score': score, 'reasons': reasons}
        }

    # Medium risk => send OTP
    if level == 'medium':
        create_and_send_otp(attempt.username, user.get('email'))
        return {
            'risk_level': 'medium',
            'next_action': 'send_otp',
            'explain': {'score': score, 'reasons': reasons}
        }

    # High risk => manual review (demo)
    return {
        'risk_level': 'high',
        'next_action': 'manual_review',
        'explain': {'score': score, 'reasons': reasons}
    }


class OTPVerify(BaseModel):
    username: str
    otp: str


@app.post('/verify_otp')
def verify(otp_payload: OTPVerify):
    ok = verify_otp(otp_payload.username, otp_payload.otp)
    if not ok:
        raise HTTPException(status_code=401, detail='invalid or expired otp')
    # In production issue a signed session token here
    return {'status': 'ok', 'message': 'authenticated'}


@app.post('/create_demo_user')
def create_demo():
    # creates a demo user for testing
    user_db.create_user('alice', 'demo-password', 'alice@example.com', lat=12.9716, lon=77.5946)
    return {'status': 'created'}


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
