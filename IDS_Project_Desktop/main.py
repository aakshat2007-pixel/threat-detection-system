import threading
import queue
import time
import math
import random
from datetime import datetime
import psutil
from tkinter import *
from tkinter import ttk, messagebox
from plyer import notification
from ip_blacklist import IPBlacklistManager

# ---------------- APEX DESIGN SYSTEM (V13-FIXED) ----------------
C_VOID = "#020617"          
C_SURFACE = "#0F172A"       
C_BORDER = "#1E293B"        
C_ACCENT = "#0EA5E9"        
C_WARN = "#F43F5E"          
C_OK = "#10B981"            
C_TERM = "#2DD4BF"          
C_TEXT_P = "#F8FAFC"        
C_TEXT_S = "#94A3B8"        

class CyberBootBg(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=C_VOID, highlightthickness=0, **kwargs)
        self.hex_chars = "0123456789ABCDEF"
        self.drops = [{'x': x, 'y': random.randint(-100, 800), 's': random.randint(8, 20)} for x in range(0, 1400, 40)]
        self.animate()

    def animate(self):
        self.delete("all")
        for d in self.drops:
            char = random.choice(self.hex_chars)
            self.create_text(d['x'], d['y'], text=char, fill="#0f172a", font=("Consolas", 10))
            d['y'] += d['s']
            if d['y'] > 900: d['y'] = -20
        self.after(30, self.animate)

class CyberButton(Canvas):
    def __init__(self, parent, text, color, command, width=280, height=50):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)
        self.command, self.color = command, color
        self.rect = self.create_rectangle(0, 0, width, height, fill=C_VOID, outline=color, width=2)
        self.lbl = self.create_text(width/2, height/2, text=text, fill=color, font=("Segoe UI Bold", 10))
        self.bind("<Enter>", lambda e: self.itemconfig(self.rect, fill=color, outline=C_TEXT_P))
        self.bind("<Enter>", lambda e: self.itemconfig(self.lbl, fill=C_VOID), add="+")
        self.bind("<Leave>", lambda e: self.itemconfig(self.rect, fill=C_VOID, outline=color))
        self.bind("<Leave>", lambda e: self.itemconfig(self.lbl, fill=color), add="+")
        self.bind("<Button-1>", lambda e: self.command())

class SentinelPrimeTurbo(Tk):
    def __init__(self):
        super().__init__()
        self.title("SENTINEL PRIME: COMMAND CENTER")
        self.geometry("1400x900")
        self.configure(bg=C_VOID)
        self.show_auth()

    def show_auth(self):
        self.auth_f = Frame(self, bg=C_VOID); self.auth_f.pack(fill=BOTH, expand=True)
        CyberBootBg(self.auth_f).place(relx=0, rely=0, relwidth=1, relheight=1)
        card = Frame(self.auth_f, bg=C_VOID, padx=60, pady=70, highlightbackground=C_ACCENT, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor=CENTER)
        Label(card, text="SECURE TERMINAL", bg=C_VOID, fg=C_ACCENT, font=("Segoe UI", 24, "bold")).pack(pady=(0, 5))
        Label(card, text="CLEARANCE LEVEL 5 REQUIRED", bg=C_VOID, fg=C_TEXT_S, font=("Consolas", 9)).pack(pady=(0, 45))
        self.u = self.add_field(card, "OPERATOR_ID")
        self.p = self.add_field(card, "SEC_ACCESS_KEY", True)
        self.btn = CyberButton(card, "INITIALIZE HANDSHAKE", C_ACCENT, self.run_boot)
        self.btn.pack(pady=(40, 0))
        self.boot_log = Label(card, text="", bg=C_VOID, fg=C_OK, font=("Consolas", 8))

    def add_field(self, p, l, is_p=False):
        f = Frame(p, bg=C_VOID); f.pack(fill=X, pady=12)
        Label(f, text=l, bg=C_VOID, fg=C_TEXT_S, font=("Consolas", 8, "bold")).pack(anchor=W)
        e = Entry(f, bg=C_VOID, fg=C_ACCENT, insertbackground=C_ACCENT, font=("Consolas", 12), border=0, show="*" if is_p else "")
        e.pack(fill=X, ipady=12, pady=5)
        Frame(f, height=1, bg=C_BORDER).pack(fill=X); return e

    def run_boot(self):
        if self.u.get() == "akshat" and self.p.get() == "123":
            self.btn.pack_forget()
            self.boot_log.pack(pady=10); self.boot_sequence(0)
        else: messagebox.showerror("DENIED", "ACCESS RESTRICTED")

    def boot_sequence(self, step):
        logs = ["Loading Kernel...", "Mounting Secure FS...", "Linking Data Streams...", "Initializing Prime Core...", "ACCESS GRANTED"]
        if step < len(logs):
            self.boot_log.config(text=logs[step])
            self.after(80, lambda: self.boot_sequence(step + 1))
        else:
            self.auth_f.pack_forget()
            Dashboard(self).pack(fill=BOTH, expand=True)

