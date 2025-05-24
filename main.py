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
                bg=self.colors['white']).pack(side=tk.LEFT, padx=5)
        history_member_var = tk.StringVar()
        member_filter = ttk.Combobox(controls_frame, textvariable=history_member_var, width=25)
        member_filter['values'] = ["All Members"] + [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_filter.set("All Members")
        member_filter.pack(side=tk.LEFT, padx=5)
        
        # Exercise filter
        tk.Label(controls_frame, text="Exercise:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).pack(side=tk.LEFT, padx=5)
        exercise_filter_var = tk.StringVar()
        exercise_filter = ttk.Combobox(controls_frame, textvariable=exercise_filter_var, width=15)
        exercise_filter['values'] = ["All"] + ["Running", "Weight Lifting", "Yoga", "Swimming", "Cycling"]
        exercise_filter.set("All")
        exercise_filter.pack(side=tk.LEFT, padx=5)
        
        # Date filter
        tk.Label(controls_frame, text="Date:", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['white']).pack(side=tk.LEFT, padx=5)
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
        
        # Create a notebook for nutrition tracking
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tab 1: Log Meals
        log_meals_frame = tk.Frame(notebook, bg="white")
        notebook.add(log_meals_frame, text="Log Meals")
        
        # Tab 2: Meal History
        meal_history_frame = tk.Frame(notebook, bg="white")
        notebook.add(meal_history_frame, text="Meal History")
        
        # Meal logging form
        meal_form_frame = tk.LabelFrame(log_meals_frame, text="Log New Meal", bg="white", padx=15, pady=15)
        meal_form_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Member selection
        tk.Label(meal_form_frame, text="Select Member:", bg="white").pack(anchor=tk.W, pady=5)
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(meal_form_frame, textvariable=member_var, width=30)
        member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.pack(anchor=tk.W, pady=5)
        
        # Meal type
        tk.Label(meal_form_frame, text="Meal Type:", bg="white").pack(anchor=tk.W, pady=5)
        meal_type_var = tk.StringVar()
        meal_types = ["Breakfast", "Lunch", "Dinner", "Snack"]
        meal_type_combo = ttk.Combobox(meal_form_frame, textvariable=meal_type_var, width=30, values=meal_types)
        meal_type_combo.pack(anchor=tk.W, pady=5)
        
        # Food items
        tk.Label(meal_form_frame, text="Food Items:", bg="white").pack(anchor=tk.W, pady=5)
        food_var = tk.StringVar()
        food_entry = tk.Entry(meal_form_frame, textvariable=food_var, width=32)
        food_entry.pack(anchor=tk.W, pady=5)
        
        # Calories
        tk.Label(meal_form_frame, text="Calories:", bg="white").pack(anchor=tk.W, pady=5)
        calories_var = tk.StringVar()
        calories_entry = tk.Entry(meal_form_frame, textvariable=calories_var, width=32)
        calories_entry.pack(anchor=tk.W, pady=5)
        
        def save_meal():
            if all([member_var.get(), meal_type_var.get(), food_var.get(), calories_var.get()]):
                member_id = member_var.get().split(" - ")[0]
                member = self.system.find_member_by_id(member_id)
                if member:
                    if not hasattr(member, "meals"):
                        member.meals = []
                    meal = {
                        "id": str(uuid.uuid4()),
                        "date": datetime.now(),
                        "meal_type": meal_type_var.get(),
                        "food_items": food_var.get(),
                        "calories": int(calories_var.get()),
                        "protein": 0,
                        "carbs": 0,
                        "fat": 0
                    }
                    member.meals.append(meal)
                    messagebox.showinfo("Success", "Meal logged successfully!")
                    meal_type_var.set("")
                    food_var.set("")
                    calories_var.set("")
            else:
                messagebox.showwarning("Missing Information", "Please fill in all fields.")
        
        tk.Button(meal_form_frame, text="Log Meal", bg="#2ecc71", fg="white",
                 font=("Arial", 12), command=save_meal).pack(pady=10)

    def show_reports(self):
        self._clear_content_frame()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        page_title = tk.Label(title_frame, text="Reports & Analytics", font=("Arial", 20, "bold"), bg="#f0f0f0")
        page_title.pack(side=tk.LEFT)
        
        # Reports options
        options_frame = tk.Frame(self.content_frame, bg="white", padx=15, pady=15)
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Report selection
        tk.Label(options_frame, text="Select Report Type:", bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        report_var = tk.StringVar(value="Fitness Report")
        report_types = ["Fitness Report", "Nutrition Report", "Revenue Report", "Membership Analysis"]
        
        for report_type in report_types:
            rb = tk.Radiobutton(options_frame, text=report_type, variable=report_var, 
                             value=report_type, bg="white", font=("Arial", 11))
            rb.pack(anchor=tk.W, pady=3)
        
        # Report content frame
        self.reports_frame = tk.Frame(self.content_frame, bg="white")
        self.reports_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def generate_report():
            # Clear previous report
            for widget in self.reports_frame.winfo_children():
                widget.destroy()
            
            report_type = report_var.get()
            
            if report_type == "Fitness Report":
                self._generate_fitness_report()
            elif report_type == "Nutrition Report":
                self._generate_nutrition_report()
            elif report_type == "Revenue Report":
                self._generate_revenue_report()
            elif report_type == "Membership Analysis":
                self._generate_membership_analysis()
        
        generate_btn = tk.Button(options_frame, text="Generate Report", bg="#2ecc71", fg="white",
                              font=("Arial", 12), padx=10, pady=5, command=generate_report)
        generate_btn.pack(pady=15)

    def _generate_fitness_report(self):
        """Generate fitness report"""
        report_frame = tk.LabelFrame(self.reports_frame, text="Fitness Report", bg="white", 
                                   padx=15, pady=15, font=("Arial", 12))
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Calculate total workouts
        total_workouts = 0
        total_calories = 0
        exercise_data = {}
        
        for member in self.system.view_members():
            if hasattr(member, 'workouts') and member.workouts:
                total_workouts += len(member.workouts)
                total_calories += sum(w.get('calories', 0) for w in member.workouts)
                
                # Collect exercise type data
                for workout in member.workouts:
                    ex_type = workout.get('exercise_type', 'Unknown')
                    exercise_data[ex_type] = exercise_data.get(ex_type, 0) + 1
        
        tk.Label(report_frame, text=f"Total Workouts Logged: {total_workouts}", 
               bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        tk.Label(report_frame, text=f"Total Calories Burned: {total_calories}", 
               bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        # Most active member
        most_active = None
        max_workouts = 0
        for member in self.system.view_members():
            if hasattr(member, 'workouts') and member.workouts:
                if len(member.workouts) > max_workouts:
                    max_workouts = len(member.workouts)
                    most_active = member
        
        if most_active:
            tk.Label(report_frame, text=f"Most Active Member: {most_active.name} ({max_workouts} workouts)", 
                   bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        # Add chart if matplotlib is available and we have data
        if MATPLOTLIB_AVAILABLE and total_workouts > 0 and exercise_data:
            try:
                # Create a simple chart
                fig = plt.Figure(figsize=(8, 4), dpi=100)
                ax = fig.add_subplot(111)
                
                exercise_types = list(exercise_data.keys())
                exercise_counts = list(exercise_data.values())
                
                bars = ax.bar(exercise_types, exercise_counts)
                ax.set_title('Exercise Type Distribution')
                ax.set_ylabel('Number of Workouts')
                
                # Rotate x-axis labels for better readability
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}', ha='center', va='bottom')
                
                fig.tight_layout()
                
                canvas_chart = FigureCanvasTkAgg(fig, report_frame)
                canvas_chart.draw()
                canvas_chart.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=15)
                
            except Exception as e:
                print(f"Chart generation error: {str(e)}")
                tk.Label(report_frame, text="Chart could not be generated", 
                       bg="white", fg="orange").pack(pady=5)
        elif not MATPLOTLIB_AVAILABLE:
            tk.Label(report_frame, text="Install matplotlib to view charts: pip install matplotlib", 
                   bg="white", fg="gray", font=("Arial", 10)).pack(pady=5)

    def _generate_nutrition_report(self):
        """Generate nutrition report"""
        report_frame = tk.LabelFrame(self.reports_frame, text="Nutrition Report", bg="white", 
                                   padx=15, pady=15, font=("Arial", 12))
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        total_meals = 0
        total_calories = 0
        for member in self.system.view_members():
            if hasattr(member, 'meals') and member.meals:
                total_meals += len(member.meals)
                total_calories += sum(m.get('calories', 0) for m in member.meals)
        
        tk.Label(report_frame, text=f"Total Meals Logged: {total_meals}", 
               bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        tk.Label(report_frame, text=f"Total Calories Consumed: {total_calories}", 
               bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)

    def _generate_revenue_report(self):
        """Generate revenue report"""
        report_frame = tk.LabelFrame(self.reports_frame, text="Revenue Report", bg="white", 
                                   padx=15, pady=15, font=("Arial", 12))
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        report_data = self.system.generate_revenue_report()
        
        tk.Label(report_frame, text=f"Total Revenue: ${report_data['total_revenue']:.2f}", 
               bg="white", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=10)
        
        if report_data['top_class']:
            tk.Label(report_frame, text=f"Top Class: {report_data['top_class'][0]} ({report_data['top_class'][1]} members)", 
                   bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        tk.Label(report_frame, text=f"Active Members: {report_data['active_members']}", 
               bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)

    def _generate_membership_analysis(self):
        """Generate membership analysis"""
        report_frame = tk.LabelFrame(self.reports_frame, text="Membership Analysis", bg="white", 
                                   padx=15, pady=15, font=("Arial", 12))
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Count membership types
        membership_counts = {"Basic": 0, "Premium": 0, "VIP": 0}
        for member in self.system.view_members():
            if member.membership_type in membership_counts:
                membership_counts[member.membership_type] += 1
        
        tk.Label(report_frame, text="Membership Distribution:", 
               bg="white", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=10)
        
        for membership_type, count in membership_counts.items():
            tk.Label(report_frame, text=f"{membership_type}: {count} members", 
                   bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)

    def _calculate_end_date(self, duration, duration_unit, start_date=None):
        """Calculate the end date based on duration and unit"""
        if start_date is None:
            start_date = datetime.now()
            
        if duration_unit == "Days":
            return start_date + timedelta(days=duration)
        elif duration_unit == "Weeks":
            return start_date + timedelta(weeks=duration)
        elif duration_unit == "Months":
            # Approximating months as 30 days
            return start_date + timedelta(days=duration * 30)
        return start_date

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
