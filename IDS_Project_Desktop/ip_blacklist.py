import json
import os

class IPBlacklistManager:
    def __init__(self, threshold=3, log_file=None):
        self.threshold = threshold
        # Force file to be on the Desktop
        if log_file is None:
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            self.log_file = os.path.join(desktop, "blacklist.json")
        else:
            self.log_file = log_file
            
        self.threat_counts = {}
        self.blacklisted_ips = set()
        self.load_blacklist()

    def record_threat(self, ip):
        if ip in self.blacklisted_ips:
            return True
        
        self.threat_counts[ip] = self.threat_counts.get(ip, 0) + 1
        if self.threat_counts[ip] >= self.threshold:
            self.blacklisted_ips.add(ip)
            self.save_blacklist()
            return True
        return False

    def load_blacklist(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    data = json.load(f)
                    self.blacklisted_ips = set(data.get("blacklisted", []))
            except:
                pass

    def save_blacklist(self):
        try:
            with open(self.log_file, "w") as f:
                json.dump({"blacklisted": list(self.blacklisted_ips)}, f)
        except Exception as e:
            print(f"Error saving blacklist: {e}")