class Dashboard(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=C_VOID)
        self.active = False; self.stats = {'pkts': 0, 'thrt': 0}
        self.notifications_enabled = True 
        self.last_notify_time = 0 
        self.q = queue.Queue(); self.buf = []; self.lock = threading.Lock()
        
        # Use a fixed Malicious Node list to ensure they reach the threshold
        self.malicious_nodes = ["10.0.0.1", "10.0.0.5", "10.0.0.12", "172.16.5.4", "192.168.1.101"]
        self.blacklist = IPBlacklistManager(threshold=3) 
        
        self.nodes = []
        self.last_net = psutil.net_io_counters(); self.last_net_time = time.time()
        self.setup_ui(); self.animate_dashboard()

    def setup_ui(self):
        nav = Frame(self, bg=C_SURFACE, height=90, highlightbackground=C_BORDER, highlightthickness=1)
        nav.pack(side=TOP, fill=X); nav.pack_propagate(False)
        Label(nav, text="SENTINEL PRIME // COMMAND CENTER [AUTONOMOUS]", bg=C_SURFACE, fg=C_ACCENT, font=("Consolas", 18, "bold")).pack(side=LEFT, padx=30)
        telemetry = Frame(nav, bg=C_SURFACE); telemetry.pack(side=RIGHT, padx=30)
        self.net_lbl = Label(telemetry, text="NET: 0 KB/s", bg=C_SURFACE, fg=C_TERM, font=("Consolas", 9, "bold"))
        self.net_lbl.pack(side=LEFT, padx=20)
        self.cpu_bar = self.create_vital_bar(telemetry, "CPU_CORE")
        self.ram_bar = self.create_vital_bar(telemetry, "MEM_ALLOC")
        main = Frame(self, bg=C_VOID, padx=20, pady=20); main.pack(fill=BOTH, expand=True)
        left = Frame(main, bg=C_VOID, width=320); left.pack(side=LEFT, fill=Y); left.pack_propagate(False)
        self.tile_p = self.create_glow_tile(left, "NETWORK_TRAFFIC", C_ACCENT)
        self.tile_t = self.create_glow_tile(left, "THREAT_DETECTIONS", C_WARN)
        ctrl = Frame(left, bg=C_SURFACE, padx=20, pady=25, highlightbackground=C_BORDER, highlightthickness=1)
        ctrl.pack(fill=X, pady=15)
        CyberButton(ctrl, "ENGAGE PROTOCOL", C_OK, self.start, width=275).pack(pady=6)
        CyberButton(ctrl, "HALT_SEQUENCE", C_WARN, self.stop, width=275).pack(pady=6)
        
        # Notification Toggle
        self.notif_btn = CyberButton(ctrl, "NOTIFICATIONS: ON", C_TERM, self.toggle_notifs, width=275)
        self.notif_btn.pack(pady=6)
        
        CyberButton(ctrl, "THREAT_DATABASE", C_ACCENT, self.show_bl, width=275).pack(pady=(15, 0))
        right = Frame(main, bg=C_VOID, width=350); right.pack(side=RIGHT, fill=Y); right.pack_propagate(False)
        term_f = Frame(right, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        term_f.pack(fill=BOTH, expand=True, pady=(0, 15))
        self.term_txt = Text(term_f, bg=C_VOID, fg=C_TERM, font=("Consolas", 8), border=0, padx=10, pady=10)
        self.term_txt.pack(fill=BOTH, expand=True, padx=5, pady=5)
        center = Frame(main, bg=C_VOID); center.pack(side=LEFT, fill=BOTH, expand=True, padx=(20, 20))
        orb_f = Frame(center, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1); orb_f.pack(fill=X, pady=(0, 20))
        self.canv = Canvas(orb_f, bg=C_SURFACE, height=450, highlightthickness=0); self.canv.pack(fill=X, padx=15, pady=15)
        feed_f = Frame(center, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1); feed_f.pack(fill=BOTH, expand=True)
        self.setup_intel_feed(feed_f)

    def create_vital_bar(self, parent, label):
        f = Frame(parent, bg=C_SURFACE, padx=10); f.pack(side=LEFT)
        Label(f, text=label, bg=C_SURFACE, fg=C_TEXT_S, font=("Consolas", 7, "bold")).pack()
        c = Canvas(f, width=100, height=6, bg=C_VOID, highlightthickness=0); c.pack()
        bar = c.create_rectangle(0, 0, 0, 6, fill=C_ACCENT); return c, bar

    def create_glow_tile(self, p, t, c):
        f = Frame(p, bg=C_SURFACE, padx=25, pady=25, highlightbackground=C_BORDER, highlightthickness=1); f.pack(fill=X, pady=(0, 15))
        Label(f, text=t, bg=C_SURFACE, fg=C_TEXT_S, font=("Consolas", 8, "bold")).pack(anchor=W)
        l = Label(f, text="0000", bg=C_SURFACE, fg=c, font=("Consolas", 32, "bold")); l.pack(anchor=W); return l

    def setup_intel_feed(self, p):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("Treeview", background=C_SURFACE, foreground=C_TEXT_P, fieldbackground=C_SURFACE, rowheight=35, borderwidth=0)
        s.configure("Treeview.Heading", background=C_BORDER, foreground=C_ACCENT, font=("Consolas", 10, "bold"), borderwidth=0)
        self.tree = ttk.Treeview(p, columns=("1", "2", "3", "4"), show="headings", height=6)
        for i, h in enumerate(["TIME", "NODE_ID", "PROTOCOL", "STATUS"]): self.tree.heading(str(i+1), text=h)
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.tag_configure("BLOCKED", foreground=C_WARN)
        self.scan_canv = Canvas(p, height=2, bg=C_ACCENT, highlightthickness=0); self.scan_canv.place(x=0, y=30, relwidth=1)
        self.scan_y = 30

    def toggle_notifs(self):
        self.notifications_enabled = not self.notifications_enabled
        new_text = "NOTIFICATIONS: ON" if self.notifications_enabled else "NOTIFICATIONS: OFF"
        new_color = C_TERM if self.notifications_enabled else C_WARN
        self.notif_btn.itemconfig(self.notif_btn.lbl, text=new_text, fill=new_color)
        self.notif_btn.itemconfig(self.notif_btn.rect, outline=new_color)

    def log_to_term(self, msg):
        self.term_txt.insert(END, f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {msg}\n"); self.term_txt.see(END)
        if float(self.term_txt.index('end')) > 150.0: self.term_txt.delete("1.0", "2.0")

    def animate_dashboard(self):
        self.angle = 0; self.draw_orbital(); self.animate_scan_line()

    def animate_scan_line(self):
        self.scan_y += 6
        if self.scan_y > 280: self.scan_y = 30
        self.scan_canv.place(y=self.scan_y); self.after(20, self.animate_scan_line)

    def draw_orbital(self):
        self.canv.delete("all"); cx, cy, r = 320, 225, 200
        for i in range(1, 5):
            d = r * (i/4); self.canv.create_oval(cx-d, cy-d, cx+d, cy+d, outline=C_BORDER, width=1, dash=(2,4))
        self.canv.create_line(cx-r, cy, cx+r, cy, fill=C_BORDER); self.canv.create_line(cx, cy-r, cx, cy+r, fill=C_BORDER)
        sw = math.radians(self.angle); self.canv.create_line(cx, cy, cx+r*math.cos(sw), cy+r*math.sin(sw), fill=C_ACCENT, width=2)
        for i in range(25):
            a = math.radians(self.angle - i*2); alpha = (25-i)/25
            self.canv.create_line(cx, cy, cx+r*math.cos(a), cy+r*math.sin(a), fill=self.lerp(C_SURFACE, C_ACCENT, alpha))
        for n in self.nodes[:]:
            n['l'] -= 0.04
            if n['l'] <= 0: self.nodes.remove(n)
            else:
                sz = 6 * n['l']; col = self.lerp(C_SURFACE, n['c'], n['l'])
                self.canv.create_oval(n['x']-sz, n['y']-sz, n['x']+sz, n['y']+sz, fill=col, outline="")
                if n['c'] == C_WARN:
                    rs = 18 * (1.2 - n['l']); self.canv.create_rectangle(n['x']-rs, n['y']-rs, n['x']+rs, n['y']+rs, outline=C_WARN, width=1)
        self.angle = (self.angle + 8) % 360
        self.after(20, self.draw_orbital)

    def lerp(self, c1, c2, t):
        def r(h): return tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        r1, g1, b1 = r(c1); r2, g2, b2 = r(c2)
        return '#%02x%02x%02x' % (int(r1+(r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))

    def start(self):
        self.active = True; self.log_to_term("TURBO_MODE_ENGAGED."); threading.Thread(target=self.sim_engine, daemon=True).start()
        threading.Thread(target=self.intel_engine, daemon=True).start(); self.update_telemetry()

    def stop(self): self.active = False; self.log_to_term("STANDBY.")

    def sim_engine(self):
        while self.active:
            is_t = random.random() < 0.2
            if is_t:
                # Use a specific malicious IP
                src = random.choice(self.malicious_nodes)
            else:
                src = f"NODE_{random.randint(100,999)}"
            
            with self.lock: self.buf.append(([6, 2000 if is_t else 400, 0, 0, 3389 if is_t else 80], src, "EXT_LNK"))
            self.stats['pkts'] += 1; ang = random.uniform(0, 2*math.pi); dist = random.uniform(40, 190); node_id = src
            self.nodes.append({'x': 320+dist*math.cos(ang), 'y': 225+dist*math.sin(ang), 'l': 1.0, 'c': C_WARN if is_t else C_ACCENT, 'id': node_id})
            
            if is_t:
                self.log_to_term(f"ALERT: BREACH_DETECTED FROM {node_id}")
                # Immediately increment threat counter for visibility
                self.stats['thrt'] += 1
                current_time = time.time()
                if self.active and self.notifications_enabled and (current_time - self.last_notify_time > 5):
                    try:
                        notification.notify(title="AUTONOMOUS ALERT", message=f"Threat Intercepted: {node_id}", timeout=1)
                        self.last_notify_time = current_time
                    except: pass
            else: self.log_to_term(f"RECV_{node_id}")
            time.sleep(random.uniform(0.02, 0.08))

    def intel_engine(self):
        while self.active:
            if self.buf:
                with self.lock: f, s, d = self.buf.pop(0)
                lvl = "SECURE"
                if f[1] > 1500 or f[4] == 3389:
                    if s in self.blacklist.blacklisted_ips:
                        lvl = "BLOCKED"
                    else:
                        lvl = "CRITICAL"
                        if self.blacklist.record_threat(s): 
                            lvl = "BLOCKED"
                            self.log_to_term(f"AUTONOMOUS_ACTION: {s} PERMANENTLY BLOCKED.")
                self.q.put((datetime.now().strftime("%H:%M:%S"), s, d, lvl))
            else: time.sleep(0.05)

    def update_telemetry(self):
        cpu = psutil.cpu_percent(); ram = psutil.virtual_memory().percent
        self.cpu_bar[0].coords(self.cpu_bar[1], 0, 0, cpu, 6); self.ram_bar[0].coords(self.ram_bar[1], 0, 0, ram, 6)
        now = time.time(); net_now = psutil.net_io_counters(); diff = now - self.last_net_time
        if diff > 0: kbps = ((net_now.bytes_recv - self.last_net.bytes_recv) / diff) / 1024; self.net_lbl.config(text=f"NET: {kbps:.1f} KB/s")
        self.last_net = net_now; self.last_net_time = now
        while not self.q.empty():
            row = self.q.get(); 
            tag = "BLOCKED" if row[-1] == "BLOCKED" else "NORMAL"
            self.tree.insert("", 0, values=row, tags=(tag,))
            if len(self.tree.get_children()) > 12: self.tree.delete(self.tree.get_children()[-1])
        self.tile_p.config(text=f"{self.stats['pkts']:04d}"); self.tile_t.config(text=f"{self.stats['thrt']:04d}")
        if self.active: self.after(100, self.update_telemetry)

    def show_bl(self):
        win = Toplevel(self); win.title("Prime DB"); win.geometry("500x600"); win.configure(bg=C_VOID)
        Label(win, text="RESTRICTED_THREAT_DATABASE", bg=C_VOID, fg=C_WARN, font=("Consolas", 14, "bold")).pack(pady=20)
        lb = Listbox(win, bg=C_SURFACE, fg=C_TERM, border=0, font=("Consolas", 10)); lb.pack(fill=BOTH, expand=True, padx=25, pady=10)
        # Force reload from file to ensure visibility
        self.blacklist.load_blacklist()
        for ip in sorted(self.blacklist.blacklisted_ips): lb.insert(END, f" > BLOCKED: {ip}")
        CyberButton(win, "CLOSE", C_ACCENT, win.destroy, width=240).pack(pady=20)

if __name__ == "__main__":
    SentinelPrimeTurbo().mainloop()
