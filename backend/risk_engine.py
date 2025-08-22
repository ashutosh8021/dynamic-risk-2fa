import joblib
import os

MODEL_PATH = 'risk_clf.joblib'


class RiskEngine:
    def __init__(self, use_ml=False):
        # only use ML if model artifact exists
        self.use_ml = use_ml and os.path.exists(MODEL_PATH)
        self.clf = None
        if self.use_ml:
            self.clf = joblib.load(MODEL_PATH)

    def score(self, features: dict):
        """
        Returns (numeric_score, reasons_list)
        Numeric score: for rules -> computed points; for ML -> weighted from predicted probs
        """
        reasons = []
        if self.use_ml and self.clf is not None:
            X = [[
                int(features.get('ip_unknown', 0)),
                float(features.get('geo_distance_km', 0.0)),
                int(features.get('time_anomaly', 0)),
                int(features.get('device_unknown', 0)),
                int(features.get('failed_attempts', 0))
            ]]
            probs = self.clf.predict_proba(X)[0]
            # weight medium class and high class to form a pseudo-score
            score = probs[1] * 50 + probs[2] * 100
        else:
            score = compute_rule_score(features)

        # textual reasons for explainability
        if features.get('ip_unknown'):
            reasons.append('new IP')
        if features.get('device_unknown'):
            reasons.append('unknown device')
        if features.get('time_anomaly'):
            reasons.append('time anomaly')
        if features.get('geo_distance_km', 0) > 50:
            reasons.append(f"large geo delta: {features.get('geo_distance_km'):.1f} km")
        if features.get('failed_attempts', 0) > 0:
            reasons.append(f"{features.get('failed_attempts')} failed attempts")
        return score, reasons


# rule weights (tuneable)
RULE_WEIGHTS = {
    'ip_unknown': 40,
    'geo_distance_km': 0.5,   # per km
    'time_anomaly': 20,
    'device_unknown': 30,
    'failed_attempts': 10,
}


def compute_rule_score(features: dict) -> float:
    score = 0.0
    if features.get('ip_unknown'):
        score += RULE_WEIGHTS['ip_unknown']
    score += RULE_WEIGHTS['geo_distance_km'] * features.get('geo_distance_km', 0)
    if features.get('time_anomaly'):
        score += RULE_WEIGHTS['time_anomaly']
    if features.get('device_unknown'):
        score += RULE_WEIGHTS['device_unknown']
    score += RULE_WEIGHTS['failed_attempts'] * features.get('failed_attempts', 0)
    return score


def map_score_to_level(score: float) -> str:
    if score < 30:
        return 'low'
    if score < 70:
        return 'medium'
    return 'high'


# helpers
def haversine_km(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, asin, sqrt
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lon1)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


def compute_features_for_user(user: dict, attempt) -> dict:
    """
    user: dict from SimpleUserDB
    attempt: object with fields ip, user_agent, lat, lon, timestamp
    """
    features = {}
    known_ips = set(user.get('known_ips', []))
    known_devices = set(user.get('known_devices', []))

    features['ip_unknown'] = 0 if attempt.ip in known_ips else 1

    lat0 = user.get('lat', None)
    lon0 = user.get('lon', None)
    if lat0 is not None and lon0 is not None:
        try:
            dist = haversine_km(lat0, lon0, attempt.lat, attempt.lon)
        except Exception:
            dist = 0.0
    else:
        dist = 0.0
    features['geo_distance_km'] = dist

    # simple time anomaly heuristic: consider hours 23-5 anomalous (demo)
    hour = int((attempt.timestamp % 86400) // 3600)
    features['time_anomaly'] = 1 if (hour < 6 or hour > 22) else 0

    features['device_unknown'] = 0 if attempt.user_agent in known_devices else 1
    features['failed_attempts'] = user.get('failed_attempts', 0)
    return features
