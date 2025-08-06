"""
To-Do List Application
A GUI-based task management application using Python and tkinter.
Features: Create, update, delete, mark complete, and organize tasks efficiently.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import sys

# Handle termcolor import with fallback
try:
    from termcolor import colored
    TERMCOLOR_AVAILABLE = True
except ImportError:
    TERMCOLOR_AVAILABLE = False
    print("termcolor module not found. Installing...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "termcolor"])
        from termcolor import colored
        TERMCOLOR_AVAILABLE = True
    except Exception as e:
        print(f"Could not install termcolor: {e}")
        # Fallback function for colored output
        def colored(text, color=None, attrs=None):
            return text

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Data storage
        self.tasks = []
        self.data_file = "todo_data.json"
        
        # Status bar visibility
        self.status_bar_visible = True
        
        # Create GUI components
        self.create_menu()
        self.create_widgets()
        self.create_status_bar()
        
        # Load existing data
        self.load_tasks()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Control-n>', lambda e: self.add_task())
        self.root.bind('<Delete>', lambda e: self.delete_task())
        self.root.bind('<F5>', lambda e: self.refresh_tasks())
        
    def create_menu(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Task", command=self.add_task, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_tasks, accelerator="Ctrl+S")
        file_menu.add_command(label="Load", command=self.load_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Edit Task", command=self.edit_task)
        edit_menu.add_command(label="Delete Task", command=self.delete_task, accelerator="Del")
        edit_menu.add_command(label="Mark Complete", command=self.toggle_complete)
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear Completed", command=self.clear_completed)
        edit_menu.add_command(label="Clear All", command=self.clear_all_tasks)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_tasks, accelerator="F5")
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Status Bar", command=self.toggle_status_bar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="To-Do List Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Task input frame
        input_frame = ttk.LabelFrame(main_frame, text="Add New Task", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Task:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.task_entry = ttk.Entry(input_frame, font=('Arial', 10))
        self.task_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        self.add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=2)
        
        # Priority selection
        ttk.Label(input_frame, text="Priority:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                     values=["High", "Medium", "Low"], state="readonly", width=10)
        priority_combo.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Task list frame
        list_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for tasks
        columns = ('Task', 'Priority', 'Status', 'Created')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.task_tree.heading('Task', text='Task Description')
        self.task_tree.heading('Priority', text='Priority')
        self.task_tree.heading('Status', text='Status')
        self.task_tree.heading('Created', text='Created')
        
        # Define column widths
        self.task_tree.column('Task', width=300)
        self.task_tree.column('Priority', width=80)
        self.task_tree.column('Status', width=80)
        self.task_tree.column('Created', width=120)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid treeview and scrollbar
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click to edit
        self.task_tree.bind('<Double-1>', lambda e: self.edit_task())
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(button_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Mark Complete", command=self.toggle_complete).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Completed", command=self.clear_completed).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Refresh", command=self.refresh_tasks).pack(side=tk.LEFT, padx=(0, 5))
        
    def create_status_bar(self):
        """Create the status bar"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Task count label
        self.task_count_var = tk.StringVar()
        self.task_count_label = ttk.Label(self.status_frame, textvariable=self.task_count_var,
                                         relief=tk.SUNKEN, anchor=tk.E)
        self.task_count_label.pack(side=tk.RIGHT)
        
        self.update_task_count()
        
    def toggle_status_bar(self):
        """Toggle the visibility of the status bar"""
        if self.status_bar_visible:
            self.status_frame.grid_remove()
            self.status_bar_visible = False
        else:
            self.status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
            self.status_bar_visible = True
            
    def show_status_message(self, message, message_type="info"):
        """Show a message in the status bar with optional color coding"""
        self.status_var.set(message)
        if TERMCOLOR_AVAILABLE:
            print(colored(f"Status: {message}", "green" if message_type == "success" else "yellow"))
        
    def add_task(self):
        """Add a new task to the list"""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task description!")
            return
            
        task = {
            'id': len(self.tasks) + 1,
            'text': task_text,
            'priority': self.priority_var.get(),
            'status': 'Pending',
            'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'completed': False
        }
        
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.refresh_tasks()
        self.save_tasks()
        self.show_status_message(f"Task '{task_text}' added successfully!", "success")
        
    def edit_task(self):
        """Edit the selected task"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit!")
            return
            
        item = self.task_tree.item(selected[0])
        task_text = item['values'][0]
        
        # Find the task in our data
        task_index = None
        for i, task in enumerate(self.tasks):
            if task['text'] == task_text:
                task_index = i
                break
                
        if task_index is None:
            messagebox.showerror("Error", "Task not found!")
            return
            
        # Create edit dialog
        new_text = simpledialog.askstring("Edit Task", "Edit task description:", 
                                         initialvalue=task_text)
        if new_text and new_text.strip():
            self.tasks[task_index]['text'] = new_text.strip()
            self.refresh_tasks()
            self.save_tasks()
            self.show_status_message(f"Task updated successfully!", "success")
            
    def delete_task(self):
        """Delete the selected task"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            item = self.task_tree.item(selected[0])
            task_text = item['values'][0]
            
            # Remove from data
            self.tasks = [task for task in self.tasks if task['text'] != task_text]
            self.refresh_tasks()
            self.save_tasks()
            self.show_status_message(f"Task deleted successfully!", "success")
            
    def toggle_complete(self):
        """Toggle the completion status of the selected task"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
            return
            
        item = self.task_tree.item(selected[0])
        task_text = item['values'][0]
        
        # Find and update the task
        for task in self.tasks:
            if task['text'] == task_text:
                task['completed'] = not task['completed']
                task['status'] = 'Completed' if task['completed'] else 'Pending'
                break
                
        self.refresh_tasks()
        self.save_tasks()
        status = "completed" if task['completed'] else "pending"
        self.show_status_message(f"Task marked as {status}!", "success")
        
    def clear_completed(self):
        """Remove all completed tasks"""
        completed_count = len([task for task in self.tasks if task['completed']])
        if completed_count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
            
        if messagebox.askyesno("Confirm Clear", f"Remove {completed_count} completed task(s)?"):
            self.tasks = [task for task in self.tasks if not task['completed']]
            self.refresh_tasks()
            self.save_tasks()
            self.show_status_message(f"Cleared {completed_count} completed task(s)!", "success")
            
    def clear_all_tasks(self):
        """Clear all tasks"""
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to clear!")
            return
            
        if messagebox.askyesno("Confirm Clear All", "Are you sure you want to delete ALL tasks?"):
            self.tasks.clear()
            self.refresh_tasks()
            self.save_tasks()
            self.show_status_message("All tasks cleared!", "success")
            
    def refresh_tasks(self):
        """Refresh the task display"""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        # Add current tasks
        for task in self.tasks:
            tag = 'completed' if task['completed'] else 'pending'
            self.task_tree.insert('', tk.END, values=(
                task['text'],
                task['priority'],
                task['status'],
                task['created']
            ), tags=(tag,))
            
        # Configure tags for visual distinction
        self.task_tree.tag_configure('completed', foreground='gray', font=('Arial', 9, 'italic'))
        self.task_tree.tag_configure('pending', foreground='black', font=('Arial', 9))
        
        self.update_task_count()
        
    def update_task_count(self):
        """Update the task count in the status bar"""
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task['completed']])
        pending = total - completed
        self.task_count_var.set(f"Total: {total} | Pending: {pending} | Completed: {completed}")
        
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save tasks: {str(e)}")
            
    def load_tasks(self):
        """Load tasks from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
                self.refresh_tasks()
                self.show_status_message(f"Loaded {len(self.tasks)} task(s)", "success")
            else:
                self.show_status_message("No saved tasks found", "info")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load tasks: {str(e)}")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """To-Do List Manager v1.0

A comprehensive task management application built with Python and tkinter.

Features:
• Create, edit, and delete tasks
• Set task priorities
• Mark tasks as complete
• Persistent data storage
• Keyboard shortcuts
• Status bar with task statistics

Keyboard Shortcuts:
• Ctrl+N: Add new task
• Delete: Delete selected task
• F5: Refresh task list

Created for efficient task management and organization."""
        
        messagebox.showinfo("About To-Do List Manager", about_text)
        
    def on_closing(self):
        """Handle application closing"""
        self.save_tasks()
        self.root.destroy()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ToDoApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
