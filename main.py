import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import Member, Trainer, FitnessClass, Transaction, FitnessManagementSystem
import uuid
import sys

class SmartFitnessApp:
    def __init__(self, root):
        self.root = root
        self.system = FitnessManagementSystem()
        self.root.title("Smart Fitness Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Create sample data for testing
        self._create_sample_data()
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.sidebar = tk.Frame(self.main_frame, width=200, bg="#2c3e50")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Create content area
        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # App title
        title_label = tk.Label(self.sidebar, text="SFMS", font=("Arial", 24, "bold"), 
                              bg="#2c3e50", fg="white")
        title_label.pack(pady=20)
        
        # Menu buttons
        self._create_menu_button("User Management", self.show_user_management)
        self._create_menu_button("Workout Tracking", self.show_workout_tracking)
        self._create_menu_button("Goal Tracking", self.show_goal_tracking)
        self._create_menu_button("Nutrition Tracking", self.show_nutrition_tracking)
        self._create_menu_button("Reports & Analytics", self.show_reports)
        self._create_menu_button("Switch to Text Mode", self.switch_to_text_mode)
        self._create_menu_button("Exit", self.root.destroy)
        
        # Show user management by default
        self.show_user_management()
        
    def _create_sample_data(self):
        # Create some sample members
        member1 = Member("M001", "John Doe", 30, "Premium", "Weight Loss")
        member2 = Member("M002", "Jane Smith", 25, "Basic", "Muscle Gain")
        self.system.register_member(member1)
        self.system.register_member(member2)
        
        # Add some progress data
        member1.track_progress({"weight": 80, "running_speed": 10})
        member1.track_progress({"weight": 78, "running_speed": 11})
        
        # Create some trainers
        trainer1 = Trainer("T001", "Mike Johnson", "Yoga")
        trainer2 = Trainer("T002", "Sara Brown", "Strength Training")
        self.system.add_trainer(trainer1)
        self.system.add_trainer(trainer2)
        
        # Create some fitness classes
        class1 = FitnessClass("C001", "Morning Yoga", 15, "Monday, 8:00 AM")
        class2 = FitnessClass("C002", "HIIT Training", 10, "Tuesday, 6:00 PM")
        class1.assign_trainer(trainer1)
        class2.assign_trainer(trainer2)
        self.system.schedule_class(class1)
        self.system.schedule_class(class2)
        
        # Create some transactions
        trans1 = Transaction("T001", member1, 50.00, "Premium Membership")
        trans2 = Transaction("T002", member2, 30.00, "Basic Membership")
        self.system.add_transaction(trans1)
        self.system.add_transaction(trans2)
    
    def _create_menu_button(self, text, command):
        btn = tk.Button(self.sidebar, text=text, font=("Arial", 12), 
                      bg="#34495e", fg="white", bd=0, padx=10, pady=10,
                      activebackground="#3498db", activeforeground="white",
                      width=20, command=command)
        btn.pack(pady=5, padx=10)
    
    def _clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_user_management(self):
        self._clear_content_frame()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        page_title = tk.Label(title_frame, text="User Management", font=("Arial", 20, "bold"), bg="#f0f0f0")
        page_title.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        add_btn = tk.Button(button_frame, text="Add New Member", bg="#2ecc71", fg="white",
                          font=("Arial", 12), padx=10, pady=5, command=self.add_new_member)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        update_btn = tk.Button(button_frame, text="Update Selected", bg="#f39c12", fg="white",
                             font=("Arial", 12), padx=10, pady=5, command=self.update_member)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(button_frame, text="Delete Selected", bg="#e74c3c", fg="white",
                             font=("Arial", 12), padx=10, pady=5, command=self.delete_member)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Members table
        table_frame = tk.Frame(self.content_frame, bg="white", padx=10, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview for members
        columns = ('ID', 'Name', 'Age', 'Membership Type', 'Fitness Goals')
        self.members_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.members_table.heading(col, text=col)
            self.members_table.column(col, width=120)
        
        # Adding scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.members_table.yview)
        self.members_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.members_table.pack(fill=tk.BOTH, expand=True)
        
        # Load members into table
        self.load_members_table()
    
    def load_members_table(self):
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
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Member")
        add_window.geometry("400x350")
        add_window.configure(bg="#f0f0f0")
        
        # Form
        tk.Label(add_window, text="Add New Member", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        form_frame = tk.Frame(add_window, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Member ID
        tk.Label(form_frame, text="Member ID:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, pady=5)
        member_id_var = tk.StringVar(value=f"M{str(uuid.uuid4().int)[:3]}")
        member_id_entry = tk.Entry(form_frame, textvariable=member_id_var)
        member_id_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Name
        tk.Label(form_frame, text="Name:", bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        name_entry = tk.Entry(form_frame, textvariable=name_var)
        name_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Age
        tk.Label(form_frame, text="Age:", bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=5)
        age_var = tk.IntVar()
        age_entry = tk.Entry(form_frame, textvariable=age_var)
        age_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Membership Type
        tk.Label(form_frame, text="Membership Type:", bg="#f0f0f0").grid(row=3, column=0, sticky=tk.W, pady=5)
        membership_var = tk.StringVar()
        membership_combo = ttk.Combobox(form_frame, textvariable=membership_var, 
                                       values=["Basic", "Premium", "VIP"])
        membership_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Fitness Goals
        tk.Label(form_frame, text="Fitness Goals:", bg="#f0f0f0").grid(row=4, column=0, sticky=tk.W, pady=5)
        goals_var = tk.StringVar()
        goals_combo = ttk.Combobox(form_frame, textvariable=goals_var, 
                                 values=["Weight Loss", "Muscle Gain", "Endurance"])
        goals_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Submit button
        def save_member():
            try:
                new_member = Member(
                    member_id_var.get(),
                    name_var.get(),
                    int(age_var.get()),
                    membership_var.get(),
                    goals_var.get()
                )
                self.system.register_member(new_member)
                self.load_members_table()
                messagebox.showinfo("Success", "Member added successfully!")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add member: {str(e)}")
        
        submit_btn = tk.Button(add_window, text="Save Member", bg="#2ecc71", fg="white",
                             font=("Arial", 12), padx=10, pady=5, command=save_member)
        submit_btn.pack(pady=20)
    
    def update_member(self):
        # Get selected member
        selected = self.members_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a member to update.")
            return
            
        # Get member data
        member_id = self.members_table.item(selected[0])['values'][0]
        member = self.system.find_member_by_id(member_id)
        if not member:
            messagebox.showerror("Error", "Member not found.")
            return
            
        # Create update window
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Member")
        update_window.geometry("400x350")
        update_window.configure(bg="#f0f0f0")
        
        tk.Label(update_window, text="Update Member", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        form_frame = tk.Frame(update_window, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Name
        tk.Label(form_frame, text="Name:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=member.name)
        name_entry = tk.Entry(form_frame, textvariable=name_var)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Age
        tk.Label(form_frame, text="Age:", bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=5)
        age_var = tk.IntVar(value=member.age)
        age_entry = tk.Entry(form_frame, textvariable=age_var)
        age_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Membership Type
        tk.Label(form_frame, text="Membership Type:", bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=5)
        membership_var = tk.StringVar(value=member.membership_type)
        membership_combo = ttk.Combobox(form_frame, textvariable=membership_var, 
                                       values=["Basic", "Premium", "VIP"])
        membership_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Fitness Goals
        tk.Label(form_frame, text="Fitness Goals:", bg="#f0f0f0").grid(row=3, column=0, sticky=tk.W, pady=5)
        goals_var = tk.StringVar(value=member.fitness_goals)
        goals_combo = ttk.Combobox(form_frame, textvariable=goals_var, 
                                 values=["Weight Loss", "Muscle Gain", "Endurance"])
        goals_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Submit button
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
        
        submit_btn = tk.Button(update_window, text="Save Changes", bg="#f39c12", fg="white",
                             font=("Arial", 12), padx=10, pady=5, command=save_updates)
        submit_btn.pack(pady=20)
    
    def delete_member(self):
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
        self._clear_content_frame()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        page_title = tk.Label(title_frame, text="Workout Tracking", font=("Arial", 20, "bold"), bg="#f0f0f0")
        page_title.pack(side=tk.LEFT)
        
        # Workout form
        form_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Member selection
        tk.Label(form_frame, text="Select Member:", bg="white").grid(row=0, column=0, sticky=tk.W, pady=10)
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(form_frame, textvariable=member_var, width=30)
        member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.grid(row=0, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Exercise type
        tk.Label(form_frame, text="Exercise Type:", bg="white").grid(row=1, column=0, sticky=tk.W, pady=10)
        exercise_var = tk.StringVar()
        exercise_combo = ttk.Combobox(form_frame, textvariable=exercise_var, width=30, 
                                    values=["Running", "Weight Lifting", "Yoga", "Swimming", "Cycling"])
        exercise_combo.grid(row=1, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Duration
        tk.Label(form_frame, text="Duration (minutes):", bg="white").grid(row=2, column=0, sticky=tk.W, pady=10)
        duration_var = tk.IntVar()
        duration_entry = tk.Entry(form_frame, textvariable=duration_var, width=32)
        duration_entry.grid(row=2, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Calories
        tk.Label(form_frame, text="Calories Burned:", bg="white").grid(row=3, column=0, sticky=tk.W, pady=10)
        calories_var = tk.IntVar()
        calories_entry = tk.Entry(form_frame, textvariable=calories_var, width=32)
        calories_entry.grid(row=3, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Notes
        tk.Label(form_frame, text="Notes:", bg="white").grid(row=4, column=0, sticky=tk.W, pady=10)
        notes_var = tk.StringVar()
        notes_entry = tk.Entry(form_frame, textvariable=notes_var, width=32)
        notes_entry.grid(row=4, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Save button
        def log_workout():
            if not member_var.get() or not exercise_var.get():
                messagebox.showwarning("Missing Information", "Please select a member and exercise type.")
                return
                
            try:
                # Extract member_id from the combo box value (format: "ID - Name")
                member_id = member_var.get().split(" - ")[0]
                member = self.system.find_member_by_id(member_id)
                
                if member:
                    workout_data = {
                        "exercise_type": exercise_var.get(),
                        "duration": duration_var.get(),
                        "calories": calories_var.get(),
                        "notes": notes_var.get()
                    }
                    member.track_progress(workout_data)
                    messagebox.showinfo("Success", "Workout logged successfully!")
                    
                    # Clear form fields
                    exercise_var.set("")
                    duration_var.set(0)
                    calories_var.set(0)
                    notes_var.set("")
                else:
                    messagebox.showerror("Error", "Member not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to log workout: {str(e)}")
                
        save_btn = tk.Button(form_frame, text="Log Workout", bg="#3498db", fg="white",
                          font=("Arial", 12), padx=10, pady=5, command=log_workout)
        save_btn.grid(row=5, column=1, sticky=tk.E, pady=20)

    def show_goal_tracking(self):
        self._clear_content_frame()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        page_title = tk.Label(title_frame, text="Goal Tracking & Progress", font=("Arial", 20, "bold"), bg="#f0f0f0")
        page_title.pack(side=tk.LEFT)
        
        # Content area with two columns
        content_area = tk.Frame(self.content_frame, bg="#f0f0f0")
        content_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left column - Goal setting
        left_column = tk.LabelFrame(content_area, text="Set Fitness Goals", bg="white", padx=15, pady=15, font=("Arial", 12))
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Member selection
        tk.Label(left_column, text="Select Member:", bg="white").pack(anchor=tk.W, pady=5)
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(left_column, textvariable=member_var, width=30)
        member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.pack(anchor=tk.W, pady=5)
        
        # Goal type
        tk.Label(left_column, text="Goal Type:", bg="white").pack(anchor=tk.W, pady=5)
        goal_type_var = tk.StringVar()
        goal_types = ["Weight Loss", "Muscle Gain", "Running Distance", "Calories to Burn"]
        goal_type_combo = ttk.Combobox(left_column, textvariable=goal_type_var, width=30, values=goal_types)
        goal_type_combo.pack(anchor=tk.W, pady=5)
        
        # Target value
        tk.Label(left_column, text="Target Value:", bg="white").pack(anchor=tk.W, pady=5)
        target_var = tk.StringVar()
        target_entry = tk.Entry(left_column, textvariable=target_var, width=32)
        target_entry.pack(anchor=tk.W, pady=5)
        
        # Duration
        tk.Label(left_column, text="Duration (weeks):", bg="white").pack(anchor=tk.W, pady=5)
        duration_var = tk.IntVar(value=4)
        duration_entry = tk.Entry(left_column, textvariable=duration_var, width=32)
        duration_entry.pack(anchor=tk.W, pady=5)
        
        # Save button
        def save_goal():
            if not member_var.get() or not goal_type_var.get() or not target_var.get():
                messagebox.showwarning("Missing Information", "Please fill in all required fields.")
                return
                
            try:
                # In a real app, you would save this to a database or member's goals
                messagebox.showinfo("Success", "Goal saved successfully!")
                
                # Clear form fields
                goal_type_var.set("")
                target_var.set("")
                duration_var.set(4)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save goal: {str(e)}")
        
        save_btn = tk.Button(left_column, text="Set Goal", bg="#3498db", fg="white",
                          font=("Arial", 12), padx=10, pady=5, command=save_goal)
        save_btn.pack(anchor=tk.E, pady=10)
        
        # Right column - Progress visualization
        right_column = tk.LabelFrame(content_area, text="Progress Visualization", bg="white", padx=15, pady=15, font=("Arial", 12))
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sample progress chart
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Sample data - would be replaced with actual member data in a real app
        dates = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        weights = [85, 83, 82, 80]
        
        ax.plot(dates, weights, marker='o')
        ax.set_title('Weight Loss Progress (kg)')
        ax.set_ylim(70, 90)
        ax.grid(True)
        
        canvas = FigureCanvasTkAgg(fig, right_column)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_nutrition_tracking(self):
        self._clear_content_frame()
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        page_title = tk.Label(title_frame, text="Nutrition & Diet Tracking", font=("Arial", 20, "bold"), bg="#f0f0f0")
        page_title.pack(side=tk.LEFT)
        
        # Form for logging meals
        form_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Member selection
        tk.Label(form_frame, text="Select Member:", bg="white").grid(row=0, column=0, sticky=tk.W, pady=10)
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(form_frame, textvariable=member_var, width=30)
        member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
        member_combo.grid(row=0, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Meal Type
        tk.Label(form_frame, text="Meal Type:", bg="white").grid(row=1, column=0, sticky=tk.W, pady=10)
        meal_type_var = tk.StringVar()
        meal_type_combo = ttk.Combobox(form_frame, textvariable=meal_type_var, width=30, 
                                      values=["Breakfast", "Lunch", "Dinner", "Snack"])
        meal_type_combo.grid(row=1, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Food Items
        tk.Label(form_frame, text="Food Items:", bg="white").grid(row=2, column=0, sticky=tk.W, pady=10)
        food_var = tk.StringVar()
        food_entry = tk.Entry(form_frame, textvariable=food_var, width=32)
        food_entry.grid(row=2, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Calories
        tk.Label(form_frame, text="Total Calories:", bg="white").grid(row=3, column=0, sticky=tk.W, pady=10)
        calories_var = tk.IntVar()
        calories_entry = tk.Entry(form_frame, textvariable=calories_var, width=32)
        calories_entry.grid(row=3, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Protein
        tk.Label(form_frame, text="Protein (g):", bg="white").grid(row=4, column=0, sticky=tk.W, pady=10)
        protein_var = tk.IntVar()
        protein_entry = tk.Entry(form_frame, textvariable=protein_var, width=32)
        protein_entry.grid(row=4, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Carbs
        tk.Label(form_frame, text="Carbohydrates (g):", bg="white").grid(row=5, column=0, sticky=tk.W, pady=10)
        carbs_var = tk.IntVar()
        carbs_entry = tk.Entry(form_frame, textvariable=carbs_var, width=32)
        carbs_entry.grid(row=5, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Fat
        tk.Label(form_frame, text="Fat (g):", bg="white").grid(row=6, column=0, sticky=tk.W, pady=10)
        fat_var = tk.IntVar()
        fat_entry = tk.Entry(form_frame, textvariable=fat_var, width=32)
        fat_entry.grid(row=6, column=1, sticky=tk.W, pady=10, padx=5)
        
        # Save button
        def log_meal():
            if not member_var.get() or not meal_type_var.get() or not food_var.get():
                messagebox.showwarning("Missing Information", "Please fill in all required fields.")
                return
                
            try:
                # Extract member_id from the combo box value (format: "ID - Name")
                member_id = member_var.get().split(" - ")[0]
                member = self.system.find_member_by_id(member_id)
                
                if member:
                    # In a real app, you would save this to a database
                    meal_data = {
                        "meal_type": meal_type_var.get(),
                        "food_items": food_var.get(),
                        "calories": calories_var.get(),
                        "protein": protein_var.get(),
                        "carbs": carbs_var.get(),
                        "fat": fat_var.get(),
                        "type": "nutrition"
                    }
                    member.track_progress(meal_data)
                    messagebox.showinfo("Success", "Meal logged successfully!")
                    
                    # Clear form fields
                    meal_type_var.set("")
                    food_var.set("")
                    calories_var.set(0)
                    protein_var.set(0)
                    carbs_var.set(0)
                    fat_var.set(0)
                else:
                    messagebox.showerror("Error", "Member not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to log meal: {str(e)}")
                
        save_btn = tk.Button(form_frame, text="Log Meal", bg="#3498db", fg="white",
                          font=("Arial", 12), padx=10, pady=5, command=log_meal)
        save_btn.grid(row=7, column=1, sticky=tk.E, pady=20)
        
        # Nutrition advice section
        advice_frame = tk.LabelFrame(self.content_frame, text="Nutrition Tips", bg="white", padx=15, pady=15, font=("Arial", 12))
        advice_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tips = [
            "Stay hydrated! Aim for at least 8 glasses of water daily.",
            "Include protein in every meal to support muscle recovery.",
            "Eat a variety of colorful vegetables to ensure you get different nutrients.",
            "Limit processed foods and focus on whole, natural foods.",
            "Don't skip meals, especially breakfast!"
        ]
        
        for tip in tips:
            tip_label = tk.Label(advice_frame, text="• " + tip, bg="white", anchor="w", justify=tk.LEFT, wraplength=800)
            tip_label.pack(anchor=tk.W, pady=5)
    
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
        
        # Generate button
        def generate_report():
            report_type = report_var.get()
            report_content_frame = tk.LabelFrame(self.content_frame, text=f"{report_type}", bg="white", 
                                              padx=15, pady=15, font=("Arial", 12))
            report_content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            if report_type == "Revenue Report":
                # Get revenue report data
                report_data = self.system.generate_revenue_report()
                
                # Display report content
                tk.Label(report_content_frame, text=f"Total Revenue: ${report_data['total_revenue']:.2f}", 
                       bg="white", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=10)
                
                if report_data['top_class']:
                    tk.Label(report_content_frame, text=f"Top Class: {report_data['top_class'][0]} ({report_data['top_class'][1]} members)", 
                           bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
                
                tk.Label(report_content_frame, text=f"Active Members: {report_data['active_members']}", 
                       bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
                
                # Create a simple bar chart
                fig = plt.Figure(figsize=(8, 4), dpi=100)
                ax = fig.add_subplot(111)
                
                # Sample class data - would be replaced with actual data
                classes = ["Yoga", "HIIT", "Strength", "Cardio", "Pilates"]
                enrollments = [12, 20, 15, 10, 8]
                
                ax.bar(classes, enrollments)
                ax.set_title('Class Enrollments')
                ax.set_ylabel('Number of Members')
                ax.grid(True, axis='y', linestyle='--', alpha=0.7)
                
                canvas = FigureCanvasTkAgg(fig, report_content_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=15)
            
            elif report_type == "Fitness Report" or report_type == "Nutrition Report":
                # Member selection for individual reports
                member_frame = tk.Frame(report_content_frame, bg="white")
                member_frame.pack(fill=tk.X, pady=10)
                
                tk.Label(member_frame, text="Select Member:", bg="white").pack(side=tk.LEFT, padx=5)
                member_var = tk.StringVar()
                member_combo = ttk.Combobox(member_frame, textvariable=member_var, width=30)
                member_combo['values'] = [f"{m.member_id} - {m.name}" for m in self.system.view_members()]
                member_combo.pack(side=tk.LEFT, padx=5)
                
                def show_member_report():
                    if not member_var.get():
                        messagebox.showwarning("No Selection", "Please select a member first.")
                        return
                        
                    member_id = member_var.get().split(" - ")[0]
                    member = self.system.find_member_by_id(member_id)
                    
                    if not member:
                        messagebox.showerror("Error", "Member not found.")
                        return
                        
                    # Clear any previous report
                    for widget in report_details_frame.winfo_children():
                        widget.destroy()
                        
                    # Display member info
                    tk.Label(report_details_frame, text=f"Member: {member.name}", 
                           bg="white", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=5)
                    tk.Label(report_details_frame, text=f"Membership Type: {member.membership_type}", 
                           bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=3)
                    tk.Label(report_details_frame, text=f"Fitness Goals: {member.fitness_goals}", 
                           bg="white", font=("Arial", 12)).pack(anchor=tk.W, pady=3)
                    
                    # Filter progress data based on report type
                    progress_data = member.get_progress()
                    
                    if report_type == "Fitness Report":
                        # Just a placeholder chart - in a real app, you would use actual fitness data
                        fig = plt.Figure(figsize=(8, 4), dpi=100)
                        ax = fig.add_subplot(111)
                        
                        # Sample workout data - would be replaced with actual data
                        dates = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
                        workouts = [3, 5, 4, 6]
                        
                        ax.plot(dates, workouts, 'o-', color='#3498db')
                        ax.set_title('Workout Frequency')
                        ax.set_ylabel('Number of Workouts')
                        ax.grid(True, linestyle='--', alpha=0.7)
                        
                        canvas = FigureCanvasTkAgg(fig, report_details_frame)
                        canvas.draw()
                        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=15)
                    
                    elif report_type == "Nutrition Report":
                        # Just a placeholder chart - in a real app, you would use actual nutrition data
                        fig = plt.Figure(figsize=(8, 4), dpi=100)
                        ax = fig.add_subplot(111)
                        
                        # Sample macros data - would be replaced with actual data
                        categories = ['Protein', 'Carbs', 'Fat']
                        values = [25, 50, 25]  # Percentage distribution
                        
                        ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, 
                             colors=['#3498db', '#2ecc71', '#e74c3c'])
                        ax.set_title('Macronutrient Distribution')
                        
                        canvas = FigureCanvasTkAgg(fig, report_details_frame)
                        canvas.draw()
                        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=15)
                
                view_btn = tk.Button(member_frame, text="View Report", bg="#3498db", fg="white",
                                 command=show_member_report)
                view_btn.pack(side=tk.LEFT, padx=10)
                
                # Frame to hold the report details
                report_details_frame = tk.Frame(report_content_frame, bg="white")
                report_details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
                
            else:  # Membership Analysis
                # Display overall membership statistics
                tk.Label(report_content_frame, text="Membership Distribution", 
                       bg="white", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=10)
                
                # Count membership types
                membership_counts = {"Basic": 0, "Premium": 0, "VIP": 0}
                for member in self.system.view_members():
                    if member.membership_type in membership_counts:
                        membership_counts[member.membership_type] += 1
                
                # Create pie chart for membership distribution
                fig = plt.Figure(figsize=(6, 5), dpi=100)
                ax = fig.add_subplot(111)
                
                labels = list(membership_counts.keys())
                sizes = list(membership_counts.values())
                
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                     colors=['#3498db', '#e67e22', '#9b59b6'])
                ax.set_title('Membership Type Distribution')
                
                canvas = FigureCanvasTkAgg(fig, report_content_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=15)
                
                # Show some mock statistics
                stats_frame = tk.Frame(report_content_frame, bg="white")
                stats_frame.pack(fill=tk.X, pady=10)
                
                tk.Label(stats_frame, text="Membership Statistics:", 
                       bg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
                
                tk.Label(stats_frame, text="Average Member Age:", bg="white").grid(row=1, column=0, sticky=tk.W, pady=3)
                tk.Label(stats_frame, text="32 years", bg="white").grid(row=1, column=1, sticky=tk.W, pady=3)
                
                tk.Label(stats_frame, text="Most Popular Fitness Goal:", bg="white").grid(row=2, column=0, sticky=tk.W, pady=3)
                tk.Label(stats_frame, text="Weight Loss", bg="white").grid(row=2, column=1, sticky=tk.W, pady=3)
                
                tk.Label(stats_frame, text="Average Membership Duration:", bg="white").grid(row=3, column=0, sticky=tk.W, pady=3)
                tk.Label(stats_frame, text="8.5 months", bg="white").grid(row=3, column=1, sticky=tk.W, pady=3)
        
        generate_btn = tk.Button(options_frame, text="Generate Report", bg="#2ecc71", fg="white",
                              font=("Arial", 12), padx=10, pady=5, command=generate_report)
        generate_btn.pack(pady=15)
    
    def switch_to_text_mode(self):
        confirm = messagebox.askyesno("Switch Interface", 
                                    "Are you sure you want to switch to text-based interface?")
        if confirm:
            self.root.withdraw()  # Hide the GUI window
            self.run_text_interface()
    
    def run_text_interface(self):
        print("\nWelcome to Smart Fitness Management System (Text Mode)")
        
        while True:
            print("\nMain Menu:")
            print("1. Register New Member")
            print("2. View All Members")
            print("3. Book a Fitness Class")
            print("4. Process Payment")
            print("5. Generate Revenue Report")
            print("6. View Member Progress")
            print("7. Switch to GUI Mode")
            print("8. Exit")
            
            choice = input("\nEnter your choice (1-8): ")
            
            if choice == '1':
                self.text_register_member()
            elif choice == '2':
                self.text_view_members()
            elif choice == '3':
                self.text_book_class()
            elif choice == '4':
                self.text_process_payment()
            elif choice == '5':
                self.text_generate_revenue_report()
            elif choice == '6':
                self.text_view_member_progress()
            elif choice == '7':
                print("Switching to GUI mode...")
                self.root.deiconify()  # Show the GUI window again
                break
            elif choice == '8':
                print("Thank you for using SFMS. Goodbye!")
                self.root.destroy()
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
    
    def text_register_member(self):
        print("\n--- Register New Member ---")
        member_id = input("Enter Member ID: ")
        name = input("Enter Name: ")
        
        try:
            age = int(input("Enter Age: "))
        except ValueError:
            print("Invalid age. Using default value of 30.")
            age = 30
            
        print("Membership Types: Basic, Premium, VIP")
        membership_type = input("Enter Membership Type: ")
        
        print("Fitness Goals: Weight Loss, Muscle Gain, Endurance")
        fitness_goals = input("Enter Fitness Goals: ")
        
        member = Member(member_id, name, age, membership_type, fitness_goals)
        if self.system.register_member(member):
            print(f"Member {name} registered successfully!")
        else:
            print("Failed to register member. Member ID may already exist.")
    
    def text_view_members(self):
        print("\n--- All Members ---")
        members = self.system.view_members()
        
        if not members:
            print("No members found.")
            return
            
        for member in members:
            print(f"ID: {member.member_id}, Name: {member.name}, Age: {member.age}, " +
                 f"Membership: {member.membership_type}, Goals: {member.fitness_goals}")
    
    def text_book_class(self):
        print("\n--- Book a Fitness Class ---")
        member_id = input("Enter Member ID: ")
        member = self.system.find_member_by_id(member_id)
        
        if not member:
            print("Member not found.")
            return
            
        print("\nAvailable Classes:")
        for i, cls in enumerate(self.system.fitness_classes):
            print(f"{i+1}. {cls.name} - {cls.schedule} - {cls.current_enrollments}/{cls.capacity} enrolled")
        
        try:
            class_idx = int(input("\nEnter class number to book: ")) - 1
            if 0 <= class_idx < len(self.system.fitness_classes):
                class_obj = self.system.fitness_classes[class_idx]
                
                if member.book_class(class_obj) and class_obj.enroll_member(member):
                    print(f"Successfully booked {class_obj.name} for {member.name}!")
                else:
                    print("Failed to book class. Class may be full or already booked.")
            else:
                print("Invalid class number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def text_process_payment(self):
        print("\n--- Process Payment ---")
        member_id = input("Enter Member ID: ")
        member = self.system.find_member_by_id(member_id)
        
        if not member:
            print("Member not found.")
            return
            
        try:
            amount = float(input("Enter payment amount: $"))
            service = input("Enter service description: ")
            
            transaction_id = f"T{str(uuid.uuid4().int)[:4]}"
            transaction = Transaction(transaction_id, member, amount, service)
            
            if self.system.add_transaction(transaction):
                print("Payment processed successfully!")
                print(transaction.generate_receipt())
            else:
                print("Failed to process payment.")
        except ValueError:
            print("Invalid amount. Payment cancelled.")
    
    def text_generate_revenue_report(self):
        print("\n--- Revenue Report ---")
        report = self.system.generate_revenue_report()
        
        print(f"Total Revenue: ${report['total_revenue']:.2f}")
        if report['top_class']:
            print(f"Top Class: {report['top_class'][0]} ({report['top_class'][1]} members)")
        print(f"Active Members: {report['active_members']}")
    
    def text_view_member_progress(self):
        print("\n--- View Member Progress ---")
        member_id = input("Enter Member ID: ")
        
        progress_data = self.system.view_member_progress(member_id)
        
        if not progress_data:
            print("No progress data found for this member or member does not exist.")
            return
            
        print(f"Progress Data for Member {member_id}:")
        for i, data in enumerate(progress_data):
            print(f"\nEntry {i+1} - {data['date']}:")
            for key, value in data.items():
                if key != 'date':
                    print(f"  {key}: {value}")


def main():
    root = tk.Tk()
    app = SmartFitnessApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
