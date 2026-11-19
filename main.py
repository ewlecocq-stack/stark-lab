
import customtkinter as ctk
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ==========================================
# STARK LAB V2 - HOLOGRAPHIC ARMOR SYSTEM
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#050A13"
PANEL = "#0B1524"
CYAN = "#00D9FF"
BLUE = "#087EFF"
WHITE = "#EAF8FF"
GREEN = "#00FF99"


class StarkLab(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("STARK LAB | ARMOR DEVELOPMENT")
        self.geometry("1500x900")
        self.minsize(1100, 700)
        self.configure(fg_color=BG)

        self.armor_name = "PROJECT MARK I"
        self.armor_color = "#00D9FF"

        self.energy = 92
        self.armor = 100
        self.power = 85

        self.angle = 35
        self.animation_id = None
        self.armor_canvas = None

        self.create_interface()
        self.update_clock()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    # ======================================
    # INTERFACE PRINCIPALE
    # ======================================

    def create_interface(self):

        header = ctk.CTkFrame(
            self, fg_color=PANEL,
            corner_radius=0, height=75
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="◈ STARK LAB",
            font=("Arial", 28, "bold"),
            text_color=CYAN
        ).pack(side="left", padx=30)

        ctk.CTkLabel(
            header,
            text="ARMOR DEVELOPMENT SYSTEM // V2.0",
            font=("Consolas", 13),
            text_color=WHITE
        ).pack(side="left", padx=20)

        self.clock = ctk.CTkLabel(
            header,
            text="",
            font=("Consolas", 15),
            text_color=CYAN
        )
        self.clock.pack(side="right", padx=30)

        main = ctk.CTkFrame(self, fg_color=BG)
        main.pack(fill="both", expand=True, padx=15, pady=15)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=3)
        main.grid_columnconfigure(2, weight=2)
        main.grid_rowconfigure(0, weight=1)

        # MENU GAUCHE
        menu = ctk.CTkFrame(
            main, fg_color=PANEL,
            corner_radius=15, width=230
        )
        menu.grid(row=0, column=0, sticky="nsew", padx=7)
        menu.grid_propagate(False)

        ctk.CTkLabel(
            menu,
            text="CONTROL CENTER",
            font=("Arial", 17, "bold"),
            text_color=CYAN
        ).pack(pady=25)

        self.menu_button(menu, "⌂  DASHBOARD", self.dashboard)
        self.menu_button(menu, "◈  ARMOR DESIGN", self.design)
        self.menu_button(menu, "⌕  SCANNER", self.scanner)
        self.menu_button(menu, "⚙  SETTINGS", self.settings)

        ctk.CTkLabel(
            menu,
            text="SYSTEM STATUS",
            font=("Arial", 13, "bold"),
            text_color=CYAN
        ).pack(pady=(45, 10))

        ctk.CTkLabel(
            menu,
            text="● SYSTEM ONLINE",
            text_color=GREEN
        ).pack(pady=5)

        ctk.CTkLabel(
            menu,
            text="3D ENGINE: ONLINE",
            text_color=GREEN
        ).pack(pady=5)

        ctk.CTkLabel(
            menu,
            text="MENTOR: STANDBY",
            text_color=GREEN
        ).pack(pady=5)

        # CENTRE
        self.center = ctk.CTkFrame(
            main, fg_color=PANEL, corner_radius=15
        )
        self.center.grid(row=0, column=1, sticky="nsew", padx=7)

        # MENTOR
        right = ctk.CTkFrame(
            main, fg_color=PANEL,
            corner_radius=15, width=330
        )
        right.grid(row=0, column=2, sticky="nsew", padx=7)
        right.grid_propagate(False)

        self.create_center()
        self.create_mentor(right)

    def menu_button(self, parent, text, command):

        ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=48,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#12304A",
            text_color=WHITE,
            anchor="w",
            font=("Arial", 13, "bold")
        ).pack(fill="x", padx=12, pady=6)

    # ======================================
    # CONSTRUCTION ARMURE 3D
    # ======================================

    def add_armor_part(self, ax, center, size, color):

        x, y, z = center
        sx, sy, sz = [v / 2 for v in size]

        vertices = [
            (x-sx, y-sy, z-sz),
            (x+sx, y-sy, z-sz),
            (x+sx, y+sy, z-sz),
            (x-sx, y+sy, z-sz),
            (x-sx, y-sy, z+sz),
            (x+sx, y-sy, z+sz),
            (x+sx, y+sy, z+sz),
            (x-sx, y+sy, z+sz)
        ]

        faces = [
            [vertices[i] for i in face]
            for face in [
                [0, 1, 2, 3],
                [4, 5, 6, 7],
                [0, 1, 5, 4],
                [2, 3, 7, 6],
                [1, 2, 6, 5],
                [0, 3, 7, 4]
            ]
        ]

        mesh = Poly3DCollection(
            faces,
            facecolors=color,
            edgecolors="#8DEBFF",
            linewidths=0.7,
            alpha=0.95
        )

        ax.add_collection3d(mesh)

    def draw_armor(self, ax):

        c = self.armor_color

        # TORSE
        self.add_armor_part(
            ax, (0, 0, 2.25),
            (0.95, 0.48, 1.05), c
        )

        # CASQUE
        self.add_armor_part(
            ax, (0, 0, 3.15),
            (0.55, 0.48, 0.62), c
        )

        # VISIERE
        self.add_armor_part(
            ax, (0, -0.25, 3.17),
            (0.38, 0.04, 0.12), "#D9FFFF"
        )

        # PLAQUE TORSE
        self.add_armor_part(
            ax, (0, -0.27, 2.65),
            (0.78, 0.06, 0.25), "#B5D9E8"
        )

        # REACTEUR CENTRAL
        ax.scatter(
            [0], [-0.34], [2.3],
            color="#FFFFFF",
            s=190,
            edgecolors=CYAN,
            linewidths=3,
            depthshade=False
        )

        # EPAULES
        for x in [-0.68, 0.68]:
            self.add_armor_part(
                ax, (x, 0, 2.7),
                (0.42, 0.55, 0.45), c
            )

        # BRAS
        for x in [-0.78, 0.78]:

            self.add_armor_part(
                ax, (x, 0, 2.15),
                (0.32, 0.4, 0.75), c
            )

            self.add_armor_part(
                ax, (x, 0, 1.65),
                (0.35, 0.4, 0.3), "#B5D9E8"
            )

        # JAMBES
        for x in [-0.28, 0.28]:

            self.add_armor_part(
                ax, (x, 0, 1.1),
                (0.38, 0.45, 0.85), c
            )

            self.add_armor_part(
                ax, (x, -0.08, 0.45),
                (0.42, 0.65, 0.35), "#B5D9E8"
            )

    # ======================================
    # AFFICHAGE 3D
    # ======================================

    def create_center(self):

        ctk.CTkLabel(
            self.center,
            text="HOLOGRAPHIC ARMOR VISUALIZATION",
            font=("Arial", 20, "bold"),
            text_color=CYAN
        ).pack(pady=(15, 5))

        self.armor_display = ctk.CTkFrame(
            self.center,
            fg_color="#07101D",
            corner_radius=15,
            border_width=1,
            border_color="#145477"
        )

        self.armor_display.pack(
            fill="both", expand=True,
            padx=15, pady=10
        )

        figure = Figure(figsize=(5, 5), dpi=90)
        figure.patch.set_facecolor("#07101D")

        self.armor_ax = figure.add_subplot(
            111, projection="3d"
        )

        ax = self.armor_ax
        ax.set_facecolor("#07101D")

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_zlim(0, 3.8)

        ax.set_box_aspect((1, 1, 1.5))
        ax.set_axis_off()

        ax.view_init(elev=12, azim=self.angle)

        self.draw_armor(ax)

        self.armor_canvas = FigureCanvasTkAgg(
            figure, master=self.armor_display
        )

        self.armor_canvas.draw()

        self.armor_canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

        # ROTATION A LA SOURIS
        self.armor_canvas.mpl_connect(
            "motion_notify_event",
            self.mouse_rotate
        )

        self.armor_label = ctk.CTkLabel(
            self.armor_display,
            text=f"{self.armor_name} // 3D MODEL",
            font=("Consolas", 13),
            text_color=CYAN
        )

        self.armor_label.pack(pady=5)

        ctk.CTkLabel(
            self.armor_display,
            text="DRAG WITH MOUSE TO ROTATE",
            font=("Consolas", 10),
            text_color="#66889D"
        ).pack(pady=5)

        self.create_stats()

        self.animation_id = self.after(
            100, self.animate_armor
        )

    def mouse_rotate(self, event):

        if event.button == 1 and event.inaxes == self.armor_ax:
            self.angle = self.armor_ax.azim
            self.armor_canvas.draw_idle()

    def animate_armor(self):

        if self.armor_canvas is None:
            return

        try:
            if not self.armor_canvas.get_tk_widget().winfo_exists():
                return

            self.angle = (self.angle + 0.4) % 360

            self.armor_ax.view_init(
                elev=12, azim=self.angle
            )

            self.armor_canvas.draw_idle()

            self.animation_id = self.after(
                80, self.animate_armor
            )

        except Exception:
            self.animation_id = None

    # ======================================
    # STATISTIQUES
    # ======================================

    def create_stats(self):

        stats = ctk.CTkFrame(
            self.center, fg_color="transparent"
        )

        stats.pack(fill="x", padx=15, pady=15)

        self.add_stat(stats, "ENERGY", self.energy, 0)
        self.add_stat(stats, "STRUCTURE", self.armor, 1)
        self.add_stat(stats, "SYSTEM", self.power, 2)

    def add_stat(self, parent, name, value, column):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#101F32",
            corner_radius=10
        )

        frame.grid(
            row=0, column=column,
            sticky="ew", padx=5
        )

        parent.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            frame, text=name,
            text_color=CYAN,
            font=("Arial", 12, "bold")
        ).pack(pady=(12, 5))

        ctk.CTkLabel(
            frame,
            text=f"{value}%",
            text_color=WHITE,
            font=("Arial", 23, "bold")
        ).pack(pady=(0, 12))

    # ======================================
    # MENTOR IA
    # ======================================

    def create_mentor(self, parent):

        ctk.CTkLabel(
            parent,
            text="◈ MENTOR AI",
            font=("Arial", 20, "bold"),
            text_color=CYAN
        ).pack(pady=20)

        ctk.CTkLabel(
            parent,
            text="PERSONAL DEVELOPMENT ASSISTANT",
            font=("Consolas", 10),
            text_color="#7896AC"
        ).pack(pady=5)

        self.chat = ctk.CTkTextbox(
            parent,
            fg_color="#07101D",
            text_color=WHITE,
            corner_radius=10,
            font=("Consolas", 12),
            wrap="word"
        )

        self.chat.pack(
            fill="both", expand=True,
            padx=12, pady=12
        )

        self.chat.insert(
            "end",
            "MENTOR AI: Connection established.\n\n"
            "Welcome to Stark Lab.\n"
            "Your armor development system is ready.\n\n"
            "What are we building today?\n\n"
        )

        self.chat.configure(state="disabled")

        self.message = ctk.CTkEntry(
            parent,
            placeholder_text="Talk to your mentor...",
            height=45
        )

        self.message.pack(fill="x", padx=12, pady=5)

        self.message.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        ctk.CTkButton(
            parent,
            text="SEND MESSAGE",
            command=self.send_message,
            fg_color=BLUE,
            height=40
        ).pack(fill="x", padx=12, pady=(5, 15))

    def send_message(self):

        message = self.message.get().strip()

        if not message:
            return

        self.chat.configure(state="normal")
        self.chat.insert("end", f"\nYOU: {message}\n")

        text = message.lower()

        if "bonjour" in text or "salut" in text:
            answer = "Bonjour ! Le laboratoire est opérationnel."

        elif "armure" in text or "costume" in text:
            answer = "Commençons par définir le style de ton armure."

        elif "energie" in text or "énergie" in text:
            answer = f"Énergie actuelle : {self.energy}%."

        elif "aide" in text:
            answer = "Je peux t'aider à concevoir ton armure et organiser ses modules."

        elif "nom" in text:
            answer = "Tu peux modifier le nom dans ARMOR DESIGN."

        elif "scanner" in text:
            answer = "Le scanner est disponible dans le menu de gauche."

        else:
            answer = "Intéressant. Développons cette idée ensemble."

        self.chat.insert(
            "end", f"\nMENTOR AI: {answer}\n"
        )

        self.chat.see("end")
        self.chat.configure(state="disabled")

        self.message.delete(0, "end")

    # ======================================
    # GESTION DES PAGES
    # ======================================

    def clear_center(self):

        if self.animation_id is not None:
            try:
                self.after_cancel(self.animation_id)
            except Exception:
                pass

        self.animation_id = None
        self.armor_canvas = None

        for widget in self.center.winfo_children():
            widget.destroy()

    def dashboard(self):

        self.clear_center()
        self.create_center()

    # ======================================
    # CONCEPTION ARMURE
    # ======================================

    def design(self):

        self.clear_center()

        ctk.CTkLabel(
            self.center,
            text="ARMOR DESIGN STUDIO",
            font=("Arial", 23, "bold"),
            text_color=CYAN
        ).pack(pady=35)

        ctk.CTkLabel(
            self.center,
            text="ARMOR PROJECT NAME",
            text_color=WHITE
        ).pack(pady=10)

        name = ctk.CTkEntry(
            self.center,
            width=300,
            placeholder_text="Enter armor name..."
        )

        name.pack(pady=10)
        name.insert(0, self.armor_name)

        ctk.CTkLabel(
            self.center,
            text="ARMOR COLOR",
            text_color=WHITE
        ).pack(pady=10)

        color = ctk.CTkOptionMenu(
            self.center,
            values=["Cyan", "Red", "Gold", "Purple", "White"]
        )

        color.pack(pady=10)

        color_codes = {
            "Cyan": "#00D9FF",
            "Red": "#FF3344",
            "Gold": "#FFD700",
            "Purple": "#A855F7",
            "White": "#EAF8FF"
        }

        ctk.CTkLabel(
            self.center,
            text="DESIGN MODULE // CONFIGURATION",
            text_color="#66889D",
            font=("Consolas", 12)
        ).pack(pady=30)

        def save():

            self.armor_name = name.get().strip() or "NEW PROJECT"
            self.armor_color = color_codes[color.get()]

            self.dashboard()

            self.show_message(
                "PROJECT SAVED",
                f"{self.armor_name} has been updated."
            )

        ctk.CTkButton(
            self.center,
            text="SAVE ARMOR PROJECT",
            command=save,
            fg_color=BLUE,
            width=250,
            height=45
        ).pack(pady=25)

    # ======================================
    # SCANNER
    # ======================================

    def scanner(self):

        self.clear_center()

        ctk.CTkLabel(
            self.center,
            text="HOLOGRAPHIC SCANNER",
            font=("Arial", 23, "bold"),
            text_color=CYAN
        ).pack(pady=40)

        result = ctk.CTkLabel(
            self.center,
            text="SCANNER STANDBY",
            font=("Consolas", 18),
            text_color=GREEN
        )

        result.pack(pady=40)

        def scan():

            result.configure(
                text=(
                    "SCAN COMPLETE\n\n"
                    f"PROJECT: {self.armor_name}\n"
                    f"COLOR: {self.armor_color}\n"
                    f"ENERGY: {self.energy}%\n"
                    f"STRUCTURE: {self.armor}%\n"
                    "STATUS: OPERATIONAL"
                )
            )

        ctk.CTkButton(
            self.center,
            text="START SCAN",
            command=scan,
            fg_color=BLUE,
            width=220,
            height=50
        ).pack(pady=20)

    # ======================================
    # PARAMETRES
    # ======================================

    def settings(self):

        self.clear_center()

        ctk.CTkLabel(
            self.center,
            text="SYSTEM SETTINGS",
            font=("Arial", 24, "bold"),
            text_color=CYAN
        ).pack(pady=40)

        ctk.CTkLabel(
            self.center,
            text=(
                "STARK LAB V2.0\n\n"
                "INTERFACE: ONLINE\n"
                "3D ENGINE: MATPLOTLIB\n"
                "MENTOR: SIMULATED AI\n"
                "ARMOR SYSTEM: READY\n"
                "ANIMATION: ACTIVE"
            ),
            font=("Consolas", 15),
            text_color=WHITE
        ).pack(pady=30)

    # ======================================
    # FENETRES
    # ======================================

    def show_message(self, title, message):

        dialog = ctk.CTkToplevel(self)

        dialog.title(title)
        dialog.geometry("400x180")
        dialog.configure(fg_color=PANEL)
        dialog.transient(self)

        ctk.CTkLabel(
            dialog,
            text=title,
            font=("Arial", 18, "bold"),
            text_color=CYAN
        ).pack(pady=20)

        ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=350
        ).pack(pady=10)

    # ======================================
    # HORLOGE
    # ======================================

    def update_clock(self):

        self.clock.configure(
            text=datetime.now().strftime(
                "%d/%m/%Y  %H:%M:%S"
            )
        )

        self.after(1000, self.update_clock)

    def close_app(self):

        if self.animation_id is not None:
            try:
                self.after_cancel(self.animation_id)
            except Exception:
                pass

        self.destroy()


# ==========================================
# START SYSTEM
# ==========================================

if __name__ == "__main__":

    app = StarkLab()
    app.mainloop()
