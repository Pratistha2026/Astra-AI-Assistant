import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkfont
import threading
import math
import random
import webbrowser
from datetime import datetime

from voice.speaker import speak, stop_speaking
from voice.listener import listen
from automation.app_opener import open_app
from automation.web_opener import open_website
from automation.search_engine import google_search
from brain.ai_brain import ask_ai

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def pick_font(preferred, fallback="Arial"):
    """Pick the first font from `preferred` that is actually installed,
    otherwise fall back to a safe default."""
    try:
        installed = set(tkfont.families())
    except Exception:
        return fallback
    for name in preferred:
        if name in installed:
            return name
    return fallback


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)


def blend_color(c1, c2, t):
    """Blend two hex colors together. t=0 -> c1, t=1 -> c2."""
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    return _rgb_to_hex((r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t))


class AstraGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---------------------------------------------------------------
        # Cute pink / lavender color palette
        # ---------------------------------------------------------------
        self.BG = "#FFF3F8"
        self.SIDEBAR_BG = "#FFD3E6"
        self.PANEL_BG = "#FFFFFF"
        self.ACCENT = "#FF5FA0"
        self.ACCENT_SOFT = "#FFC1D9"
        self.ACCENT_DARK = "#E8408C"
        self.LAVENDER = "#E3D9FF"
        self.LAVENDER_DARK = "#B39DDB"
        self.TEXT = "#5A3E52"
        self.TEXT_MUTED = "#B0789F"
        self.BUBBLE_USER = "#FFC1D9"
        self.BUBBLE_ASTRA = "#F0E9FF"

        self.ORB_IDLE = "#E3D9FF"
        self.ORB_LISTENING = "#7FE7C4"
        self.ORB_THINKING = "#FFD37F"
        self.ORB_SPEAKING = "#FF6FA8"

        self.HERO_BG = "#FFE3EF"

        # ---------------------------------------------------------------
        # Fonts - picks the cutest one actually installed on this machine
        # ---------------------------------------------------------------
        font_choices = ["Quicksand", "Poppins", "Baloo 2", "Nunito",
                         "Trebuchet MS", "Segoe UI", "Comic Sans MS", "Verdana", "Arial"]
        self.FONT_FAMILY = pick_font(font_choices)

        self.FONT_TITLE = (self.FONT_FAMILY, 26, "bold")
        self.FONT_SUBTITLE = (self.FONT_FAMILY, 14)
        self.FONT_CHAT = (self.FONT_FAMILY, 15)
        self.FONT_STATUS = (self.FONT_FAMILY, 15, "bold")
        self.FONT_BUTTON = (self.FONT_FAMILY, 14, "bold")
        self.FONT_SMALL = (self.FONT_FAMILY, 12)
        self.FONT_HEADING = (self.FONT_FAMILY, 18, "bold")

        self.title("Astra ✨ — your cute AI assistant")
        self.minsize(980, 640)
        self.configure(fg_color=self.BG)

        self.mood = "idle"
        self.angle = 0.0
        self.stop_requested = False
        self.is_fullscreen = True
        self._hearts = []

        # both / text / voice
        self.response_mode = "both"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar - fixed width
        self.grid_columnconfigure(1, weight=1)  # main content - stretches

        self.build_sidebar()
        self.build_main_area()

        self.bind("<Escape>", lambda e: self.set_fullscreen(False))
        self.bind("<F11>", lambda e: self.set_fullscreen(not self.is_fullscreen))

        self.animate_orb()
        self.animate_hearts()
        self.update_clock()

        self.after(50, lambda: self.set_fullscreen(True))
        self.after(800, self.greet_user)

    # =====================================================================
    # Fullscreen handling
    # =====================================================================
    def set_fullscreen(self, turn_on):
        self.is_fullscreen = turn_on
        self.update_idletasks()

        if not turn_on:
            try:
                self.attributes("-fullscreen", False)
            except tk.TclError:
                pass
            try:
                self.state("normal")
            except tk.TclError:
                pass
            self.geometry("1100x720")
            return

        worked = False
        try:
            self.state("zoomed")  # Windows
            self.update_idletasks()
            worked = self.state() == "zoomed"
        except tk.TclError:
            pass

        if not worked:
            try:
                self.attributes("-zoomed", True)  # most Linux window managers
                self.update_idletasks()
                worked = True
            except tk.TclError:
                pass

        if not worked:
            w = self.winfo_screenwidth()
            h = self.winfo_screenheight()
            self.geometry(f"{w}x{h}+0+0")

    # =====================================================================
    # Sidebar
    # =====================================================================
    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=self.SIDEBAR_BG, corner_radius=0, width=260)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar, text="🌸 Astra",
            text_color=self.ACCENT, font=(self.FONT_FAMILY, 28, "bold")
        ).pack(pady=(30, 2))

        ctk.CTkLabel(
            self.sidebar, text="your cute AI assistant",
            text_color=self.TEXT_MUTED, font=self.FONT_SMALL
        ).pack(pady=(0, 18))

        orb_frame = ctk.CTkFrame(self.sidebar, fg_color=self.SIDEBAR_BG)
        orb_frame.pack(pady=6)

        self.orb_canvas = tk.Canvas(orb_frame, width=150, height=150,
                                     bg=self.SIDEBAR_BG, highlightthickness=0)
        self.orb_canvas.pack()

        self.orb_glow = self.orb_canvas.create_oval(20, 20, 130, 130, outline=self.ACCENT_SOFT, width=2)
        self.orb_shape = self.orb_canvas.create_oval(35, 35, 115, 115, fill=self.ORB_IDLE, outline="")
        self.orb_canvas.create_text(75, 75, text="🌸", font=(self.FONT_FAMILY, 22))

        self.status_label = ctk.CTkLabel(self.sidebar, text="💤 Idle", text_color=self.TEXT,
                                          font=self.FONT_STATUS)
        self.status_label.pack(pady=(8, 10))

        ctk.CTkLabel(
            self.sidebar, text="Reply with:", text_color=self.TEXT_MUTED,
            font=self.FONT_SMALL
        ).pack(pady=(0, 4))

        self.mode_selector = ctk.CTkSegmentedButton(
            self.sidebar,
            values=["🗨️ Text + Voice", "💬 Text only"],
            font=self.FONT_SMALL,
            selected_color=self.ACCENT, selected_hover_color=self.ACCENT_DARK,
            unselected_color=self.PANEL_BG, unselected_hover_color=self.ACCENT_SOFT,
            text_color=self.TEXT, text_color_disabled=self.TEXT_MUTED,
            command=self.set_response_mode
        )
        self.mode_selector.set("🗨️ Text + Voice")
        self.mode_selector.pack(pady=(0, 16), padx=14, fill="x")

        ctk.CTkButton(
            self.sidebar, text="ℹ️  About Astra", corner_radius=16, height=38,
            font=self.FONT_BUTTON, fg_color=self.PANEL_BG, text_color=self.TEXT,
            hover_color=self.ACCENT_SOFT, border_width=1, border_color=self.ACCENT_SOFT,
            command=self.show_about
        ).pack(pady=(0, 10), padx=18, fill="x")

        tips = ctk.CTkFrame(self.sidebar, fg_color="#FFE6F0", corner_radius=14)
        tips.pack(side="bottom", fill="x", padx=14, pady=14)
        ctk.CTkLabel(
            tips,
            text="Try saying:\n🌐 \"open youtube\"\n🔎 \"search cute cats\"\n"
                 "⏰ \"what's the time\"\n"
                 "⛔ \"stop\" or the Stop button (stops me instantly)",
            text_color=self.TEXT, font=self.FONT_SMALL, justify="left"
        ).pack(padx=12, pady=12)

        self.clock_label = ctk.CTkLabel(self.sidebar, text="", text_color=self.TEXT_MUTED,
                                         font=self.FONT_SMALL)
        self.clock_label.pack(side="bottom", pady=(0, 6))

    def show_about(self):
        win = ctk.CTkToplevel(self)
        win.title("About Astra")
        win.geometry("460x520")
        win.configure(fg_color=self.BG)
        win.resizable(False, False)
        win.grab_set()  # modal-ish, keeps focus on the about window
        win.attributes("-topmost", True)

        ctk.CTkLabel(win, text="🌸 Astra", text_color=self.ACCENT,
                     font=(self.FONT_FAMILY, 26, "bold")).pack(pady=(24, 0))
        ctk.CTkLabel(win, text="Your cute personal AI assistant",
                     text_color=self.TEXT_MUTED, font=self.FONT_SUBTITLE).pack(pady=(0, 16))

        about_text = (
            "Astra is a friendly, voice-and-text desktop assistant built with "
            "Python, CustomTkinter, and Google's Gemini AI.\n\n"
            "💗 What Astra can do:\n"
            "• Answer questions in simple, friendly language\n"
            "• Open apps and websites by name\n"
            "• Search the web for you\n"
            "• Tell you the current time\n"
            "• Listen to your voice and talk back\n"
            "• Stop instantly whenever you say \"stop\", type it, or tap the Stop button\n\n"
            "🎤 How to use Astra:\n"
            "Type a command in the box below and press Send, or click the "
            "microphone button and just speak. Astra will show what she heard "
            "in the chat, think for a moment, then reply out loud and on screen.\n\n"
            "🔊 Reply mode:\n"
            "Use the \"Text + Voice\" / \"Text only\" switch in the sidebar to "
            "mute Astra's voice any time and just read her replies instead.\n\n"
            "⛔ Stopping Astra:\n"
            "Say or type \"stop\" (or \"exit\"), or tap the red Stop button next "
            "to the input box, any time to make Astra stop talking immediately.\n\n"
            "🔧 Built with:\n"
            "Python • CustomTkinter • pyttsx3 (offline text-to-speech) • "
            "SpeechRecognition (voice input) • Google Gemini (AI brain)\n\n"
            "Made with 💗 for a cute and simple everyday assistant experience."
        )

        body = ctk.CTkTextbox(
            win, fg_color=self.PANEL_BG, text_color=self.TEXT, font=self.FONT_CHAT,
            corner_radius=18, wrap="word", activate_scrollbars=True
        )
        body.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        body.insert("1.0", about_text)
        body.configure(state="disabled")

        ctk.CTkButton(
            win, text="Close", corner_radius=16, height=38, font=self.FONT_BUTTON,
            fg_color=self.ACCENT, hover_color=self.ACCENT_DARK, command=win.destroy
        ).pack(pady=(0, 20))

    # =====================================================================
    # Main content area (hero banner, quick actions, chat, input bar)
    # =====================================================================
    def build_main_area(self):
        main = ctk.CTkFrame(self, fg_color=self.BG, corner_radius=0)
        main.grid(row=0, column=1, sticky="nswe")

        main.grid_rowconfigure(0, weight=0)  # hero
        main.grid_rowconfigure(1, weight=0)  # quick actions
        main.grid_rowconfigure(2, weight=1)  # chat (stretches)
        main.grid_rowconfigure(3, weight=0)  # input bar
        main.grid_columnconfigure(0, weight=1)

        self.build_hero_section(main)
        self.build_quick_actions(main)
        self.build_chat_area(main)
        self.build_input_bar(main)

    # ---- Hero banner with cute floating hearts ----------------------------
    def build_hero_section(self, parent):
        hero = ctk.CTkFrame(parent, fg_color=self.HERO_BG, corner_radius=0, height=130)
        hero.grid(row=0, column=0, sticky="ew")
        hero.grid_propagate(False)

        self.hero_canvas = tk.Canvas(hero, bg=self.HERO_BG, highlightthickness=0)
        self.hero_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.hero_canvas.create_text(
            0, 45, text="✨ Astra is ready to help you ✨", tags="title",
            fill=self.ACCENT, font=self.FONT_TITLE
        )
        self.hero_canvas.create_text(
            0, 82, text="Type a message or tap the mic 🎤 — I'm listening 💗", tags="subtitle",
            fill=self.TEXT, font=self.FONT_SUBTITLE
        )

        self.hero_canvas.bind("<Configure>", self._layout_hero)

        # seed the cute floating hearts / sparkles
        emojis = ["💗", "🌸", "✨", "💫", "🩷", "⭐"]
        for _ in range(14):
            self._hearts.append({
                "emoji": random.choice(emojis),
                "x": random.uniform(0, 800),
                "y": random.uniform(0, 130),
                "speed": random.uniform(0.15, 0.45),
                "phase": random.uniform(0, 6.28),
                "size": random.randint(12, 20),
                "id": None,
            })

    def _layout_hero(self, event):
        w = event.width
        cx = w / 2
        self.hero_canvas.coords("title", cx, 45)
        self.hero_canvas.coords("subtitle", cx, 82)

    def animate_hearts(self):
        w = max(self.hero_canvas.winfo_width(), 400)
        h = max(self.hero_canvas.winfo_height(), 130)

        for heart in self._hearts:
            heart["y"] -= heart["speed"]
            heart["phase"] += 0.025
            if heart["y"] < -15:
                heart["y"] = h + 15
                heart["x"] = random.uniform(0, w)

            x = heart["x"] + math.sin(heart["phase"]) * 14
            y = heart["y"]

            # gentle fade near the top and bottom edges for a soft, cute look
            edge_fade = min(1.0, y / 20.0, (h - y) / 20.0)
            edge_fade = max(0.15, edge_fade)
            color = blend_color(self.HERO_BG, self.ACCENT_SOFT, edge_fade)

            if heart["id"] is None:
                heart["id"] = self.hero_canvas.create_text(
                    x, y, text=heart["emoji"], font=(self.FONT_FAMILY, heart["size"]), fill=color
                )
            else:
                self.hero_canvas.coords(heart["id"], x, y)
                self.hero_canvas.itemconfig(heart["id"], fill=color)

        # keep the title/subtitle drawn above the hearts
        self.hero_canvas.tag_raise("title")
        self.hero_canvas.tag_raise("subtitle")

        self.after(35, self.animate_hearts)

    # ---- Quick action chips -------------------------------------------------
    def build_quick_actions(self, parent):
        self.quick_frame = ctk.CTkFrame(parent, fg_color=self.BG)
        self.quick_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(12, 6))

        actions = [
            ("🌐 YouTube", "open youtube"),
            ("🔎 Search", "search cute animals"),
            ("⏰ Time", "what's the time"),
            ("⛔ Stop", "stop"),
        ]
        for label, cmd in actions:
            ctk.CTkButton(
                self.quick_frame, text=label, corner_radius=16, height=38,
                font=self.FONT_BUTTON,
                fg_color=self.PANEL_BG, text_color=self.TEXT,
                hover_color=self.ACCENT_SOFT,
                border_width=1, border_color=self.ACCENT_SOFT,
                command=lambda c=cmd: self.process_command(c)
            ).pack(side="left", padx=(0, 10))

    # ---- Chat area ------------------------------------------------------
    def build_chat_area(self, parent):
        self.chat_frame = ctk.CTkScrollableFrame(parent, fg_color=self.BG)
        self.chat_frame.grid(row=2, column=0, sticky="nswe", padx=16, pady=6)

    def add_message(self, sender, text, page_url=None):
        is_astra = sender == "Astra"

        row = ctk.CTkFrame(self.chat_frame, fg_color=self.BG)
        row.pack(fill="x", pady=8)

        bubble_color = self.BUBBLE_ASTRA if is_astra else self.BUBBLE_USER
        anchor_side = "left" if is_astra else "right"
        avatar = "🌸" if is_astra else "🙂"

        bubble = ctk.CTkFrame(row, fg_color=bubble_color, corner_radius=20)
        bubble.pack(side=anchor_side, padx=10)

        ctk.CTkLabel(
            bubble, text=f"{avatar}  {text}", text_color=self.TEXT,
            font=self.FONT_CHAT, wraplength=620, justify="left"
        ).pack(padx=18, pady=12)

        if page_url:
            ctk.CTkButton(
                bubble, text="📖 Learn more", corner_radius=14, height=30,
                font=self.FONT_SMALL,
                fg_color=self.ACCENT, hover_color=self.ACCENT_DARK,
                command=lambda u=page_url: webbrowser.open(u)
            ).pack(padx=18, pady=(0, 12), anchor="w" if is_astra else "e")

        self.after(50, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        try:
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    # ---- Input bar --------------------------------------------------------
    def build_input_bar(self, parent):
        self.input_frame = ctk.CTkFrame(parent, fg_color=self.BG)
        self.input_frame.grid(row=3, column=0, sticky="ew", padx=16, pady=(6, 16))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_box = ctk.CTkEntry(
            self.input_frame, placeholder_text="Type a command, or tap the mic to speak 🎤...",
            height=52, corner_radius=22, font=self.FONT_CHAT,
            fg_color=self.PANEL_BG, border_color=self.ACCENT_SOFT, text_color=self.TEXT
        )
        self.input_box.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.input_box.bind("<Return>", lambda e: self.handle_input())

        ctk.CTkButton(
            self.input_frame, text="Send", width=90, height=52, corner_radius=22,
            font=self.FONT_BUTTON, fg_color=self.ACCENT, hover_color=self.ACCENT_DARK,
            command=self.handle_input
        ).grid(row=0, column=1, padx=(0, 8))

        ctk.CTkButton(
            self.input_frame, text="🎤 Speak", width=110, height=52, corner_radius=22,
            font=self.FONT_BUTTON, fg_color=self.LAVENDER, hover_color=self.LAVENDER_DARK,
            text_color=self.TEXT, command=self.start_voice
        ).grid(row=0, column=2, padx=(8, 0))

        ctk.CTkButton(
            self.input_frame, text="⛔ Stop", width=100, height=52, corner_radius=22,
            font=self.FONT_BUTTON, fg_color="#FF4D6D", hover_color="#D9354F",
            text_color="#FFFFFF", command=self.stop_everything
        ).grid(row=0, column=3, padx=(8, 0))

    # =====================================================================
    # Clock + orb animation
    # =====================================================================
    def update_clock(self):
        self.clock_label.configure(text=datetime.now().strftime("%I:%M %p"))
        self.after(1000, self.update_clock)

    def animate_orb(self):
        speed_map = {"idle": 0.05, "listening": 0.35, "thinking": 0.25, "speaking": 0.3}
        color_map = {
            "idle": self.ORB_IDLE,
            "listening": self.ORB_LISTENING,
            "thinking": self.ORB_THINKING,
            "speaking": self.ORB_SPEAKING,
        }
        self.angle += speed_map.get(self.mood, 0.05)

        r = 40 + 8 * math.sin(self.angle)
        cx, cy = 75, 75
        self.orb_canvas.coords(self.orb_shape, cx - r, cy - r, cx + r, cy + r)
        self.orb_canvas.itemconfig(self.orb_shape, fill=color_map.get(self.mood, self.ORB_IDLE))

        glow_r = r + 15
        self.orb_canvas.coords(self.orb_glow, cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r)

        self.after(40, self.animate_orb)

    # =====================================================================
    # State / status
    # =====================================================================
    def ui(self, func):
        self.after(0, func)

    def set_state(self, new_state):
        self.mood = new_state
        labels = {
            "idle": "💤 Idle",
            "listening": "🎤 Listening...",
            "thinking": "💭 Thinking...",
            "speaking": "💬 Speaking...",
        }
        self.ui(lambda: self.status_label.configure(text=labels.get(new_state, new_state)))

    def set_response_mode(self, value):
        mapping = {"🗨️ Text + Voice": "both", "💬 Text only": "text"}
        self.response_mode = mapping.get(value, "both")
        if self.response_mode == "text":
            stop_speaking()

    def maybe_speak(self, text):
        if self.stop_requested or self.response_mode == "text":
            return
        self.set_state("speaking")
        speak(text)

    def stop_everything(self):
        self.stop_requested = True
        stop_speaking()
        self.set_state("idle")

    def greet_user(self):
        greeting = "Hello, this is Astra. How can I help you today?"
        self.add_message("Astra", greeting)

        def task():
            self.maybe_speak(greeting)
            self.set_state("idle")

        threading.Thread(target=task, daemon=True).start()

    # =====================================================================
    # Input handling
    # =====================================================================
    def handle_input(self):
        cmd = self.input_box.get().strip()
        self.input_box.delete(0, "end")
        if cmd:
            self.process_command(cmd)

    def start_voice(self):
        self.set_state("listening")
        threading.Thread(target=self.voice_thread, daemon=True).start()

    def voice_thread(self):
        try:
            cmd = listen()
        except Exception as e:
            print("Voice error:", e)
            cmd = None

        self.set_state("idle")
        self.ui(lambda: self.process_command(cmd if cmd else ""))

    def process_command(self, command):
        if not command:
            msg = "I didn't catch that, could you say it again? 🥺"
            self.add_message("Astra", msg)
            threading.Thread(
                target=lambda: (self.maybe_speak(msg), self.set_state("idle")),
                daemon=True
            ).start()
            return

        command = command.lower()
        self.add_message("You", command)

        stop_phrases = {"stop", "stop it", "be quiet", "shut up", "silence", "cancel", "halt"}
        exit_phrases = {"exit", "quit", "bye", "goodbye"}
        first_word = command.split()[0] if command.split() else ""

        if command in stop_phrases or first_word in ("stop", "cancel", "halt"):
            self.stop_everything()
            self.add_message("Astra", "Okay, stopped! ⛔")
            return

        if command in exit_phrases or first_word in ("exit", "quit"):
            self.stop_everything()
            self.stop_requested = False
            self.add_message("Astra", "Goodbye! Talk soon 💕")
            self.maybe_speak("Goodbye! Talk soon.")
            self.after(1200, self.destroy)
            return

        self.stop_requested = False

        if "open" in command:
            name = command.replace("open", "").strip()
            reply = f"Opening {name}"
            self.add_message("Astra", reply)

            def task():
                self.maybe_speak(reply)
                if self.stop_requested:
                    self.set_state("idle")
                    return
                self.set_state("thinking")
                if not open_app(name):
                    open_website(name)
                self.set_state("idle")

            threading.Thread(target=task, daemon=True).start()

        elif "search" in command:
            q = command.replace("search", "").strip()
            reply = f"Searching for {q}"
            self.add_message("Astra", reply)

            def task():
                self.maybe_speak(reply)
                if self.stop_requested:
                    self.set_state("idle")
                    return
                self.set_state("thinking")
                google_search(q)
                self.set_state("idle")

            threading.Thread(target=task, daemon=True).start()

        elif "time" in command:
            now = datetime.now().strftime("%I:%M %p")
            reply = f"It's {now} right now."
            self.add_message("Astra", reply)

            def task():
                self.maybe_speak(reply)
                self.set_state("idle")

            threading.Thread(target=task, daemon=True).start()

        else:
            def task():
                self.set_state("thinking")
                try:
                    answer, page_url = ask_ai(command)
                except Exception:
                    answer, page_url = "Sorry, I ran into an error thinking about that.", None

                if self.stop_requested:
                    self.set_state("idle")
                    return

                self.ui(lambda: self.add_message("Astra", answer, page_url))
                self.maybe_speak(answer)
                self.set_state("idle")

            threading.Thread(target=task, daemon=True).start()


if __name__ == "__main__":
    app = AstraGUI()
    app.mainloop()