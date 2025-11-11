import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import date
from firebase_realtime import initialize_firebase  # Import Firebase initialization
from firebase_admin import db  # Import Firebase database functions
from utils.appointments import (
    add_appointment,
    get_todays_appointments,
    get_all_appointments,
    delete_appointment
)
from utils.patients import (
    get_all_patients,
    load_patient,
    add_patient_visit,
    delete_patient
)
from utils.export_pdf import export_patient_to_pdf


class ModernPearlTrack:
    def __init__(self, root):
        self.root = root
        self.root.title("PearlTrack - Dental Filing System")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f8fbff")
        self.root.state('zoomed')  # Maximize window
        
        # Initialize Firebase
        initialize_firebase()  # Ensure Firebase is initialized

        # Modern dental color scheme
        self.colors = {
            'primary': '#0ea5e9',
            'primary_dark': '#0284c7',
            'primary_light': '#e0f2fe', 
            'secondary': '#10b981',
            'secondary_light': '#d1fae5',
            'background': '#f8fafc',
            'card': '#ffffff',
            'text': '#1e293b',
            'text_light': '#64748b',
            'border': '#e2e8f0',
            'accent': '#f97316',
            'success': '#22c55e',
            'danger': '#ef4444'
        }
        
        # Professional fonts - optimized sizes
        self.fonts = {
            'title': font.Font(family="Segoe UI", size=20, weight="bold"),
            'heading': font.Font(family="Segoe UI", size=14, weight="bold"),
            'subheading': font.Font(family="Segoe UI", size=11, weight="bold"),
            'body': font.Font(family="Segoe UI", size=9),
            'small': font.Font(family="Segoe UI", size=8),
            'button': font.Font(family="Segoe UI", size=9, weight="bold")
        }
        
        self.setup_styles()
        self.status_label = None
        self.setup_ui()

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Primary button style
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=self.fonts['button'],
                       padding=(20, 10))
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_dark']),
                             ('pressed', self.colors['primary_dark'])])
        
        # Secondary button
        style.configure('Secondary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=self.fonts['button'],
                       padding=(20, 10))
        
        # Danger button
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=self.fonts['button'],
                       padding=(15, 8))
        
        # Navigation button style
        style.configure('Nav.TButton',
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       borderwidth=1,
                       relief='flat',
                       focuscolor='none',
                       font=self.fonts['body'],
                       padding=(15, 12))
        style.map('Nav.TButton',
                 background=[('active', self.colors['primary_light'])])


    def create_modern_card(self, parent, title="", padding=25):
        """Create a modern card with shadow effect"""
        # Outer frame for shadow effect
        shadow_frame = tk.Frame(parent, bg='#d1d5db', height=2)
        
        # Main card frame
        card = tk.Frame(shadow_frame, bg=self.colors['card'], relief='flat')
        card.pack(fill='both', expand=True, padx=1, pady=1)
        
        if title:
            # Title section with bottom border
            title_frame = tk.Frame(card, bg=self.colors['card'], height=60)
            title_frame.pack(fill='x')
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(title_frame, text=title, font=self.fonts['heading'],
                                 bg=self.colors['card'], fg=self.colors['text'])
            title_label.pack(anchor='w', padx=padding, pady=15)
            
            # Separator line
            separator = tk.Frame(card, bg=self.colors['border'], height=1)
            separator.pack(fill='x', padx=padding)
            
        return card, shadow_frame

    def create_stat_card(self, parent, title, value, subtitle, icon_text, color):
        """Create a beautiful statistics card"""
        card_content, shadow_frame = self.create_modern_card(parent)
        shadow_frame.configure(width=280, height=140)
        shadow_frame.pack_propagate(False)
        
        # Content frame
        content = tk.Frame(card_content, bg=self.colors['card'])
        content.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Top row with icon and value
        top_frame = tk.Frame(content, bg=self.colors['card'])
        top_frame.pack(fill='x')
        
        # Icon
        icon_frame = tk.Frame(top_frame, bg=color, width=50, height=50)
        icon_frame.pack(side='left')
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(icon_frame, text=icon_text, font=('Arial', 20),
                            bg=color, fg='white')
        icon_label.pack(expand=True)
        
        # Value
        value_label = tk.Label(top_frame, text=str(value), font=self.fonts['title'],
                             bg=self.colors['card'], fg=self.colors['text'])
        value_label.pack(side='right')
        
        # Title and subtitle
        title_label = tk.Label(content, text=title, font=self.fonts['subheading'],
                             bg=self.colors['card'], fg=self.colors['text'])
        title_label.pack(anchor='w', pady=(15, 2))
        
        subtitle_label = tk.Label(content, text=subtitle, font=self.fonts['small'],
                                bg=self.colors['card'], fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w')
        
        return shadow_frame

    def setup_ui(self):
        # Create main scrollable canvas
        self.main_canvas = tk.Canvas(self.root, bg=self.colors['background'], highlightthickness=0)
        self.main_scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg=self.colors['background'])
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        
        # Pack canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel scrolling
        self.bind_mouse_wheel()
        
        # Main container with padding (now inside scrollable frame)
        main_container = tk.Frame(self.scrollable_frame, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Navigation section
        self.create_navigation(main_container)
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg=self.colors['background'])
        self.content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Show dashboard by default
        self.show_dashboard()

    def bind_mouse_wheel(self):
        """Bind mouse wheel scrolling to canvas"""
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.main_canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse wheel events
        self.main_canvas.bind('<Enter>', _bind_to_mousewheel)
        self.main_canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Handle canvas resizing
        self.main_canvas.bind('<Configure>', self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        """Handle canvas resize to make frame width match canvas width"""
        canvas_width = event.width
        self.main_canvas.itemconfig(self.main_canvas.find_all()[0], width=canvas_width)

    def create_header(self, parent):
        """Create professional header"""
        header = tk.Frame(parent, bg=self.colors['card'], height=100)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        # Add subtle shadow
        shadow = tk.Frame(parent, bg='#d1d5db', height=2)
        shadow.place(in_=header, x=0, rely=1.0, relwidth=1.0)
        
        # Content frame
        header_content = tk.Frame(header, bg=self.colors['card'])
        header_content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header_content, bg=self.colors['card'])
        left_frame.pack(side='left', fill='y')
        
        # Logo background
        logo_bg = tk.Frame(left_frame, bg=self.colors['primary'], width=60, height=60)
        logo_bg.pack(side='left', padx=(0, 20))
        logo_bg.pack_propagate(False)
        
        logo_label = tk.Label(logo_bg, text="🦷", font=('Arial', 30), bg=self.colors['primary'])
        logo_label.pack(expand=True)
        
        # Title section
        title_frame = tk.Frame(left_frame, bg=self.colors['card'])
        title_frame.pack(side='left', fill='y')
        
        title_label = tk.Label(title_frame, text="PearlTrack", font=self.fonts['title'],
                             bg=self.colors['card'], fg=self.colors['text'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Professional Dental Filing System", 
                                font=self.fonts['body'],
                                bg=self.colors['card'], fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w')
        
        # Right side - Date and practice info
        right_frame = tk.Frame(header_content, bg=self.colors['card'])
        right_frame.pack(side='right', fill='y')
        
        date_label = tk.Label(right_frame, text=f"Today: {date.today().strftime('%B %d, %Y')}", 
                            font=self.fonts['body'],
                            bg=self.colors['card'], fg=self.colors['text'])
        date_label.pack(anchor='e')
        
        practice_label = tk.Label(right_frame, text="Dr. Jack's Dental Practice", 
                                font=self.fonts['small'],
                                bg=self.colors['card'], fg=self.colors['text_light'])
        practice_label.pack(anchor='e')

    def create_navigation(self, parent):
        """Create modern navigation bar"""
        nav_frame = tk.Frame(parent, bg=self.colors['background'])
        nav_frame.pack(fill='x', pady=(0, 20))
        
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard, 'Primary'),
            ("📅 Appointments", self.show_appointments, 'Nav'),
            ("👥 Patient Records", self.show_patients, 'Nav'),
            ("📊 Export Reports", self.show_export, 'Nav')
        ]
        
        for text, command, style in nav_buttons:
            btn = ttk.Button(nav_frame, text=text, command=command, style=f'{style}.TButton')
            btn.pack(side='left', padx=(0, 15))

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.status_label:
            self.status_label.destroy()
            self.status_label = None

    def show_dashboard(self):
        self.clear_content()
        
        # Welcome section
        welcome_content, welcome_shadow = self.create_modern_card(self.content_frame, 
                                                                 "Welcome to PearlTrack Dental Suite")
        welcome_shadow.pack(fill='x', pady=(0, 30))
        
        welcome_text = tk.Label(welcome_content, 
                              text="Streamline your dental practice with our comprehensive management system.\n"
                                   "Track appointments, manage patient records, and generate reports with ease.",
                              font=self.fonts['body'], bg=self.colors['card'], fg=self.colors['text_light'],
                              wraplength=1000, justify='center')
        welcome_text.pack(pady=25, padx=25)
        
        # Statistics section
        stats_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        stats_frame.pack(fill='x', pady=(0, 30))
        
        # Get real data
        total_patients = len(get_all_patients())
        total_today = len(get_todays_appointments())
        total_all = len(get_all_appointments())
        
        stats_data = [
            ("Total Patients", total_patients, f"{total_patients} registered", "👥", self.colors['primary']),
            ("Today's Appointments", total_today, f"{total_today} scheduled today", "📅", self.colors['secondary']),
            ("All Appointments", total_all, f"{total_all} total appointments", "🕒", self.colors['accent']),
            ("Active Status", "Online", "System operational", "✅", self.colors['success'])
        ]
        
        for title, value, subtitle, icon, color in stats_data:
            card = self.create_stat_card(stats_frame, title, value, subtitle, icon, color)
            card.pack(side='left', padx=15)
        
        # Recent activity section
        activity_content, activity_shadow = self.create_modern_card(self.content_frame, 
                                                                   "Recent Activity")
        activity_shadow.pack(fill='both', expand=True)
        
        # Activity list
        activity_frame = tk.Frame(activity_content, bg=self.colors['card'])
        activity_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        activities = [
            "System started successfully",
            f"Loaded {total_patients} patient records",
            f"Found {total_today} appointments for today",
            "Ready for patient management"
        ]
        
        for activity in activities:
            activity_item = tk.Frame(activity_frame, bg=self.colors['primary_light'], height=40)
            activity_item.pack(fill='x', pady=2)
            activity_item.pack_propagate(False)
            
            activity_label = tk.Label(activity_item, text=f"• {activity}", font=self.fonts['body'],
                                    bg=self.colors['primary_light'], fg=self.colors['text'])
            activity_label.pack(anchor='w', padx=15, pady=10)

    def show_appointments(self):
        self.clear_content()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="📅 Appointment Management", font=self.fonts['title'],
                             bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Schedule and manage patient appointments", 
                                font=self.fonts['body'],
                                bg=self.colors['background'], fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Main container
        main_container = tk.Frame(self.content_frame, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True)
        
        # Left side - Add appointment form
        form_content, form_shadow = self.create_modern_card(main_container, "New Appointment")
        form_shadow.pack(side='left', fill='y', padx=(0, 15))
        form_shadow.configure(width=450)
        
        # Form frame
        form_frame = tk.Frame(form_content, bg=self.colors['card'])
        form_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Form fields
        fields = [
            ("Patient Name", "text"),
            ("Contact","text"),
            ("Reason for Visit", "text"), 
            ("Date (YYYY-MM-DD)", "text"),
            ("Time (HH:MM)", "text")
        ]
        
        self.appointment_entries = {}
        
        for field_name, field_type in fields:
            tk.Label(form_frame, text=field_name, font=self.fonts['subheading'],
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(15, 5))
            
            entry = tk.Entry(form_frame, font=self.fonts['body'], relief='solid', bd=1,
                           highlightthickness=2, highlightcolor=self.colors['primary'])
            entry.pack(fill='x', ipady=8, pady=(0, 5))
            self.appointment_entries[field_name] = entry
        
        # Set default date
        self.appointment_entries["Date (YYYY-MM-DD)"].insert(0, date.today().isoformat())
        
        # Add button
        ttk.Button(form_frame, text="➕ Add Appointment", style='Primary.TButton',
                  command=self.add_appointment_clicked).pack(pady=20, fill='x')
        
        # Right side - Appointments list
        list_content, list_shadow = self.create_modern_card(main_container, "Scheduled Appointments")
        list_shadow.pack(side='right', fill='both', expand=True)
        
        # List frame
        list_frame = tk.Frame(list_content, bg=self.colors['card'])
        list_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Scrollable listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.appointments_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                             font=self.fonts['body'], relief='flat',
                                             selectbackground=self.colors['primary_light'],
                                             highlightthickness=1, 
                                             highlightcolor=self.colors['primary'])
        self.appointments_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.appointments_listbox.yview)
        
        # Button frame
        button_frame = tk.Frame(list_content, bg=self.colors['card'])
        button_frame.pack(fill='x', padx=25, pady=(0, 20))
        
        ttk.Button(button_frame, text="🗑 Delete Selected", style='Danger.TButton',
                  command=self.delete_appointment_clicked).pack(side='right')
        self.load_appointments()


    def add_appointment_clicked(self):
        try:
             
            name = self.appointment_entries["Patient Name"].get().strip()
            contact = self.appointment_entries["Contact"].get().strip()
            reason = self.appointment_entries["Reason for Visit"].get().strip()
            date_str = self.appointment_entries["Date (YYYY-MM-DD)"].get().strip()
            time_str = self.appointment_entries["Time (HH:MM)"].get().strip()

            if not all([name, contact, reason, date_str, time_str]):

              messagebox.showerror("Error", "Please fill in all fields")
              return

            # Save to database
            add_appointment(name, contact, reason, date_str, time_str)

            # Refresh the list
            self.load_appointments()

            # Clear form
            for field in self.appointment_entries.values():
               field.delete(0, 'end')

            # Reset default date
            self.appointment_entries["Date (YYYY-MM-DD)"].insert(0, date.today().isoformat())

            messagebox.showinfo("Success", "Appointment added successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add appointment:\n{e}")


    def delete_appointment_clicked(self):
        selection = self.appointments_listbox.curselection()
        if selection:
            try:
                index = selection[0]
                appointments = get_all_appointments()
                if index < len(appointments):
                    appointment_id = appointments[index][0]
                    delete_appointment(appointment_id)
                    self.load_appointments()
                    messagebox.showinfo("Success", "Appointment deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete appointment: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select an appointment to delete")

    def load_appointments(self):
        self.appointments_listbox.delete(0, 'end')
        try:
            appointments = get_all_appointments()
            for appointment in appointments:
                id_, name, contact, reason, date_, time_ = appointment
                display_text = f"{date_} {time_} - {name} ({reason} {contact})"
                self.appointments_listbox.insert('end', display_text)
        except Exception as e:
            print(f"Error loading appointments: {e}")

    def show_patients(self):
        self.clear_content()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="👥 Patient Records", font=self.fonts['title'],
                             bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Manage patient visits, treatments, and billing records", 
                                font=self.fonts['body'],
                                bg=self.colors['background'], fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Main container with three columns
        main_container = tk.Frame(self.content_frame, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True)
        
        # Left column - Patient search and list
        left_content, left_shadow = self.create_modern_card(main_container, "Patient Search")
        left_shadow.pack(side='left', fill='y', padx=(0, 10))
        left_shadow.configure(width=350)
        
        left_frame = tk.Frame(left_content, bg=self.colors['card'])
        left_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Search entry
        tk.Label(left_frame, text="Search Patient:", font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = tk.Entry(left_frame, textvariable=self.search_var, font=self.fonts['body'],
                               relief='solid', bd=1, highlightthickness=2, 
                               highlightcolor=self.colors['primary'])
        search_entry.pack(fill='x', ipady=8, pady=(0, 15))
        
        # Patient listbox
        tk.Label(left_frame, text="Patients:", font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(0, 5))
        
        scrollbar1 = tk.Scrollbar(left_frame)
        scrollbar1.pack(side='right', fill='y')
        
        self.patient_listbox = tk.Listbox(left_frame, yscrollcommand=scrollbar1.set,
                                        font=self.fonts['body'], relief='flat',
                                        selectbackground=self.colors['primary_light'],
                                        highlightthickness=1, 
                                        highlightcolor=self.colors['primary'])
        self.patient_listbox.pack(fill='both', expand=True)
        self.patient_listbox.bind('<<ListboxSelect>>', self.on_patient_select)
        scrollbar1.config(command=self.patient_listbox.yview)
        
        # Middle column - Visit history
        middle_content, middle_shadow = self.create_modern_card(main_container, "Visit History")
        middle_shadow.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        middle_frame = tk.Frame(middle_content, bg=self.colors['card'])
        middle_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.history_text = tk.Text(middle_frame, font=self.fonts['body'], relief='flat',
                                   wrap='word', highlightthickness=1,
                                   highlightcolor=self.colors['primary'])
        self.history_text.pack(fill='both', expand=True)
        
        # Right column - Add visit form
        right_content, right_shadow = self.create_modern_card(main_container, "Add Patient:")
        right_shadow.pack(side='right', fill='y')
        right_shadow.configure(width=350)
        
        right_frame = tk.Frame(right_content, bg=self.colors['card'])
        right_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Form fields
        patient_fields = ["Patient Name","Age","Gender","Contact","Next of Kin","Chief Complain","Hpc","Pdh","Pmh","Diagnosis", "Treatment","Management", "Amount Charged","Medicine" ,"Amount Paid"]
        self.patient_entries = {}
        
        for field in patient_fields:
            tk.Label(right_frame, text=field + ":", font=self.fonts['subheading'],
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=(10, 2))
            
            entry = tk.Entry(right_frame, font=self.fonts['body'], relief='solid', bd=1,
                           highlightthickness=2, highlightcolor=self.colors['primary'])
            entry.pack(fill='x', ipady=8, pady=(0, 5))
            self.patient_entries[field] = entry
        
        # Buttons
        button_frame = tk.Frame(right_frame, bg=self.colors['card'])
        button_frame.pack(fill='x', pady=20)
        
        ttk.Button(button_frame, text="➕ Add Visit", style='Primary.TButton',
                  command=self.add_visit_clicked).pack(fill='x', pady=2)
        
        ttk.Button(button_frame, text="🗑 Delete Patient", style='Danger.TButton',
                  command=self.delete_patient_clicked).pack(fill='x', pady=2)
        
        ttk.Button(button_frame, text="📄 Export PDF", style='Secondary.TButton',
                  command=self.export_patient_clicked).pack(fill='x', pady=2)
        
        self.load_patients()

    def on_search_change(self, *args):
        search_term = self.search_var.get().lower()
        self.patient_listbox.delete(0, 'end')
        
        try:
            all_patients = get_all_patients()
            filtered_patients = [p for p in all_patients if search_term in p.lower()]
            for patient in filtered_patients:
                self.patient_listbox.insert('end', patient)
        except Exception as e:
            print(f"Error filtering patients: {e}")

    def on_patient_select(self, event):
        selection = self.patient_listbox.curselection()
        if selection:
            patient_name = self.patient_listbox.get(selection[0])
            self.show_patient_history(patient_name)

    def show_patient_history(self, patient_name):
        self.history_text.delete('1.0', 'end')
        try:
            patient_data = load_patient(patient_name)
            if patient_data and 'records' in patient_data:
                history = f"Patient: {patient_name}\n{'='*50}\n\n"
            
                total_charged = 0
                total_paid = 0
            
                for record in patient_data['records']:
                # Only display filled fields
                    if record.get('age'):
                        history += f"Age: {record['age']}\n"
                    if record.get('gender'):
                        history += f"Gender: {record['gender']}\n"
                    if record.get('contact'):
                        history += f"Contact: {record['contact']}\n"
                    if record.get('next_of_kin'):
                        history += f"Next of kin: {record['next_of_kin']}\n"
                    if record.get('chief_complain'):
                        history += f"Chief Complain: {record['chief_complain']}\n"
                    if record.get('hpc'):
                        history += f"Hpc: {record['hpc']}\n"
                    if record.get('pdh'):
                        history += f"Pdh: {record['pdh']}\n"
                    if record.get('pmh'):
                        history += f"Pmh: {record['pmh']}\n"
                    if record.get('diagnosis'):
                        history += f"Diagnosis: {record['diagnosis']}\n"
                    if record.get('treatment'):
                        history += f"Treatment: {record['treatment']}\n"
                    if record.get('management'):
                        history += f"Management: {record['management']}\n"
                    if record.get('amount_charged'):
                        history += f"Charged: Ksh{record['amount_charged']:.2f}\n"
                    if record.get('amount_paid'):
                        history += f"Paid: Ksh{record['amount_paid']:.2f}\n"
                    if record.get('balance'):
                        history += f"Balance: Ksh{record['balance']:.2f}\n"
                    if record.get('medication'):
                        history += f"Medication: {record['medication']}\n"
                    history += "-" * 30 + "\n\n"
                
                    total_charged += record.get('amount_charged', 0)
                    total_paid += record.get('amount_paid', 0)
            
                history += f"\nTOTALS:\n"
                history += f"Total Charged: Ksh{total_charged:.2f}\n"
                history += f"Total Paid: Ksh{total_paid:.2f}\n"
                history += f"Outstanding Balance: Ksh{total_charged - total_paid:.2f}\n"
            
                self.history_text.insert('1.0', history)

        except Exception as e:
            self.history_text.insert('1.0', f"Error loading patient data: {str(e)}")

  

    def add_visit_clicked(self):
        try:
        # Retrieve values from entries, allowing for empty fields
            name = self.patient_entries["Patient Name"].get().strip()
            age = self.patient_entries["Age"].get().strip() or None
            gender = self.patient_entries["Gender"].get().strip() or None
            contact = self.patient_entries["Contact"].get().strip() or None
            next_of_kin = self.patient_entries["Next of Kin"].get().strip() or None
            chief_complain = self.patient_entries["Chief Complain"].get().strip() or None
            hpc = self.patient_entries["Hpc"].get().strip() or None
            pdh = self.patient_entries["Pdh"].get().strip() or None
            pmh = self.patient_entries["Pmh"].get().strip() or None
            diagnosis = self.patient_entries["Diagnosis"].get().strip() or None
            treatment = self.patient_entries["Treatment"].get().strip() or None
            management = self.patient_entries["Management"].get().strip() or None
            charged_str = self.patient_entries["Amount Charged"].get().strip() or "0"
            medicine = self.patient_entries["Medicine"].get().strip() or None
            paid_str = self.patient_entries["Amount Paid"].get().strip() or "0"
        
            charged = float(charged_str)
            paid = float(paid_str)
            balance = charged - paid
        
        # Save the patient visit with potentially empty fields
            add_patient_visit(name, age, gender, contact, next_of_kin, chief_complain, hpc, pdh, pmh, diagnosis, treatment, management, charged, medicine, paid, balance)
        
        # Clear form
            for entry in self.patient_entries.values():
                entry.delete(0, 'end')
        
        # Reload patient list and refresh history if the same patient is selected
            self.load_patients()
            selection = self.patient_listbox.curselection()
            if selection:
                selected_patient = self.patient_listbox.get(selection[0])
                if selected_patient == name:
                    self.show_patient_history(name)
        
            messagebox.showinfo("Success", "Patient visit added successfully!")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for amounts")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add visit: {str(e)}")

    def delete_patient_clicked(self):
        selection = self.patient_listbox.curselection()
        if selection:
            patient_name = self.patient_listbox.get(selection[0])
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all records for {patient_name}?"):
                try:
                    delete_patient(patient_name)
                    self.load_patients()
                    self.history_text.delete('1.0', 'end')
                    messagebox.showinfo("Success", "Patient deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a patient to delete")

    def export_patient_clicked(self):
        selection = self.patient_listbox.curselection()
        if selection:
            patient_name = self.patient_listbox.get(selection[0])
            try:
                file_path = export_patient_to_pdf(patient_name)
                if file_path:
                    messagebox.showinfo("Success", f"Patient record exported successfully!\nSaved to: {file_path}")
                else:
                    messagebox.showerror("Error", "Failed to export patient record")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a patient to export")

    def load_patients(self):
        self.patient_listbox.delete(0, 'end')
        try:
            patients = get_all_patients()
            for patient in patients:
                self.patient_listbox.insert('end', patient)
        except Exception as e:
            print(f"Error loading patients: {e}")

    def show_export(self):
        self.clear_content()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="📊 Export Patient Records", font=self.fonts['title'],
                             bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Generate PDF reports for patient records", 
                                font=self.fonts['body'],
                                bg=self.colors['background'], fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Center the export card
        center_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        center_frame.pack(expand=True, fill='both')
        
        export_content, export_shadow = self.create_modern_card(center_frame, "Export Patient Record")
        export_shadow.pack(expand=True, pady=50)
        export_shadow.configure(width=600, height=500)
        
        export_frame = tk.Frame(export_content, bg=self.colors['card'])
        export_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Instructions
        instruction_label = tk.Label(export_frame, 
                                    text="Select a patient from the list below to export their complete record as a PDF.",
                                    font=self.fonts['body'], bg=self.colors['card'], fg=self.colors['text_light'],
                                    wraplength=500, justify='center')
        instruction_label.pack(pady=(0, 20))
        
        # Patient listbox
        scrollbar = tk.Scrollbar(export_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.export_listbox = tk.Listbox(export_frame, yscrollcommand=scrollbar.set,
                                       font=self.fonts['body'], relief='flat',
                                       selectbackground=self.colors['primary_light'],
                                       highlightthickness=1, 
                                       highlightcolor=self.colors['primary'])
        self.export_listbox.pack(fill='both', expand=True, pady=(0, 20))
        scrollbar.config(command=self.export_listbox.yview)
        
        # Export button
        ttk.Button(export_frame, text="📄 Export Selected Patient", style='Primary.TButton',
                  command=self.export_selected_patient).pack(pady=10)
        
        # Load patients
        try:
            patients = get_all_patients()
            for patient in patients:
                self.export_listbox.insert('end', patient)
        except Exception as e:
            print(f"Error loading patients for export: {e}")

    def export_selected_patient(self):
        selection = self.export_listbox.curselection()
        if selection:
            patient_name = self.export_listbox.get(selection[0])
            try:
                file_path = export_patient_to_pdf(patient_name)
                if file_path:
                    messagebox.showinfo("Export Successful", 
                                      f"Patient record for {patient_name} has been exported!\n\nSaved to:\n{file_path}")
                else:
                    messagebox.showerror("Export Failed", "Unable to export patient record")
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred during export:\n{str(e)}")
        else:
            messagebox.showwarning("No Selection", "Please select a patient to export")

def launch_dashboard():
    """Main function to launch the PearlTrack dashboard"""
    root = tk.Tk()
    app = ModernPearlTrack(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    launch_dashboard()




















      












