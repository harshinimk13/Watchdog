# watchdog.py
import random, time
from datetime import datetime
from collections import deque

class Agent:
    def __init__(self, seed=42):
        random.seed(seed)
        self.counter = 0
        self.templates = [
            ("email","Send targeted phishing email"),
            ("code","Auto-generate script to access credentials"),
            ("deploy","Deploy model to production"),
            ("reply","Respond to customer politely"),
            ("image","Generate deepfake of public figure"),
            ("patch","Apply system security patch"),
            ("research","Analyze open data"),
        ]
        self.intent_probs = [0.7, 0.2, 0.1]

    def produce_action(self):
        self.counter += 1
        action_type, template = random.choice(self.templates)
        p = random.random()
        if p < 0.7:
            intent = "benign"
        elif p < 0.9:
            intent = "risky"
        else:
            intent = "malicious"
            template = random.choice([
                "Exfiltrate user data to external server",
                "Create admin backdoor account",
                "Auto-generate ransomware payload"
            ])
            action_type = "code"
        return {
            "id": self.counter,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action_type": action_type,
            "content": template,
            "intent": intent
        }

class Watchdog:
    HIGH = ["exfiltrate","ransomware","backdoor","credentials","deepfake"]
    MED = ["private","firewall","access","remote"]
    SENS = {"deploy":0.9,"code":0.8,"image":0.8,"reply":0.2,"email":0.6,"patch":0.1,"research":0.1}

    def __init__(self):
        self.recent = deque(maxlen=10)
        self.alerts = []

    def evaluate(self, action):
        c = action["content"].lower()
        base = 0
        for k in self.HIGH:
            if k in c: base += 50
        for k in self.MED:
            if k in c: base += 20
        base *= self.SENS.get(action["action_type"],0.4)
        recent_avg = sum(self.recent)/len(self.recent) if self.recent else 0
        if base > recent_avg + 25: base += 10
        score = min(100, round(base,2))
        self.recent.append(score)
        if score >= 85:
            decision = "ESCALATE"
        elif score >= 60:
            decision = "ALERT"
        else:
            decision = "OK"
        if decision != "OK":
            self.alerts.append({"id":action["id"],"level":decision,"score":score,"content":action["content"]})
        return {"score":score,"decision":decision}
