import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import uuid

# Import datetime properly to avoid conflicts
import datetime as dt
from datetime import datetime, timedelta

# Import matplotlib with better error handling
try:
    import matplotlib
    matplotlib.use('TkAgg')  # Set backend before importing pyplot
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
    print("Matplotlib loaded successfully")
except ImportError as e:
    print(f"Warning: matplotlib not available: {e}")
    MATPLOTLIB_AVAILABLE = False
except Exception as e:
    print(f"Warning: matplotlib error: {e}")
    MATPLOTLIB_AVAILABLE = False

from models import Member, Trainer, FitnessClass, Transaction, FitnessManagementSystem

class SmartFitnessApp:
    def __init__(self, root):
        self.root = root
        self.system = FitnessManagementSystem()
        self.root.title("Smart Fitness Management System - GUI Version")
        self.root.geometry("1400x800")
        self.root.configure(bg="#ecf0f1")
        
        # Set window icon and make it resizable
        self.root.minsize(1200, 700)
        try:
            self.root.state('zoomed')  # Maximize on Windows
        except:
            pass  # Handle case where zoomed is not available
        
        # Create sample data for testing
        self._create_sample_data()
        
        # Define color scheme
        self.colors = {
            'primary': '#2c3e50',      # Dark blue-gray
            'secondary': '#34495e',    # Medium blue-gray
            'accent': '#3498db',       # Blue
            'success': '#27ae60',      # Green
            'warning': '#f39c12',      # Orange
            'danger': '#e74c3c',       # Red
            'light': '#ecf0f1',        # Light gray
            'white': '#ffffff',        # White
            'text': '#2c3e50'          # Dark text
        }
        
        # Create main layout
        self._create_main_layout()
        
        # Show welcome screen initially
        self.show_welcome_screen()
        
    def _create_main_layout(self):
        # Create main container
        self.main_container = tk.Frame(self.root, bg=self.colors['light'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self._create_header()
        
        # Create main content area
        self.content_container = tk.Frame(self.main_container, bg=self.colors['light'])
        self.content_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self._create_sidebar()
        
        # Create content area
        self.content_frame = tk.Frame(self.content_container, bg=self.colors['white'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)
        
    def _create_header(self):
        """Create application header with title and status"""
        header_frame = tk.Frame(self.main_container, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="🏋️ Smart Fitness Management System", 
            font=("Segoe UI", 28, "bold"), 
            bg=self.colors['primary'], 
            fg=self.colors['white']
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Status info
        status_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        status_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
        members_count = len(self.system.view_members())
        tk.Label(
            status_frame, 
            text=f"Active Members: {members_count}", 
            font=("Segoe UI", 12), 
            bg=self.colors['primary'], 
            fg=self.colors['white']
        ).pack(anchor=tk.E)
        
        tk.Label(
            status_frame, 
            text=f"System Status: Online", 
            font=("Segoe UI", 10), 
            bg=self.colors['primary'], 
            fg=self.colors['success']
        ).pack(anchor=tk.E)
        
    def _create_sidebar(self):
        """Create enhanced sidebar with better styling"""
        self.sidebar = tk.Frame(self.content_container, width=280, bg=self.colors['secondary'])
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 20), pady=20)
        self.sidebar.pack_propagate(False)
        
        # Sidebar title
        sidebar_title = tk.Label(
            self.sidebar, 
            text="Navigation", 
            font=("Segoe UI", 16, "bold"), 
            bg=self.colors['secondary'], 
            fg=self.colors['white'],
            pady=20
        )
        sidebar_title.pack(fill=tk.X)
        
        # Navigation buttons with icons
        nav_buttons = [
            ("🏠 Dashboard", self.show_welcome_screen, self.colors['accent']),
            ("👥 User Management", self.show_user_management, self.colors['success']),
            ("💪 Workout Tracking", self.show_workout_tracking, self.colors['warning']),
            ("🎯 Goal Tracking", self.show_goal_tracking, self.colors['accent']),
            ("🥗 Nutrition Tracking", self.show_nutrition_tracking, self.colors['success']),
            ("📊 Reports & Analytics", self.show_reports, self.colors['danger']),
            ("❌ Exit Application", self.confirm_exit, self.colors['text'])
        ]
        
        for text, command, color in nav_buttons:
            self._create_nav_button(text, command, color)
            
    def _create_nav_button(self, text, command, color):
        """Create styled navigation button"""
        btn = tk.Button(
            self.sidebar,
            text=text,
            font=("Segoe UI", 12, "bold"),
            bg=color,
            fg=self.colors['white'],
            bd=0,
            pady=15,
            padx=20,
            cursor="hand2",
            relief=tk.FLAT,
            command=command
        )
        btn.pack(fill=tk.X, padx=15, pady=5)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self._darken_color(color))
        def on_leave(e):
            btn.configure(bg=color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
    def _darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            self.colors['accent']: '#2980b9',
            self.colors['success']: '#229954',
            self.colors['warning']: '#e67e22',
            self.colors['danger']: '#c0392b',
            self.colors['text']: '#1a1a1a'
        }
        return color_map.get(color, color)
        
    def confirm_exit(self):
        """Confirm before exiting application"""
        if messagebox.askyesno("Exit Application", "Are you sure you want to exit the Smart Fitness Management System?"):
            self.root.destroy()
            
    def show_welcome_screen(self):
        """Enhanced welcome dashboard"""
        self._clear_content_frame()
        
        # Welcome header
        welcome_frame = tk.Frame(self.content_frame, bg=self.colors['white'])
        welcome_frame.pack(fill=tk.X, padx=30, pady=30)
        
        tk.Label(
            welcome_frame,
            text="Welcome to Smart Fitness Management System",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack()
        
        tk.Label(
            welcome_frame,
            text="Manage your fitness center with advanced tracking and analytics",
            font=("Segoe UI", 14),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        # Dashboard cards
        cards_frame = tk.Frame(self.content_frame, bg=self.colors['white'])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Create dashboard cards
        self._create_dashboard_cards(cards_frame)
        
        # Quick actions
        actions_frame = tk.LabelFrame(
            self.content_frame,
            text="Quick Actions",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        actions_frame.pack(fill=tk.X, padx=30, pady=20)
        
        quick_actions = [
            ("➕ Add New Member", self.add_new_member, self.colors['success']),
            ("📝 Log Workout", lambda: self.show_workout_tracking(), self.colors['warning']),
            ("📊 View Reports", lambda: self.show_reports(), self.colors['danger'])
        ]
        
        for i, (text, command, color) in enumerate(quick_actions):
            btn = tk.Button(
                actions_frame,
                text=text,
                font=("Segoe UI", 12, "bold"),
                bg=color,
                fg=self.colors['white'],
                bd=0,
                pady=10,
                padx=20,
                cursor="hand2",
                command=command
            )
            btn.grid(row=0, column=i, padx=10, pady=15, sticky="ew")
            actions_frame.grid_columnconfigure(i, weight=1)
            
    def _create_dashboard_cards(self, parent):
        """Create dashboard statistics cards"""
        members_count = len(self.system.view_members())
        total_revenue = sum(t.amount_paid for t in self.system.transactions)
        active_classes = len(self.system.fitness_classes)
        
        # Calculate total workouts from all members
        total_workouts = 0
        for member in self.system.view_members():
            if hasattr(member, 'workouts') and member.workouts:
                total_workouts += len(member.workouts)
        
        cards_data = [
            ("👥", "Total Members", members_count, self.colors['accent']),
            ("💰", "Total Revenue", f"${total_revenue:.2f}", self.colors['success']),
            ("🏃", "Active Classes", active_classes, self.colors['warning']),
            ("💪", "Total Workouts", total_workouts, self.colors['danger'])
        ]
        
        for i, (icon, title, value, color) in enumerate(cards_data):
            card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=2)
            card.grid(row=0, column=i, padx=15, pady=15, sticky="nsew", ipadx=20, ipady=20)
            
            tk.Label(
                card,
                text=icon,
                font=("Segoe UI", 36),
                bg=color,
                fg=self.colors['white']
            ).pack()
            
            tk.Label(
                card,
                text=str(value),
                font=("Segoe UI", 20, "bold"),
                bg=color,
                fg=self.colors['white']
            ).pack()
            
            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 12),
                bg=color,
                fg=self.colors['white']
            ).pack()
            
        # Configure grid weights
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1)
            
    def _create_sample_data(self):
        """Create enhanced sample data with workouts and goals"""
        # Create sample members
        member1 = Member("M001", "John Doe", 30, "Premium", "Weight Loss")
        member2 = Member("M002", "Jane Smith", 25, "Basic", "Muscle Gain")
        member3 = Member("M003", "Mike Johnson", 35, "VIP", "Endurance")
        
        self.system.register_member(member1)
        self.system.register_member(member2)
        self.system.register_member(member3)
        
        # Add workout data with proper datetime objects
        current_time = datetime.now()
        member1.workouts = [
            {
                "id": str(uuid.uuid4()),
                "date": current_time - timedelta(days=1),
                "exercise_type": "Running",
                "duration": 30,
                "calories": 350,
                "notes": "Morning run"
            },
            {
                "id": str(uuid.uuid4()),
                "date": current_time - timedelta(days=3),
                "exercise_type": "Weight Lifting",
                "duration": 45,
                "calories": 200,
                "notes": "Upper body workout"
            }
        ]
        
        member2.workouts = [
            {
                "id": str(uuid.uuid4()),
                "date": current_time - timedelta(days=2),
                "exercise_type": "Yoga",
                "duration": 60,
                "calories": 180,
                "notes": "Relaxing session"
            }
        ]
        
        # Add goals with proper datetime objects
        member1.goals = [
            {
                "id": str(uuid.uuid4()),
                "goal_type": "Calories to Burn",
                "target": "2000",
                "start_value": "0",
                "duration": 4,
                "duration_unit": "Weeks",
                "created": current_time - timedelta(days=5),
                "end_date": current_time + timedelta(weeks=4),
                "progress": 27.5
            }
        ]
        
        # Add meals with proper datetime objects
        member1.meals = [
            {
                "id": str(uuid.uuid4()),
                "date": current_time,
                "meal_type": "Breakfast",
                "food_items": "Oatmeal with fruits",
                "calories": 350,
                "protein": 12,
                "carbs": 65,
                "fat": 8
            }
        ]
        
        # Create trainers
        trainer1 = Trainer("T001", "Mike Johnson", "Yoga")
        trainer2 = Trainer("T002", "Sara Brown", "Strength Training")
        trainer3 = Trainer("T003", "Alex Wilson", "Cardio")
        
        self.system.add_trainer(trainer1)
        self.system.add_trainer(trainer2)
        self.system.add_trainer(trainer3)
        
        # Create fitness classes
        class1 = FitnessClass("C001", "Morning Yoga", 15, "Monday, 8:00 AM")
        class2 = FitnessClass("C002", "HIIT Training", 10, "Tuesday, 6:00 PM")
        class3 = FitnessClass("C003", "Strength Building", 12, "Wednesday, 7:00 PM")
        
        class1.assign_trainer(trainer1)
        class2.assign_trainer(trainer2)
        class3.assign_trainer(trainer3)
        
        self.system.schedule_class(class1)
        self.system.schedule_class(class2)
        self.system.schedule_class(class3)
        
        # Create transactions
        trans1 = Transaction("T001", member1, 50.00, "Premium Membership")
        trans2 = Transaction("T002", member2, 30.00, "Basic Membership")
        trans3 = Transaction("T003", member3, 75.00, "VIP Membership")
        
        self.system.add_transaction(trans1)
        self.system.add_transaction(trans2)
        self.system.add_transaction(trans3)
    
    def _clear_content_frame(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _create_styled_button(self, parent, text, command, color=None, **kwargs):
        """Create a styled button with consistent appearance"""
        if color is None:
            color = self.colors['accent']
            
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg=self.colors['white'],
            bd=0,
            pady=8,
            padx=15,
            cursor="hand2",
            relief=tk.FLAT,
            **kwargs
        )
        
        # Add hover effect
        def on_enter(e):
            btn.configure(bg=self._darken_color(color))
        def on_leave(e):
            btn.configure(bg=color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def show_user_management(self):
        """Enhanced user management interface"""
        self._clear_content_frame()
        
        # Page header
        header_frame = tk.Frame(self.content_frame, bg=self.colors['white'])
        header_frame.pack(fill=tk.X, padx=30, pady=20)
        
        tk.Label(
            header_frame,
            text="👥 User Management",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(side=tk.LEFT)
        
        # Action buttons
        actions_frame = tk.Frame(header_frame, bg=self.colors['white'])
        actions_frame.pack(side=tk.RIGHT)
        
        self._create_styled_button(
            actions_frame, "➕ Add Member", self.add_new_member, self.colors['success']
        ).pack(side=tk.LEFT, padx=5)
        
        self._create_styled_button(
            actions_frame, "✏️ Update", self.update_member, self.colors['warning']
        ).pack(side=tk.LEFT, padx=5)
        
        self._create_styled_button(
            actions_frame, "🗑️ Delete", self.delete_member, self.colors['danger']
        ).pack(side=tk.LEFT, padx=5)
        
        # Members table with enhanced styling
        table_container = tk.Frame(self.content_frame, bg=self.colors['white'])
        table_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Create treeview with custom style
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Segoe UI", 11))
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 12, "bold"))
        
        columns = ('ID', 'Name', 'Age', 'Membership Type', 'Fitness Goals')
        self.members_table = ttk.Treeview(
            table_container, 
            columns=columns, 
            show='headings',
            style="Custom.Treeview"
        )
        
        # Define headings
        for col in columns:
            self.members_table.heading(col, text=col)
            self.members_table.column(col, width=150, anchor=tk.CENTER)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.members_table.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.members_table.xview)
        
        self.members_table.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.members_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load members
        self.load_members_table()
        
        # Add member statistics
        stats_frame = tk.LabelFrame(
            self.content_frame,
            text="Member Statistics",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        stats_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        members = self.system.view_members()
        membership_counts = {"Basic": 0, "Premium": 0, "VIP": 0}
        goal_counts = {}
        
        for member in members:
            if member.membership_type in membership_counts:
                membership_counts[member.membership_type] += 1
            goal_counts[member.fitness_goals] = goal_counts.get(member.fitness_goals, 0) + 1
        
        # Display statistics
        stats_text = f"Total Members: {len(members)} | "
        stats_text += f"Basic: {membership_counts['Basic']} | "
        stats_text += f"Premium: {membership_counts['Premium']} | "
        stats_text += f"VIP: {membership_counts['VIP']}"
        
        tk.Label(
            stats_frame,
            text=stats_text,
            font=("Segoe UI", 11),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(pady=10)

    def load_members_table(self):
        """Load members into table with enhanced data"""
        # Clear existing items
        for item in self.members_table.get_children():
            self.members_table.delete(item)
            
        # Add members to table
        for member in self.system.view_members():
            self.members_table.insert('', tk.END, values=(
                member.member_id,
                member.name,
                member.age,
                member.membership_type,
                member.fitness_goals
            ))

    def add_new_member(self):
        """Enhanced add member dialog"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Member")
        add_window.geometry("450x400")
        add_window.configure(bg=self.colors['light'])
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Center the window
        add_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Header
        header_frame = tk.Frame(add_window, bg=self.colors['success'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="➕ Add New Member",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['success'],
            fg=self.colors['white']
        ).pack(expand=True)
        
        # Form
        form_frame = tk.Frame(add_window, bg=self.colors['white'], padx=30, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Member ID
        tk.Label(form_frame, text="Member ID:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=10)
        member_id_var = tk.StringVar(value=f"M{str(uuid.uuid4().int)[:3]}")
        member_id_entry = tk.Entry(form_frame, textvariable=member_id_var, state='readonly',
                                  font=("Segoe UI", 11), width=25)
        member_id_entry.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        # Name
        tk.Label(form_frame, text="Full Name:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=1, column=0, sticky=tk.W, pady=10)
        name_var = tk.StringVar()
        name_entry = tk.Entry(form_frame, textvariable=name_var, font=("Segoe UI", 11), width=25)
        name_entry.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        # Age
        tk.Label(form_frame, text="Age:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=2, column=0, sticky=tk.W, pady=10)
        age_var = tk.IntVar()
        age_entry = tk.Entry(form_frame, textvariable=age_var, font=("Segoe UI", 11), width=25)
        age_entry.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        # Membership Type
        tk.Label(form_frame, text="Membership Type:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=3, column=0, sticky=tk.W, pady=10)
        membership_var = tk.StringVar()
        membership_combo = ttk.Combobox(form_frame, textvariable=membership_var, 
                                       values=["Basic", "Premium", "VIP"], font=("Segoe UI", 11), width=23)
        membership_combo.grid(row=3, column=1, sticky=tk.W, pady=10)
        
        # Fitness Goals
        tk.Label(form_frame, text="Fitness Goals:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=4, column=0, sticky=tk.W, pady=10)
        goals_var = tk.StringVar()
        goals_combo = ttk.Combobox(form_frame, textvariable=goals_var, 
                                 values=["Weight Loss", "Muscle Gain", "Endurance", "General Fitness"], 
                                 font=("Segoe UI", 11), width=23)
        goals_combo.grid(row=4, column=1, sticky=tk.W, pady=10)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['white'])
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def save_member():
            try:
                if not all([name_var.get(), age_var.get(), membership_var.get(), goals_var.get()]):
                    messagebox.showwarning("Missing Information", "Please fill in all fields.")
                    return
                    
                new_member = Member(
                    member_id_var.get(),
                    name_var.get(),
                    int(age_var.get()),
                    membership_var.get(),
                    goals_var.get()
                )
                self.system.register_member(new_member)
                self.load_members_table()
                messagebox.showinfo("Success", f"Member {name_var.get()} added successfully!")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid age.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add member: {str(e)}")
        
        self._create_styled_button(
            button_frame, "💾 Save Member", save_member, self.colors['success']
        ).pack(side=tk.LEFT, padx=5)
        
        self._create_styled_button(
            button_frame, "❌ Cancel", add_window.destroy, self.colors['danger']
        ).pack(side=tk.LEFT, padx=5)
        
        # Focus on name entry
        name_entry.focus()

    def update_member(self):
        """Enhanced update member dialog"""
        selected = self.members_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a member to update.")
            return
            
        member_id = self.members_table.item(selected[0])['values'][0]
        member = self.system.find_member_by_id(member_id)
        if not member:
            messagebox.showerror("Error", "Member not found.")
            return
        
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Member")
        update_window.geometry("450x400")
        update_window.configure(bg=self.colors['light'])
        update_window.transient(self.root)
        update_window.grab_set()
        
        # Center the window
        update_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Header
        header_frame = tk.Frame(update_window, bg=self.colors['warning'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="✏️ Update Member",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['warning'],
            fg=self.colors['white']
        ).pack(expand=True)
        
        # Form
        form_frame = tk.Frame(update_window, bg=self.colors['white'], padx=30, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Name
        tk.Label(form_frame, text="Full Name:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=10)
        name_var = tk.StringVar(value=member.name)
        name_entry = tk.Entry(form_frame, textvariable=name_var, font=("Segoe UI", 11), width=25)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        # Age
        tk.Label(form_frame, text="Age:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=1, column=0, sticky=tk.W, pady=10)
        age_var = tk.IntVar(value=member.age)
        age_entry = tk.Entry(form_frame, textvariable=age_var, font=("Segoe UI", 11), width=25)
        age_entry.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        # Membership Type
        tk.Label(form_frame, text="Membership Type:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=2, column=0, sticky=tk.W, pady=10)
        membership_var = tk.StringVar(value=member.membership_type)
        membership_combo = ttk.Combobox(form_frame, textvariable=membership_var, 
                                       values=["Basic", "Premium", "VIP"], font=("Segoe UI", 11), width=23)
        membership_combo.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        # Fitness Goals
        tk.Label(form_frame, text="Fitness Goals:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=3, column=0, sticky=tk.W, pady=10)
        goals_var = tk.StringVar(value=member.fitness_goals)
        goals_combo = ttk.Combobox(form_frame, textvariable=goals_var, 
                                 values=["Weight Loss", "Muscle Gain", "Endurance", "General Fitness"], 
                                 font=("Segoe UI", 11), width=23)
        goals_combo.grid(row=3, column=1, sticky=tk.W, pady=10)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['white'])
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def save_updates():
            try:
                member.name = name_var.get()
                member.age = int(age_var.get())
                member.update_membership(membership_var.get())
                member.fitness_goals = goals_var.get()
                self.load_members_table()
                messagebox.showinfo("Success", "Member updated successfully!")
                update_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update member: {str(e)}")
        
        self._create_styled_button(
            button_frame, "💾 Save Changes", save_updates, self.colors['success']
        ).pack(side=tk.LEFT, padx=5)
        
        self._create_styled_button(
            button_frame, "❌ Cancel", update_window.destroy, self.colors['danger']
        ).pack(side=tk.LEFT, padx=5)
        
    def delete_member(self):
        """Enhanced delete member confirmation"""
        selected = self.members_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a member to delete.")
            return
            
        member_id = self.members_table.item(selected[0])['values'][0]
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete member with ID: {member_id}?")
        if confirm:
            if self.system.cancel_membership(member_id):
                messagebox.showinfo("Success", "Member deleted successfully!")
                self.load_members_table()
            else:
                messagebox.showerror("Error", "Failed to delete member.")
    
    def show_workout_tracking(self):
        """Enhanced workout tracking interface"""
        self._clear_content_frame()
        
        # Page header
        header_frame = tk.Frame(self.content_frame, bg=self.colors['white'])
        header_frame.pack(fill=tk.X, padx=30, pady=20)
        
        tk.Label(
            header_frame,
            text="💪 Workout Tracking",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(side=tk.LEFT)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Tab 1: Log Workout
        log_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(log_frame, text="📝 Log Workout")
        
        # Tab 2: Workout History
        history_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(history_frame, text="📊 Workout History")
        
        # Tab 3: Exercise Library
        library_frame = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(library_frame, text="📚 Exercise Library")
        
        self._create_workout_log_tab(log_frame)
        self._create_workout_history_tab(history_frame)
        self._create_exercise_library_tab(library_frame)

    def _create_workout_log_tab(self, parent):
        """Create workout logging form"""
        # Form container
        form_container = tk.Frame(parent, bg=self.colors['white'])
        form_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Left side - Form
        form_frame = tk.LabelFrame(
            form_container,
            text="Log New Workout",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Member selection
        tk.Label(form_frame, text="Select Member:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, padx=15, pady=10)
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(form_frame, textvariable=member_var, width=35, font=("Segoe UI", 11))
        member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.grid(row=0, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Exercise type
        tk.Label(form_frame, text="Exercise Type:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=1, column=0, sticky=tk.W, padx=15, pady=10)
        exercise_var = tk.StringVar()
        exercise_combo = ttk.Combobox(form_frame, textvariable=exercise_var, width=35, font=("Segoe UI", 11),
                                    values=["Running", "Weight Lifting", "Yoga", "Swimming", "Cycling", 
                                           "HIIT", "Pilates", "CrossFit", "Boxing", "Dance"])
        exercise_combo.grid(row=1, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Duration
        tk.Label(form_frame, text="Duration (minutes):", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=2, column=0, sticky=tk.W, padx=15, pady=10)
        duration_var = tk.IntVar()
        duration_entry = tk.Entry(form_frame, textvariable=duration_var, width=37, font=("Segoe UI", 11))
        duration_entry.grid(row=2, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Calories
        tk.Label(form_frame, text="Calories Burned:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=3, column=0, sticky=tk.W, padx=15, pady=10)
        calories_var = tk.IntVar()
        calories_entry = tk.Entry(form_frame, textvariable=calories_var, width=37, font=("Segoe UI", 11))
        calories_entry.grid(row=3, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Intensity Level
        tk.Label(form_frame, text="Intensity Level:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=4, column=0, sticky=tk.W, padx=15, pady=10)
        intensity_var = tk.StringVar()
        intensity_combo = ttk.Combobox(form_frame, textvariable=intensity_var, width=35, font=("Segoe UI", 11),
                                     values=["Low", "Moderate", "High", "Very High"])
        intensity_combo.grid(row=4, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Notes
        tk.Label(form_frame, text="Notes:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).grid(row=5, column=0, sticky=tk.NW, padx=15, pady=10)
        notes_var = tk.StringVar()
        notes_text = tk.Text(form_frame, width=35, height=4, font=("Segoe UI", 11))
        notes_text.grid(row=5, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Save button
        def log_workout():
            if not member_var.get() or not exercise_var.get():
                messagebox.showwarning("Missing Information", "Please select a member and exercise type.")
                return
                
            try:
                member_id = member_var.get().split(" - ")[0]
                member = self.system.find_member_by_id(member_id)
                
                if member:
                    workout_data = {
                        "id": str(uuid.uuid4()),
                        "date": datetime.now(),
                        "exercise_type": exercise_var.get(),
                        "duration": duration_var.get(),
                        "calories": calories_var.get(),
                        "intensity": intensity_var.get(),
                        "notes": notes_text.get("1.0", tk.END).strip()
                    }
                    
                    if not hasattr(member, "workouts"):
                        member.workouts = []
                    member.workouts.append(workout_data)
                    member.track_progress({"type": "workout", **workout_data})
                    
                    messagebox.showinfo("Success", "Workout logged successfully!")
                    
                    # Clear form fields
                    exercise_var.set("")
                    duration_var.set(0)
                    calories_var.set(0)
                    intensity_var.set("")
                    notes_text.delete("1.0", tk.END)
                    
                    self.load_workout_history()
                else:
                    messagebox.showerror("Error", "Member not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to log workout: {str(e)}")
        
        button_frame = tk.Frame(form_frame, bg=self.colors['white'])
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        self._create_styled_button(
            button_frame, "💾 Log Workout", log_workout, self.colors['success']
        ).pack()
        
        # Right side - Today's Summary
        summary_frame = tk.LabelFrame(
            form_container,
            text="Today's Activity Summary",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        summary_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Calculate today's stats
        today = datetime.now().strftime("%Y-%m-%d")
        today_workouts = 0
        today_calories = 0
        
        for member in self.system.view_members():
            if hasattr(member, "workouts") and member.workouts:
                for workout in member.workouts:
                    if workout["date"].strftime("%Y-%m-%d") == today:
                        today_workouts += 1
                        today_calories += workout.get("calories", 0)
        
        tk.Label(
            summary_frame,
            text=f"Workouts Today: {today_workouts}",
            font=("Segoe UI", 12),
            bg=self.colors['white']
        ).pack(pady=10)
        
        tk.Label(
            summary_frame,
            text=f"Total Calories: {today_calories}",
            font=("Segoe UI", 12),
            bg=self.colors['white']
        ).pack(pady=10)

    def _create_workout_history_tab(self, parent):
        """Create workout history view with filtering"""
        # Controls frame
        controls_frame = tk.Frame(parent, bg=self.colors['white'])
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Member filter
        tk.Label(controls_frame, text="Member:", font=("Segoe UI", 11, "bold"), 
                bg="white").pack(side=tk.LEFT, padx=5)
        history_member_var = tk.StringVar()
        member_filter = ttk.Combobox(controls_frame, textvariable=history_member_var, width=25)
        member_filter['values'] = ["All Members"] + [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_filter.set("All Members")
        member_filter.pack(side=tk.LEFT, padx=5)
        
        # Exercise filter
        tk.Label(controls_frame, text="Exercise:", font=("Segoe UI", 11, "bold"), 
                bg="white").pack(side=tk.LEFT, padx=5)
        exercise_filter_var = tk.StringVar()
        exercise_filter = ttk.Combobox(controls_frame, textvariable=exercise_filter_var, width=15)
        exercise_filter['values'] = ["All"] + ["Running", "Weight Lifting", "Yoga", "Swimming", "Cycling"]
        exercise_filter.set("All")
        exercise_filter.pack(side=tk.LEFT, padx=5)
        
        # Date filter
        tk.Label(controls_frame, text="Date:", font=("Segoe UI", 11, "bold"), 
                bg="white").pack(side=tk.LEFT, padx=5)
        date_filter_var = tk.StringVar()
        date_filter = tk.Entry(controls_frame, textvariable=date_filter_var, width=12)
        date_filter.pack(side=tk.LEFT, padx=5)
        
        # History table
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Date", "Member", "Exercise", "Duration", "Calories", "Intensity", "Notes")
        self.workout_history_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.workout_history_table.heading(col, text=col)
            self.workout_history_table.column(col, width=120)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.workout_history_table.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.workout_history_table.xview)
        
        self.workout_history_table.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        
        self.workout_history_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load workout history
        def load_workout_history():
            # Clear existing items
            for item in self.workout_history_table.get_children():
                self.workout_history_table.delete(item)
            
            for member in self.system.view_members():
                if hasattr(member, "workouts") and member.workouts:
                    for workout in member.workouts:
                        # Apply filters
                        if history_member_var.get() != "All Members" and history_member_var.get():
                            selected_member_id = history_member_var.get().split(" - ")[0]
                            if member.member_id != selected_member_id:
                                continue
                        
                        if exercise_filter_var.get() != "All" and exercise_filter_var.get():
                            if workout.get("exercise_type") != exercise_filter_var.get():
                                continue
                        
                        if date_filter_var.get():
                            try:
                                if workout["date"].strftime("%Y-%m-%d") != date_filter_var.get():
                                    continue
                            except:
                                continue
                        
                        self.workout_history_table.insert("", tk.END, values=(
                            workout["date"].strftime("%Y-%m-%d %H:%M"),
                            member.name,
                            workout.get("exercise_type", ""),
                            workout.get("duration", ""),
                            workout.get("calories", ""),
                            workout.get("intensity", ""),
                            workout.get("notes", "")[:50] + "..." if len(workout.get("notes", "")) > 50 else workout.get("notes", "")
                        ))
        
        # Bind filter events
        member_filter.bind("<<ComboboxSelected>>", lambda e: load_workout_history())
        exercise_filter.bind("<<ComboboxSelected>>", lambda e: load_workout_history())
        date_filter.bind("<KeyRelease>", lambda e: load_workout_history())
        
        # Refresh button
        self._create_styled_button(
            controls_frame, "🔄 Refresh", load_workout_history, self.colors['accent']
        ).pack(side=tk.RIGHT, padx=5)
        
        # Store the function reference for external calls
        self.load_workout_history = load_workout_history
        
        # Initial load
        load_workout_history()

    def _create_exercise_library_tab(self, parent):
        """Create exercise library with tips"""
        library_frame = tk.Frame(parent, bg=self.colors['white'])
        library_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            library_frame,
            text="Exercise Library & Tips",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=10)
        
        # Exercise categories
        exercises = {
            "Cardio Exercises": [
                ("Running", "Great for cardiovascular health and weight loss", "300-600 cal/hour"),
                ("Cycling", "Low impact cardio, good for joint health", "250-500 cal/hour"),
                ("Swimming", "Full body workout, excellent for all fitness levels", "400-700 cal/hour"),
                ("HIIT", "High intensity interval training for maximum results", "350-600 cal/hour")
            ],
            "Strength Training": [
                ("Weight Lifting", "Build muscle mass and increase metabolism", "200-400 cal/hour"),
                ("Push-ups", "Upper body strength using body weight", "150-300 cal/hour"),
                ("Squats", "Lower body strength and core stability", "200-350 cal/hour"),
                ("Deadlifts", "Full body compound movement", "250-400 cal/hour")
            ],
            "Flexibility & Recovery": [
                ("Yoga", "Improve flexibility, balance, and mental health", "150-300 cal/hour"),
                ("Pilates", "Core strength and body alignment", "200-350 cal/hour"),
                ("Stretching", "Maintain flexibility and prevent injury", "100-200 cal/hour"),
                ("Tai Chi", "Gentle movement for balance and relaxation", "150-250 cal/hour")
            ]
        }
        
        # Create scrollable frame
        canvas = tk.Canvas(library_frame, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(library_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add exercise information
        for category, exercise_list in exercises.items():
            category_frame = tk.LabelFrame(
                scrollable_frame,
                text=category,
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['white'],
                fg=self.colors['primary']
            )
            category_frame.pack(fill=tk.X, padx=10, pady=10)
            
            for exercise, description, calories in exercise_list:
                exercise_frame = tk.Frame(category_frame, bg=self.colors['light'], relief=tk.RAISED, bd=1)
                exercise_frame.pack(fill=tk.X, padx=5, pady=5)
                
                tk.Label(
                    exercise_frame,
                    text=exercise,
                    font=("Segoe UI", 11, "bold"),
                    bg=self.colors['light']
                ).pack(anchor=tk.W, padx=10, pady=2)
                
                tk.Label(
                    exercise_frame,
                    text=description,
                    font=("Segoe UI", 10),
                    bg=self.colors['light'],
                    wraplength=400,
                    justify=tk.LEFT
                ).pack(anchor=tk.W, padx=10)
                
                tk.Label(
                    exercise_frame,
                    text=f"Calories burned: {calories}",
                    font=("Segoe UI", 9),
                    bg=self.colors['light'],
                    fg=self.colors['success']
                ).pack(anchor=tk.W, padx=10, pady=2)
        
        # Update scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)

    def show_goal_tracking(self):
        self._clear_content_frame()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        page_title = tk.Label(title_frame, text="Goal Tracking & Progress", font=("Arial", 20, "bold"), bg="#f0f0f0")
        page_title.pack(side=tk.LEFT)
        
        # Create a notebook (tabbed interface) for different goal tracking views
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tab 1: Set Goals
        set_goals_frame = tk.Frame(notebook, bg="white")
        notebook.add(set_goals_frame, text="Set Goals")
        
        # Tab 2: Monitor Progress
        monitor_progress_frame = tk.Frame(notebook, bg="white")
        notebook.add(monitor_progress_frame, text="Monitor Progress")
        
        # Simple goal setting form
        goal_form_frame = tk.LabelFrame(set_goals_frame, text="Set New Goal", bg="white", padx=15, pady=15)
        goal_form_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Member selection
        tk.Label(goal_form_frame, text="Select Member:", bg="white").pack(anchor=tk.W, pady=5)
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(goal_form_frame, textvariable=member_var, width=30)
        member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.pack(anchor=tk.W, pady=5)
        
        # Goal type
        tk.Label(goal_form_frame, text="Goal Type:", bg="white").pack(anchor=tk.W, pady=5)
        goal_type_var = tk.StringVar()
        goal_types = ["Weight Loss", "Muscle Gain", "Endurance", "Strength"]
        goal_type_combo = ttk.Combobox(goal_form_frame, textvariable=goal_type_var, width=30, values=goal_types)
        goal_type_combo.pack(anchor=tk.W, pady=5)
        
        # Target value
        tk.Label(goal_form_frame, text="Target Value:", bg="white").pack(anchor=tk.W, pady=5)
        target_var = tk.StringVar()
        target_entry = tk.Entry(goal_form_frame, textvariable=target_var, width=32)
        target_entry.pack(anchor=tk.W, pady=5)
        
        def save_goal():
            if member_var.get() and goal_type_var.get() and target_var.get():
                member_id = member_var.get().split(" - ")[0]
                member = self.system.find_member_by_id(member_id)
                if member:
                    if not hasattr(member, "goals"):
                        member.goals = []
                    goal = {
                        "id": str(uuid.uuid4()),
                        "goal_type": goal_type_var.get(),
                        "target": target_var.get(),
                        "created": datetime.now(),
                        "progress": 0
                    }
                    member.goals.append(goal)
                    messagebox.showinfo("Success", "Goal saved successfully!")
                    goal_type_var.set("")
                    target_var.set("")
            else:
                messagebox.showwarning("Missing Information", "Please fill in all fields.")
        
        tk.Button(goal_form_frame, text="Save Goal", bg="#3498db", fg="white",
                 font=("Arial", 12), command=save_goal).pack(pady=10)

    def show_nutrition_tracking(self):
        self._clear_content_frame()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        page_title = tk.Label(title_frame, text="Nutrition & Diet Tracking", font=("Arial", 20, "bold"), bg="#f0f0f0")
        page_title.pack(side=tk.LEFT)
        
        # Create custom button navigation instead of notebook
        nav_frame = tk.Frame(self.content_frame, bg="white", height=80)
        nav_frame.pack(fill=tk.X, padx=20, pady=10)
        nav_frame.pack_propagate(False)
        
        # Content frame for different sections
        content_frame = tk.Frame(self.content_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Variable to track current view
        current_view = tk.StringVar(value="log_meals")
        
        # Create styled navigation buttons
        button_style = {
            'font': ("Segoe UI", 12, "bold"),
            'bd': 0,
            'pady': 15,
            'padx': 25,
            'cursor': "hand2",
            'relief': tk.FLAT,
            'width': 18,
            'height': 2
        }
        
        def switch_view(view_name):
            current_view.set(view_name)
            # Clear content frame
            for widget in content_frame.winfo_children():
                widget.destroy()
            
            # Update button styles
            for btn, view in button_views:
                if view == view_name:
                    btn.configure(bg=self.colors['success'], fg="white")
                else:
                    btn.configure(bg=self.colors['light'], fg=self.colors['text'])
            
            # Show appropriate content
            if view_name == "log_meals":
                self._create_meal_log_tab(content_frame)
            elif view_name == "meal_history":
                self._create_meal_history_tab(content_frame)
            elif view_name == "nutrition_analysis":
                self._create_nutrition_analysis_tab(content_frame)
        
        # Create navigation buttons with modern styling
        log_meals_btn = tk.Button(
            nav_frame,
            text="🍽️ Log Meals",
            command=lambda: switch_view("log_meals"),
            bg=self.colors['success'],
            fg="white",
            **button_style
        )
        log_meals_btn.pack(side=tk.LEFT, padx=10, pady=15)
        
        meal_history_btn = tk.Button(
            nav_frame,
            text="📊 Meal History",
            command=lambda: switch_view("meal_history"),
            bg=self.colors['light'],
            fg=self.colors['text'],
            **button_style
        )
        meal_history_btn.pack(side=tk.LEFT, padx=10, pady=15)
        
        nutrition_analysis_btn = tk.Button(
            nav_frame,
            text="📈 Nutrition Analysis",
            command=lambda: switch_view("nutrition_analysis"),
            bg=self.colors['light'],
            fg=self.colors['text'],
            **button_style
        )
        nutrition_analysis_btn.pack(side=tk.LEFT, padx=10, pady=15)
        
        # Store button references for style updates
        button_views = [
            (log_meals_btn, "log_meals"),
            (meal_history_btn, "meal_history"),
            (nutrition_analysis_btn, "nutrition_analysis")
        ]
        
        # Add hover effects to buttons
        def create_hover_effect(button, active_view):
            def on_enter(e):
                if current_view.get() != active_view:
                    button.configure(bg=self._darken_color(self.colors['light']))
            
            def on_leave(e):
                if current_view.get() != active_view:
                    button.configure(bg=self.colors['light'])
                elif current_view.get() == active_view:
                    button.configure(bg=self.colors['success'])
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        # Apply hover effects
        create_hover_effect(meal_history_btn, "meal_history")
        create_hover_effect(nutrition_analysis_btn, "nutrition_analysis")
        
        # Add visual separator
        separator = tk.Frame(nav_frame, bg=self.colors['accent'], height=3)
        separator.pack(fill=tk.X, padx=20, pady=(0, 10), side=tk.BOTTOM)
        
        # Initialize with log meals view
        self._create_meal_log_tab(content_frame)

    def _create_meal_log_tab(self, parent):
        """Create enhanced meal logging form"""
        # Form container
        form_container = tk.Frame(parent, bg=self.colors['white'])
        form_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Left side - Meal logging form
        form_frame = tk.LabelFrame(
            form_container,
            text="Log New Meal",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Member selection
        tk.Label(form_frame, text="Select Member:", font=("Segoe UI", 11, "bold"), 
                bg="white").grid(row=0, column=0, sticky=tk.W, padx=15, pady=10)
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(form_frame, textvariable=member_var, width=35, font=("Segoe UI", 11))
        member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.grid(row=0, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Meal type
        tk.Label(form_frame, text="Meal Type:", font=("Segoe UI", 11, "bold"), 
                bg="white").grid(row=1, column=0, sticky=tk.W, padx=15, pady=10)
        meal_type_var = tk.StringVar()
        meal_types = ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-Workout", "Post-Workout"]
        meal_type_combo = ttk.Combobox(form_frame, textvariable=meal_type_var, width=35, 
                                     font=("Segoe UI", 11), values=meal_types)
        meal_type_combo.grid(row=1, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Food items
        tk.Label(form_frame, text="Food Items:", font=("Segoe UI", 11, "bold"), 
                bg="white").grid(row=2, column=0, sticky=tk.W, padx=15, pady=10)
        food_var = tk.StringVar()
        food_entry = tk.Entry(form_frame, textvariable=food_var, width=37, font=("Segoe UI", 11))
        food_entry.grid(row=2, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Calories
        tk.Label(form_frame, text="Total Calories:", font=("Segoe UI", 11, "bold"), 
                bg="white").grid(row=3, column=0, sticky=tk.W, padx=15, pady=10)
        calories_var = tk.IntVar()
        calories_entry = tk.Entry(form_frame, textvariable=calories_var, width=37, font=("Segoe UI", 11))
        calories_entry.grid(row=3, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Protein
        tk.Label(form_frame, text="Protein (g):", font=("Segoe UI", 11, "bold"), 
                bg="white").grid(row=4, column=0, sticky=tk.W, padx=15, pady=10)
        protein_var = tk.IntVar()
        protein_entry = tk.Entry(form_frame, textvariable=protein_var, width=37, font=("Segoe UI", 11))
        protein_entry.grid(row=4, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Carbohydrates
        tk.Label(form_frame, text="Carbohydrates (g):", font=("Segoe UI", 11, "bold"), 
                bg="white").grid(row=5, column=0, sticky=tk.W, padx=15, pady=10)
        carbs_var = tk.IntVar()
        carbs_entry = tk.Entry(form_frame, textvariable=carbs_var, width=37, font=("Segoe UI", 11))
        carbs_entry.grid(row=5, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Fat
        tk.Label(form_frame, text="Fat (g):", font=("Segoe UI", 11, "bold"), 
                bg="white").grid(row=6, column=0, sticky=tk.W, padx=15, pady=10)
        fat_var = tk.IntVar()
        fat_entry = tk.Entry(form_frame, textvariable=fat_var, width=37, font=("Segoe UI", 11))
        fat_entry.grid(row=6, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Notes
        tk.Label(form_frame, text="Notes:", font=("Segoe UI", 11, "bold"), 
                bg="white").grid(row=7, column=0, sticky=tk.NW, padx=15, pady=10)
        notes_text = tk.Text(form_frame, width=35, height=3, font=("Segoe UI", 11))
        notes_text.grid(row=7, column=1, sticky=tk.W, padx=15, pady=10)
        
        # Save button
        def save_meal():
            if not all([member_var.get(), meal_type_var.get(), food_var.get()]):
                messagebox.showwarning("Missing Information", "Please fill in member, meal type, and food items.")
                return
                
            try:
                member_id = member_var.get().split(" - ")[0]
                member = self.system.find_member_by_id(member_id)
                
                if member:
                    if not hasattr(member, "meals"):
                        member.meals = []
                        
                    meal_data = {
                        "id": str(uuid.uuid4()),
                        "date": datetime.now(),
                        "meal_type": meal_type_var.get(),
                        "food_items": food_var.get(),
                        "calories": calories_var.get() if calories_var.get() else 0,
                        "protein": protein_var.get() if protein_var.get() else 0,
                        "carbs": carbs_var.get() if carbs_var.get() else 0,
                        "fat": fat_var.get() if fat_var.get() else 0,
                        "notes": notes_text.get("1.0", tk.END).strip()
                    }
                    
                    member.meals.append(meal_data)
                    member.track_progress({"type": "meal", **meal_data})
                    
                    messagebox.showinfo("Success", "Meal logged successfully!")
                    
                    # Clear form fields
                    meal_type_var.set("")
                    food_var.set("")
                    calories_var.set(0)
                    protein_var.set(0)
                    carbs_var.set(0)
                    fat_var.set(0)
                    notes_text.delete("1.0", tk.END)
                    
                    # Refresh meal history if the function exists
                    if hasattr(self, 'load_meal_history'):
                        self.load_meal_history()
                        
                else:
                    messagebox.showerror("Error", "Member not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to log meal: {str(e)}")
        
        # Save button
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        self._create_styled_button(
            button_frame, "🍽️ Log Meal", save_meal, self.colors['success']
        ).pack()
        
        # Right side - Today's nutrition summary
        summary_frame = tk.LabelFrame(
            form_container,
            text="Today's Nutrition Summary",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=self.colors['primary']
        )
        summary_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Calculate today's nutrition stats
        today = datetime.now().strftime("%Y-%m-%d")
        today_meals = 0
        today_calories = 0
        today_protein = 0
        today_carbs = 0
        today_fat = 0
        
        for member in self.system.view_members():
            if hasattr(member, "meals") and member.meals:
                for meal in member.meals:
                    if meal["date"].strftime("%Y-%m-%d") == today:
                        today_meals += 1
                        today_calories += meal.get("calories", 0)
                        today_protein += meal.get("protein", 0)
                        today_carbs += meal.get("carbs", 0)
                        today_fat += meal.get("fat", 0)
        
        tk.Label(
            summary_frame,
            text=f"Meals Logged Today: {today_meals}",
            font=("Segoe UI", 12),
            bg="white"
        ).pack(pady=10)
        
        tk.Label(
            summary_frame,
            text=f"Total Calories: {today_calories}",
            font=("Segoe UI", 12),
            bg="white"
        ).pack(pady=5)
        
        tk.Label(
            summary_frame,
            text=f"Protein: {today_protein}g",
            font=("Segoe UI", 11),
            bg="white"
        ).pack(pady=2)
        
        tk.Label(
            summary_frame,
            text=f"Carbs: {today_carbs}g",
            font=("Segoe UI", 11),
            bg="white"
        ).pack(pady=2)
        
        tk.Label(
            summary_frame,
            text=f"Fat: {today_fat}g",
            font=("Segoe UI", 11),
            bg="white"
        ).pack(pady=2)

    def _create_meal_history_tab(self, parent):
        """Create meal history view with filtering"""
        # Controls frame
        controls_frame = tk.Frame(parent, bg="white")
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Member filter
        tk.Label(controls_frame, text="Member:", font=("Segoe UI", 11, "bold"), 
                bg="white").pack(side=tk.LEFT, padx=5)
        history_member_var = tk.StringVar()
        member_filter = ttk.Combobox(controls_frame, textvariable=history_member_var, width=25)
        member_filter['values'] = ["All Members"] + [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_filter.set("All Members")
        member_filter.pack(side=tk.LEFT, padx=5)
        
        # Meal type filter
        tk.Label(controls_frame, text="Meal Type:", font=("Segoe UI", 11, "bold"), 
                bg="white").pack(side=tk.LEFT, padx=5)
        meal_type_filter_var = tk.StringVar()
        meal_type_filter = ttk.Combobox(controls_frame, textvariable=meal_type_filter_var, width=15)
        meal_type_filter['values'] = ["All"] + ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-Workout", "Post-Workout"]
        meal_type_filter.set("All")
        meal_type_filter.pack(side=tk.LEFT, padx=5)
        
        # Date filter
        tk.Label(controls_frame, text="Date (YYYY-MM-DD):", font=("Segoe UI", 11, "bold"), 
                bg="white").pack(side=tk.LEFT, padx=5)
        date_filter_var = tk.StringVar()
        date_filter = tk.Entry(controls_frame, textvariable=date_filter_var, width=12)
        date_filter.pack(side=tk.LEFT, padx=5)
        
        # History table
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Date", "Member", "Meal Type", "Food Items", "Calories", "Protein", "Carbs", "Fat", "Notes")
        self.meal_history_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure column widths
        column_widths = {
            "Date": 140,
            "Member": 120,
            "Meal Type": 100,
            "Food Items": 200,
            "Calories": 80,
            "Protein": 80,
            "Carbs": 80,
            "Fat": 80,
            "Notes": 150
        }
        
        for col in columns:
            self.meal_history_table.heading(col, text=col)
            self.meal_history_table.column(col, width=column_widths.get(col, 100))
        
        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.meal_history_table.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.meal_history_table.xview)
        
        self.meal_history_table.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        
        self.meal_history_table.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load meal history function
        def load_meal_history():
            # Clear existing items
            for item in self.meal_history_table.get_children():
                self.meal_history_table.delete(item)
            
            meals_found = 0
            for member in self.system.view_members():
                if hasattr(member, "meals") and member.meals:
                    for meal in member.meals:
                        # Apply filters
                        if history_member_var.get() != "All Members" and history_member_var.get():
                            selected_member_id = history_member_var.get().split(" - ")[0]
                            if member.member_id != selected_member_id:
                                continue
                        
                        if meal_type_filter_var.get() != "All" and meal_type_filter_var.get():
                            if meal.get("meal_type") != meal_type_filter_var.get():
                                continue
                        
                        if date_filter_var.get():
                            try:
                                if meal["date"].strftime("%Y-%m-%d") != date_filter_var.get():
                                    continue
                            except:
                                continue
                        
                        # Truncate long text for display
                        food_items = meal.get("food_items", "")
                        if len(food_items) > 30:
                            food_items = food_items[:30] + "..."

                        notes = meal.get("notes", "")
                        if len(notes) > 20:
                            notes = notes[:20] + "..."

                        self.meal_history_table.insert("", tk.END, values=(
                            meal["date"].strftime("%Y-%m-%d %H:%M"),
                            member.name,
                            meal.get("meal_type", ""),
                            food_items,
                            meal.get("calories", 0),
                            meal.get("protein", 0),
                            meal.get("carbs", 0),
                            meal.get("fat", 0),
                            notes
                        ))
                        meals_found += 1
            
            # Update status label
            if hasattr(self, 'meal_status_label'):
                self.meal_status_label.config(text=f"Total meals found: {meals_found}")
        
        # Bind filter events
        member_filter.bind("<<ComboboxSelected>>", lambda e: load_meal_history())
        meal_type_filter.bind("<<ComboboxSelected>>", lambda e: load_meal_history())
        date_filter.bind("<KeyRelease>", lambda e: load_meal_history())
        
        # Refresh button
        self._create_styled_button(
            controls_frame, "🔄 Refresh", load_meal_history, self.colors['accent']
        ).pack(side=tk.RIGHT, padx=5)
        
        # Status label
        status_frame = tk.Frame(parent, bg="white")
        status_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.meal_status_label = tk.Label(
            status_frame,
            text="Total meals found: 0",
            font=("Segoe UI", 10),
            bg="white",
            fg="gray"
        )
        self.meal_status_label.pack(anchor=tk.W)
        
        # Store the function reference for external calls
        self.load_meal_history = load_meal_history
        
        # Initial load
        load_meal_history()

    def _create_nutrition_analysis_tab(self, parent):
        """Create nutrition analysis and recommendations tab"""
        analysis_frame = tk.Frame(parent, bg="white")
        analysis_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            analysis_frame,
            text="Nutrition Analysis & Recommendations",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg=self.colors['primary']
        ).pack(pady=10)
        
        # Member selection for analysis
        selection_frame = tk.Frame(analysis_frame, bg="white")
        selection_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(selection_frame, text="Select Member for Analysis:", font=("Segoe UI", 12, "bold"), 
                bg="white").pack(side=tk.LEFT, padx=5)
        
        analysis_member_var = tk.StringVar()
        analysis_member_combo = ttk.Combobox(selection_frame, textvariable=analysis_member_var, width=30)
        analysis_member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        analysis_member_combo.pack(side=tk.LEFT, padx=5)
        
        # Analysis results frame
        results_frame = tk.Frame(analysis_frame, bg="white")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        def show_nutrition_analysis():
            # Clear previous analysis
            for widget in results_frame.winfo_children():
                widget.destroy()
                
            if not analysis_member_var.get():
                tk.Label(results_frame, text="Please select a member to view analysis", 
                       bg="white", font=("Segoe UI", 12)).pack(pady=50)
                return
                
            member_id = analysis_member_var.get().split(" - ")[0]
            member = self.system.find_member_by_id(member_id)
            
            if not member or not hasattr(member, "meals") or not member.meals:
                tk.Label(results_frame, text="No meal data available for this member", 
                       bg="white", font=("Segoe UI", 12)).pack(pady=50)
                return
            
            # Calculate nutrition statistics
            total_calories = sum(m.get("calories", 0) for m in member.meals)
            total_protein = sum(m.get("protein", 0) for m in member.meals)
            total_carbs = sum(m.get("carbs", 0) for m in member.meals)
            total_fat = sum(m.get("fat", 0) for m in member.meals)
            
            days_tracked = len(set(m["date"].strftime("%Y-%m-%d") for m in member.meals))
            avg_calories = total_calories / max(1, days_tracked)
            avg_protein = total_protein / max(1, days_tracked)
            
            # Display statistics
            stats_frame = tk.LabelFrame(
                results_frame,
                text=f"Nutrition Summary for {member.name}",
                font=("Segoe UI", 12, "bold"),
                bg="white",
                               fg=self.colors['primary']
            )
            stats_frame.pack(fill=tk.X, pady=10)
            
            stats_grid = tk.Frame(stats_frame, bg="white")
            stats_grid.pack(padx=15, pady=15)
            
            # First row
            tk.Label(stats_grid, text=f"Total Meals Logged: {len(member.meals)}", 
                   bg="white", font=("Segoe UI", 11)).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(stats_grid, text=f"Days Tracked: {days_tracked}", 
                   bg="white", font=("Segoe UI", 11)).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
            
            # Second row
            tk.Label(stats_grid, text=f"Total Calories: {total_calories}", 
                   bg="white", font=("Segoe UI", 11)).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(stats_grid, text=f"Avg Calories/Day: {avg_calories:.0f}", 
                   bg="white", font=("Segoe UI", 11)).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
            
            # Third row
            tk.Label(stats_grid, text=f"Total Protein: {total_protein}g", 
                   bg="white", font=("Segoe UI", 11)).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(stats_grid, text=f"Avg Protein/Day: {avg_protein:.0f}g", 
                   bg="white", font=("Segoe UI", 11)).grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
            
            # Recommendations
            recommendations_frame = tk.LabelFrame(
                results_frame,
                text="Nutrition Recommendations",
                font=("Segoe UI", 12, "bold"),
                bg="white",
                fg=self.colors['primary']
            )
            recommendations_frame.pack(fill=tk.X, pady=10)
            
            # Generate recommendations based on member's goals and data
            recommendations = []
            
            if member.fitness_goals == "Weight Loss":
                if avg_calories > 2000:
                    recommendations.append("🍎 Consider reducing daily calorie intake for weight loss goals")
                if avg_protein < 80:
                    recommendations.append("🥩 Increase protein intake to preserve muscle during weight loss")
                    
            elif member.fitness_goals == "Muscle Gain":
                if avg_calories < 2500:
                    recommendations.append("🍽️ Increase calorie intake to support muscle building")
                if avg_protein < 100:
                    recommendations.append("💪 Aim for higher protein intake (1.6-2.2g per kg body weight)")
                    
            elif member.fitness_goals == "Endurance":
                if total_carbs / max(1, days_tracked) < 150:
                    recommendations.append("🍝 Increase carbohydrate intake to fuel endurance activities")
                    
            # General recommendations
            if days_tracked < 7:
                recommendations.append("📝 Try to log meals more consistently for better analysis")
                
            meal_types = set(m.get("meal_type") for m in member.meals)
            if "Breakfast" not in meal_types:
                recommendations.append("🌅 Don't skip breakfast - it's important for metabolism")
                
            # Display recommendations
            if recommendations:
                for rec in recommendations:
                    tk.Label(
                        recommendations_frame,
                        text=rec,
                        bg="white",
                        font=("Segoe UI", 11),
                        wraplength=600,
                        justify=tk.LEFT
                    ).pack(anchor=tk.W, padx=15, pady=3)
            else:
                tk.Label(
                    recommendations_frame,
                    text="✅ Great job! Your nutrition tracking looks good. Keep it up!",
                    bg="white",
                    font=("Segoe UI", 11),
                    fg=self.colors['success']
                ).pack(anchor=tk.W, padx=15, pady=10)
        
        analysis_member_combo.bind("<<ComboboxSelected>>", lambda e: show_nutrition_analysis())
        
        # Analyze button
        self._create_styled_button(
            selection_frame, "📊 Analyze Nutrition", show_nutrition_analysis, self.colors['accent']
        ).pack(side=tk.LEFT, padx=10)

    def show_reports(self):
        self._clear_content_frame()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        page_title = tk.Label(title_frame, text="Reports & Analytics", font=("Arial", 20, "bold"), bg="#f0f0f0")
        page_title.pack(side=tk.LEFT)
        
        # Create a notebook for different report types
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tab 1: Fitness Report
        fitness_report_frame = tk.Frame(notebook, bg="white")
        notebook.add(fitness_report_frame, text="Fitness Report")
        
        # Tab 2: Nutrition Report
        nutrition_report_frame = tk.Frame(notebook, bg="white")
        notebook.add(nutrition_report_frame, text="Nutrition Report")
        
        # Tab 3: Performance Analysis
        performance_frame = tk.Frame(notebook, bg="white")
        notebook.add(performance_frame, text="Performance Analysis")
        
        # Tab 4: Business Analytics
        business_frame = tk.Frame(notebook, bg="white")
        notebook.add(business_frame, text="Business Analytics")
        
        # Create comprehensive reports
        self._create_comprehensive_fitness_report(fitness_report_frame)
        self._create_comprehensive_nutrition_report(nutrition_report_frame)
        self._create_performance_analysis_report(performance_frame)
        self._create_business_analytics_report(business_frame)

    def _create_comprehensive_fitness_report(self, parent):
        """Create comprehensive fitness report with real data"""
        # Member selection
        selection_frame = tk.Frame(parent, bg="white")
        selection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(selection_frame, text="Select Member for Detailed Report:", 
               font=("Segoe UI", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=5)
        
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(selection_frame, textvariable=member_var, width=30)
        member_combo['values'] = ["All Members"] + [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.set("All Members")
        member_combo.pack(side=tk.LEFT, padx=5)
        
        # Report content area
        report_content = tk.Frame(parent, bg="white")
        report_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def generate_fitness_report():
            # Clear previous report
            for widget in report_content.winfo_children():
                widget.destroy()
            
            # Create scrollable report area
            canvas = tk.Canvas(report_content, bg="white")
            scrollbar = ttk.Scrollbar(report_content, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")
            
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            if member_var.get() == "All Members":
                self._generate_overall_fitness_summary(scrollable_frame)
            else:
                member_id = member_var.get().split(" - ")[0]
                member = self.system.find_member_by_id(member_id)
                if member:
                    self._generate_individual_fitness_report(scrollable_frame, member)
            
            # Update scroll region
            scrollable_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_frame, width=e.width))
        
        # Generate button
        self._create_styled_button(
            selection_frame, "📊 Generate Report", generate_fitness_report, self.colors['success']
        ).pack(side=tk.LEFT, padx=10)
        
        member_combo.bind("<<ComboboxSelected>>", lambda e: generate_fitness_report())
        
        # Initial report generation
        generate_fitness_report()

    def _generate_overall_fitness_summary(self, parent):
        """Generate overall fitness summary for all members"""
        # Header
        header = tk.Label(parent, text="Overall Fitness Summary Report", 
                         font=("Segoe UI", 18, "bold"), bg="white", fg=self.colors['primary'])
        header.pack(pady=20)
        
        # Key Statistics
        stats_frame = tk.LabelFrame(parent, text="Key Statistics", 
                                  font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        total_members = len(self.system.view_members())
        total_workouts = 0
        total_calories_burned = 0
        total_goals = 0
        completed_goals = 0
        
        for member in self.system.view_members():
            if hasattr(member, 'workouts') and member.workouts:
                total_workouts += len(member.workouts)
                total_calories_burned += sum(w.get('calories', 0) for w in member.workouts)
            
            if hasattr(member, 'goals') and member.goals:
                total_goals += len(member.goals)
                completed_goals += len([g for g in member.goals if g.get('progress', 0) >= 100])
        
        # Display stats in grid
        stats_grid = tk.Frame(stats_frame, bg="white")
        stats_grid.pack()
        
        stats_data = [
            ("Total Active Members", total_members),
            ("Total Workouts Logged", total_workouts),
            ("Total Calories Burned", f"{total_calories_burned:,}"),
            ("Total Goals Set", total_goals),
            ("Goals Completed", completed_goals),
            ("Average Workouts per Member", f"{total_workouts/max(1, total_members):.1f}")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            stat_frame = tk.Frame(stats_grid, bg=self.colors['accent'], relief=tk.RAISED, bd=2)
            stat_frame.grid(row=row, column=col, padx=10, pady=10, ipadx=20, ipady=10, sticky="ew")
            
            tk.Label(stat_frame, text=str(value), font=("Segoe UI", 16, "bold"), 
                   bg=self.colors['accent'], fg="white").pack()
            tk.Label(stat_frame, text=label, font=("Segoe UI", 10), 
                   bg=self.colors['accent'], fg="white").pack()
        
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        
        # Exercise Type Analysis
        exercise_frame = tk.LabelFrame(parent, text="Exercise Type Analysis", 
                                     font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        exercise_frame.pack(fill=tk.X, padx=20, pady=10)
        
        exercise_counts = {}
        for member in self.system.view_members():
            if hasattr(member, 'workouts') and member.workouts:
                for workout in member.workouts:
                    ex_type = workout.get('exercise_type', 'Other')
                    exercise_counts[ex_type] = exercise_counts.get(ex_type, 0) + 1
        
        if exercise_counts:
            tk.Label(exercise_frame, text="Most Popular Exercises:", 
                   font=("Segoe UI", 12, "bold"), bg="white").pack(anchor=tk.W, pady=5)
            
            sorted_exercises = sorted(exercise_counts.items(), key=lambda x: x[1], reverse=True)
            for exercise, count in sorted_exercises[:5]:
                percentage = (count / sum(exercise_counts.values())) * 100
                tk.Label(exercise_frame, 
                       text=f"• {exercise}: {count} sessions ({percentage:.1f}%)", 
                       bg="white", font=("Segoe UI", 11)).pack(anchor=tk.W, padx=10)
        else:
            tk.Label(exercise_frame, text="No workout data available", 
                   bg="white", font=("Segoe UI", 11)).pack(pady=10)
        
        # Member Activity Levels
        activity_frame = tk.LabelFrame(parent, text="Member Activity Levels", 
                                     font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        activity_frame.pack(fill=tk.X, padx=20, pady=10)
        
        activity_levels = {"High (10+ workouts)": 0, "Medium (5-9 workouts)": 0, "Low (1-4 workouts)": 0, "Inactive (0 workouts)": 0}
        
        for member in self.system.view_members():
            workout_count = len(member.workouts) if hasattr(member, 'workouts') and member.workouts else 0
            
            if workout_count >= 10:
                activity_levels["High (10+ workouts)"] += 1
            elif workout_count >= 5:
                activity_levels["Medium (5-9 workouts)"] += 1
            elif workout_count >= 1:
                activity_levels["Low (1-4 workouts)"] += 1
            else:
                activity_levels["Inactive (0 workouts)"] += 1
        
        for level, count in activity_levels.items():
            percentage = (count / max(1, total_members)) * 100
            tk.Label(activity_frame, 
                   text=f"• {level}: {count} members ({percentage:.1f}%)", 
                   bg="white", font=("Segoe UI", 11)).pack(anchor=tk.W, padx=10, pady=2)

    def _generate_individual_fitness_report(self, parent, member):
        """Generate detailed fitness report for individual member"""
        # Header
        header = tk.Label(parent, text=f"Fitness Report: {member.name}", 
                         font=("Segoe UI", 18, "bold"), bg="white", fg=self.colors['primary'])
        header.pack(pady=20)
        
        # Member Info
        info_frame = tk.LabelFrame(parent, text="Member Information", 
                                 font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        info_grid = tk.Frame(info_frame, bg="white")
        info_grid.pack()
        
        member_info = [
            ("Member ID", member.member_id),
            ("Age", f"{member.age} years"),
            ("Membership Type", member.membership_type),
            ("Fitness Goals", member.fitness_goals)
        ]
        
        for i, (label, value) in enumerate(member_info):
            tk.Label(info_grid, text=f"{label}:", font=("Segoe UI", 11, "bold"), 
                   bg="white").grid(row=i//2, column=(i%2)*2, sticky=tk.W, padx=10, pady=5)
            tk.Label(info_grid, text=str(value), font=("Segoe UI", 11), 
                   bg="white").grid(row=i//2, column=(i%2)*2+1, sticky=tk.W, padx=10, pady=5)
        
        # Workout Summary
        workout_frame = tk.LabelFrame(parent, text="Workout Summary", 
                                    font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        workout_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if hasattr(member, 'workouts') and member.workouts:
            total_workouts = len(member.workouts)
            total_calories = sum(w.get('calories', 0) for w in member.workouts)
            total_duration = sum(w.get('duration', 0) for w in member.workouts)
            avg_calories = total_calories / total_workouts if total_workouts > 0 else 0
            
            workout_stats = [
                ("Total Workouts", total_workouts),
                ("Total Calories Burned", f"{total_calories:,}"),
                ("Total Duration", f"{total_duration} minutes"),
                ("Average Calories per Workout", f"{avg_calories:.0f}")
            ]
            
            workout_grid = tk.Frame(workout_frame, bg="white")
            workout_grid.pack()
            
            for i, (label, value) in enumerate(workout_stats):
                stat_frame = tk.Frame(workout_grid, bg=self.colors['warning'], relief=tk.RAISED, bd=2)
                stat_frame.grid(row=i//2, column=i%2, padx=10, pady=5, ipadx=15, ipady=8, sticky="ew")
                
                tk.Label(stat_frame, text=str(value), font=("Segoe UI", 14, "bold"), 
                       bg=self.colors['warning'], fg="white").pack()
                tk.Label(stat_frame, text=label, font=("Segoe UI", 9), 
                       bg=self.colors['warning'], fg="white").pack()
            
            workout_grid.grid_columnconfigure(0, weight=1)
            workout_grid.grid_columnconfigure(1, weight=1)
            
            # Exercise breakdown
            exercise_counts = {}
            for workout in member.workouts:
                ex_type = workout.get('exercise_type', 'Other')
                exercise_counts[ex_type] = exercise_counts.get(ex_type, 0) + 1
            
            tk.Label(workout_frame, text="Exercise Types:", font=("Segoe UI", 12, "bold"), 
                   bg="white").pack(anchor=tk.W, pady=(10, 5))
            
            for ex_type, count in exercise_counts.items():
                percentage = (count / total_workouts) * 100
                tk.Label(workout_frame, 
                       text=f"• {ex_type}: {count} sessions ({percentage:.1f}%)", 
                       bg="white", font=("Segoe UI", 11)).pack(anchor=tk.W, padx=10)
        else:
            tk.Label(workout_frame, text="No workout data available for this member", 
                   bg="white", font=("Segoe UI", 11), fg="gray").pack(pady=20)
        
        # Goals Progress
        goals_frame = tk.LabelFrame(parent, text="Goals Progress", 
                                  font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        goals_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if hasattr(member, 'goals') and member.goals:
            for goal in member.goals:
                goal_container = tk.Frame(goals_frame, bg="white", relief=tk.RIDGE, bd=1)
                goal_container.pack(fill=tk.X, pady=5)
                
                tk.Label(goal_container, text=f"Goal: {goal.get('goal_type', 'Unknown')}", 
                       font=("Segoe UI", 11, "bold"), bg="white").pack(anchor=tk.W, padx=10, pady=2)
                
                tk.Label(goal_container, text=f"Target: {goal.get('target', 'N/A')}", 
                       font=("Segoe UI", 10), bg="white").pack(anchor=tk.W, padx=10)
                
                progress = goal.get('progress', 0)
                progress_frame = tk.Frame(goal_container, bg="white")
                progress_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Progress bar
                progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
                progress_bar['value'] = progress
                progress_bar.pack(side=tk.LEFT)
                
                tk.Label(progress_frame, text=f"{progress:.0f}%", 
                       font=("Segoe UI", 10), bg="white").pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(goals_frame, text="No goals set for this member", 
                   bg="white", font=("Segoe UI", 11), fg="gray").pack(pady=20)
        
        # Recommendations
        recommendations_frame = tk.LabelFrame(parent, text="Personalized Recommendations", 
                                            font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        recommendations_frame.pack(fill=tk.X, padx=20, pady=10)
        
        recommendations = self._generate_member_recommendations(member)
        
        for rec in recommendations:
            tk.Label(recommendations_frame, text=f"• {rec}", 
                   bg="white", font=("Segoe UI", 11), wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=2)

    def _generate_member_recommendations(self, member):
        """Generate personalized recommendations for a member"""
        recommendations = []
        
        if hasattr(member, 'workouts') and member.workouts:
            workout_count = len(member.workouts)
            total_calories = sum(w.get('calories', 0) for w in member.workouts)
            avg_calories = total_calories / workout_count if workout_count > 0 else 0
            
            # Weekly workout frequency
            recent_workouts = [w for w in member.workouts 
                             if (datetime.now() - w['date']).days <= 7]
            
            if len(recent_workouts) < 3:
                recommendations.append("Try to increase your workout frequency to at least 3 times per week")
            
            if avg_calories < 300:
                recommendations.append("Consider increasing workout intensity to burn more calories")
            
            # Exercise variety
            exercise_types = set(w.get('exercise_type') for w in member.workouts)
            if len(exercise_types) < 3:
                recommendations.append("Add more variety to your workouts by trying different exercise types")
            
            # Goal-specific recommendations
            if member.fitness_goals == "Weight Loss" and avg_calories < 400:
                recommendations.append("For weight loss, focus on higher calorie-burning exercises like HIIT or running")
            elif member.fitness_goals == "Muscle Gain":
                strength_workouts = [w for w in member.workouts if w.get('exercise_type') == 'Weight Lifting']
                if len(strength_workouts) / workout_count < 0.5:
                    recommendations.append("Increase strength training to at least 50% of your workouts for muscle gain")
            elif member.fitness_goals == "Endurance":
                cardio_workouts = [w for w in member.workouts if w.get('exercise_type') in ['Running', 'Cycling', 'Swimming']]
                if len(cardio_workouts) / workout_count < 0.6:
                    recommendations.append("Focus more on cardio exercises to improve endurance")
        else:
            recommendations.append("Start tracking your workouts to get personalized recommendations")
            recommendations.append("Begin with 3-4 workouts per week, mixing cardio and strength training")
        
        # Nutrition recommendations if meal data exists
        if hasattr(member, 'meals') and member.meals:
            total_calories = sum(m.get('calories', 0) for m in member.meals)
            days_tracked = len(set(m['date'].strftime('%Y-%m-%d') for m in member.meals))
            avg_daily_calories = total_calories / max(1, days_tracked)
            
            if member.fitness_goals == "Weight Loss" and avg_daily_calories > 2000:
                recommendations.append("Consider reducing daily calorie intake to support weight loss")
            elif member.fitness_goals == "Muscle Gain" and avg_daily_calories < 2500:
                recommendations.append("Increase calorie intake to support muscle building")
        
        if not recommendations:
            recommendations.append("Keep up the great work! Consistency is key to achieving your fitness goals")
        
        return recommendations

    def _create_comprehensive_nutrition_report(self, parent):
        """Create comprehensive nutrition report"""
        # Member selection
        selection_frame = tk.Frame(parent, bg="white")
        selection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(selection_frame, text="Select Member for Nutrition Report:", 
               font=("Segoe UI", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=5)
        
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(selection_frame, textvariable=member_var, width=30)
        member_combo['values'] = ["All Members"] + [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.set("All Members")
        member_combo.pack(side=tk.LEFT, padx=5)
        
        # Report content area
        report_content = tk.Frame(parent, bg="white")
        report_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def generate_nutrition_report():
            # Clear previous report
            for widget in report_content.winfo_children():
                widget.destroy()
            
            # Create scrollable report area
            canvas = tk.Canvas(report_content, bg="white")
            scrollbar = ttk.Scrollbar(report_content, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")
            
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            if member_var.get() == "All Members":
                self._generate_overall_nutrition_summary(scrollable_frame)
            else:
                member_id = member_var.get().split(" - ")[0]
                member = self.system.find_member_by_id(member_id)
                if member:
                    self._generate_individual_nutrition_report(scrollable_frame, member)
            
            # Update scroll region
            scrollable_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_frame, width=e.width))
        
        # Generate button
        self._create_styled_button(
            selection_frame, "🥗 Generate Report", generate_nutrition_report, self.colors['success']
        ).pack(side=tk.LEFT, padx=10)
        
        member_combo.bind("<<ComboboxSelected>>", lambda e: generate_nutrition_report())
        
        # Initial report generation
        generate_nutrition_report()

    def _generate_overall_nutrition_summary(self, parent):
        """Generate overall nutrition summary for all members"""
        # Header
        header = tk.Label(parent, text="Overall Nutrition Summary Report", 
                         font=("Segoe UI", 18, "bold"), bg="white", fg=self.colors['primary'])
        header.pack(pady=20)
        
        # Calculate overall nutrition statistics
        total_meals = 0
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        tracking_members = 0
        
        for member in self.system.view_members():
            if hasattr(member, 'meals') and member.meals:
                tracking_members += 1
                total_meals += len(member.meals)
                for meal in member.meals:
                    total_calories += meal.get('calories', 0)
                    total_protein += meal.get('protein', 0)
                    total_carbs += meal.get('carbs', 0)
                    total_fat += meal.get('fat', 0)
        
        # Key Statistics
        stats_frame = tk.LabelFrame(parent, text="Nutrition Statistics", 
                                  font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if tracking_members > 0:
            stats_data = [
                ("Members Tracking Nutrition", tracking_members),
                ("Total Meals Logged", total_meals),
                ("Total Calories Consumed", f"{total_calories:,}"),
                ("Average Meals per Member", f"{total_meals/tracking_members:.1f}"),
                ("Total Protein Consumed", f"{total_protein:,}g"),
                ("Total Carbohydrates", f"{total_carbs:,}g")
            ]
            
            stats_grid = tk.Frame(stats_frame, bg="white")
            stats_grid.pack()
            
            for i, (label, value) in enumerate(stats_data):
                row = i // 2
                col = i % 2
                
                stat_frame = tk.Frame(stats_grid, bg=self.colors['success'], relief=tk.RAISED, bd=2)
                stat_frame.grid(row=row, column=col, padx=10, pady=5, ipadx=15, ipady=8, sticky="ew")
                
                tk.Label(stat_frame, text=str(value), font=("Segoe UI", 14, "bold"), 
                       bg=self.colors['success'], fg="white").pack()
                tk.Label(stat_frame, text=label, font=("Segoe UI", 9), 
                       bg=self.colors['success'], fg="white").pack()
            
            stats_grid.grid_columnconfigure(0, weight=1)
            stats_grid.grid_columnconfigure(1, weight=1)
        else:
            tk.Label(stats_frame, text="No nutrition data available - encourage members to start tracking meals!", 
                   bg="white", font=("Segoe UI", 12), fg="gray").pack(pady=20)

    def _generate_individual_nutrition_report(self, parent, member):
        """Generate detailed nutrition report for individual member"""
        # Header
        header = tk.Label(parent, text=f"Nutrition Report: {member.name}", 
                         font=("Segoe UI", 18, "bold"), bg="white", fg=self.colors['primary'])
        header.pack(pady=20)
        
        if not hasattr(member, 'meals') or not member.meals:
            tk.Label(parent, text="No nutrition data available for this member", 
                   bg="white", font=("Segoe UI", 14), fg="gray").pack(pady=50)
            return
        
        # Nutrition Summary
        nutrition_frame = tk.LabelFrame(parent, text="Nutrition Summary", 
                                      font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        nutrition_frame.pack(fill=tk.X, padx=20, pady=10)
        
        total_meals = len(member.meals)
        total_calories = sum(m.get('calories', 0) for m in member.meals)
        total_protein = sum(m.get('protein', 0) for m in member.meals)
        total_carbs = sum(m.get('carbs', 0) for m in member.meals)
        total_fat = sum(m.get('fat', 0) for m in member.meals)
        
        days_tracked = len(set(m['date'].strftime('%Y-%m-%d') for m in member.meals))
        avg_calories = total_calories / max(1, days_tracked)
        avg_protein = total_protein / max(1, days_tracked)
        
        nutrition_stats = [
            ("Total Meals Logged", total_meals),
            ("Days Tracked", days_tracked),
            ("Total Calories", f"{total_calories:,}"),
            ("Avg Calories/Day", f"{avg_calories:.0f}"),
            ("Total Protein", f"{total_protein}g"),
            ("Avg Protein/Day", f"{avg_protein:.0f}g")
        ]
        
        nutrition_grid = tk.Frame(nutrition_frame, bg="white")
        nutrition_grid.pack()
        
        for i, (label, value) in enumerate(nutrition_stats):
            row = i // 2
            col = i % 2
            
            stat_frame = tk.Frame(nutrition_grid, bg=self.colors['success'], relief=tk.RAISED, bd=2)
            stat_frame.grid(row=row, column=col, padx=10, pady=5, ipadx=15, ipady=8, sticky="ew")
            
            tk.Label(stat_frame, text=str(value), font=("Segoe UI", 14, "bold"), 
                   bg=self.colors['success'], fg="white").pack()
            tk.Label(stat_frame, text=label, font=("Segoe UI", 9), 
                   bg=self.colors['success'], fg="white").pack()
        
        nutrition_grid.grid_columnconfigure(0, weight=1)
        nutrition_grid.grid_columnconfigure(1, weight=1)
        
        # Meal Type Analysis
        meal_analysis_frame = tk.LabelFrame(parent, text="Meal Type Analysis", 
                                          font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        meal_analysis_frame.pack(fill=tk.X, padx=20, pady=10)
        
        meal_types = {}
        for meal in member.meals:
            meal_type = meal.get('meal_type', 'Other')
            meal_types[meal_type] = meal_types.get(meal_type, 0) + 1
        
        if meal_types:
            for meal_type, count in meal_types.items():
                percentage = (count / total_meals) * 100
                tk.Label(meal_analysis_frame, 
                       text=f"• {meal_type}: {count} meals ({percentage:.1f}%)", 
                       bg="white", font=("Segoe UI", 11)).pack(anchor=tk.W, padx=10, pady=2)
        
        # Nutrition Recommendations
        recommendations_frame = tk.LabelFrame(parent, text="Nutrition Recommendations", 
                                            font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        recommendations_frame.pack(fill=tk.X, padx=20, pady=10)
        
        recommendations = self._generate_nutrition_recommendations(member)
        
        for rec in recommendations:
            tk.Label(recommendations_frame, text=f"• {rec}", 
                   bg="white", font=("Segoe UI", 11), wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=2)

    def _generate_nutrition_recommendations(self, member):
        """Generate nutrition recommendations based on member data and goals"""
        recommendations = []
        
        if not hasattr(member, 'meals') or not member.meals:
            return ["Start tracking your meals to get personalized nutrition recommendations"]
        
        total_calories = sum(m.get('calories', 0) for m in member.meals)
        total_protein = sum(m.get('protein', 0) for m in member.meals)
        days_tracked = len(set(m['date'].strftime('%Y-%m-%d') for m in member.meals))
        
        avg_calories = total_calories / max(1, days_tracked)
        avg_protein = total_protein / max(1, days_tracked)
        
        # Goal-specific recommendations
        if member.fitness_goals == "Weight Loss":
            if avg_calories > 2000:
                recommendations.append("Consider reducing daily calorie intake to 1800-2000 for weight loss")
            if avg_protein < 80:
                recommendations.append("Increase protein intake to preserve muscle during weight loss")
        
        elif member.fitness_goals == "Muscle Gain":
            if avg_calories < 2500:
                recommendations.append("Increase calorie intake to 2500-3000 to support muscle building")
            if avg_protein < 100:
                recommendations.append("Aim for higher protein intake (1.6-2.2g per kg body weight)")
        
        # General recommendations
        meal_types = set(m.get('meal_type') for m in member.meals)
        if "Breakfast" not in meal_types:
            recommendations.append("Don't skip breakfast - it's important for metabolism")
        
        if days_tracked < 7:
            recommendations.append("Try to log meals more consistently for better analysis")
        
        if avg_protein < 50:
            recommendations.append("Increase overall protein intake for better muscle recovery")
        
        if not recommendations:
            recommendations.append("Great job with your nutrition tracking! Keep maintaining a balanced diet")
        
        return recommendations

    def _create_performance_analysis_report(self, parent):
        """Create performance analysis report"""
        tk.Label(parent, text="Performance Analysis Report", 
               font=("Segoe UI", 18, "bold"), bg="white", fg=self.colors['primary']).pack(pady=20)
        
        tk.Label(parent, text="Track progress over time, identify trends, and measure improvements", 
               font=("Segoe UI", 12), bg="white", fg="gray").pack(pady=10)
        
        # This would contain charts and graphs if matplotlib is available
        if not MATPLOTLIB_AVAILABLE:
            tk.Label(parent, text="Charts and graphs require matplotlib installation", 
                   font=("Segoe UI", 12), bg="white", fg="red").pack(pady=20)
        
        # Member progress tracking would go here
        progress_frame = tk.LabelFrame(parent, text="Member Progress Tracking", 
                                     font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(progress_frame, text="Performance analysis features will be enhanced with matplotlib charts", 
               bg="white").pack(pady=50)

    def _create_business_analytics_report(self, parent):
        """Create business analytics report"""
        tk.Label(parent, text="Business Analytics Report", 
               font=("Segoe UI", 18, "bold"), bg="white", fg=self.colors['primary']).pack(pady=20)
        
        # Revenue Analysis
        revenue_frame = tk.LabelFrame(parent, text="Revenue Analysis", 
                                    font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        revenue_frame.pack(fill=tk.X, padx=20, pady=10)
        
        total_revenue = sum(t.amount_paid for t in self.system.transactions)
        membership_revenue = {"Basic": 0, "Premium": 0, "VIP": 0}
        
        for transaction in self.system.transactions:
            if hasattr(transaction.member, 'membership_type'):
                membership_type = transaction.member.membership_type
                if membership_type in membership_revenue:
                    membership_revenue[membership_type] += transaction.amount_paid
        
        tk.Label(revenue_frame, text=f"Total Revenue: ${total_revenue:.2f}", 
               font=("Segoe UI", 14, "bold"), bg="white", fg=self.colors['success']).pack(pady=10)
        
        for membership_type, revenue in membership_revenue.items():
            percentage = (revenue / max(1, total_revenue)) * 100
            tk.Label(revenue_frame, 
                   text=f"{membership_type} Membership: ${revenue:.2f} ({percentage:.1f}%)", 
                   bg="white", font=("Segoe UI", 11)).pack(anchor=tk.W, padx=10, pady=2)
        
        # Membership Distribution
        membership_frame = tk.LabelFrame(parent, text="Membership Distribution", 
                                       font=("Segoe UI", 14, "bold"), bg="white", padx=20, pady=15)
        membership_frame.pack(fill=tk.X, padx=20, pady=10)
        
        membership_counts = {"Basic": 0, "Premium": 0, "VIP": 0}
        for member in self.system.view_members():
            if member.membership_type in membership_counts:
                membership_counts[member.membership_type] += 1
        
        total_members = sum(membership_counts.values())
        
        for membership_type, count in membership_counts.items():
            percentage = (count / max(1, total_members)) * 100
            tk.Label(membership_frame, 
                   text=f"{membership_type}: {count} members ({percentage:.1f}%)", 
                   bg="white", font=("Segoe UI", 11)).pack(anchor=tk.W, padx=10, pady=2)

def main():
    try:
        print("Starting Smart Fitness Management System...")
        
        # Check if matplotlib is available
        if not MATPLOTLIB_AVAILABLE:
            print("Warning: Charts and graphs will not be available without matplotlib")
            print("To install matplotlib, run: pip install matplotlib")
        
        root = tk.Tk()
        print("Tkinter initialized successfully")
        
        # Set window to appear in front
        try:
            root.attributes('-topmost', True)
            root.update()
            root.attributes('-topmost', False)
        except:
            pass  # Handle cases where this might not work
        
        # Create the application
        print("Creating application...")
        app = SmartFitnessApp(root)
        print("Application created successfully")
        print("UI should be visible now. If you don't see it, check if it's minimized or behind other windows")
        
        # Start the main loop
        root.mainloop()
        
    except ImportError as e:
        print(f"ERROR: Required module not found: {e}")
        print("Please make sure you've installed all required packages:")
        print("Try running these commands:")
        print("pip install matplotlib")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
