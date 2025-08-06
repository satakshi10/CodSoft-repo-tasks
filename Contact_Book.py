import json
import csv
import re
import os
from datetime import datetime
import shutil

class ContactManager:
    """An advanced contact management system with data persistence and enhanced features"""
    
    def __init__(self):
        self.contacts = []
        self.data_file = "contacts.json"
        self.backup_dir = "backups"
        self.contacts_per_page = 10
        self.load_contacts()
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Create backup directory if it doesn't exist"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def validate_email(self, email):
        """Validate email format"""
        if not email:
            return True  # Email is optional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Validate and format phone number"""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        # Check if it's a valid length (10 digits for domestic, 10-15 for international)
        if len(digits) < 10 or len(digits) > 15:
            return None, "Phone number must be 10-15 digits long"
        
        # Format phone number
        if len(digits) == 10:
            # Format as (XXX) XXX-XXXX
            formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        else:
            # For international numbers, just add dashes
            formatted = f"+{digits[:len(digits)-10]}-{digits[-10:-7]}-{digits[-7:-4]}-{digits[-4:]}"
        
        return formatted, None
    
    def load_contacts(self):
        """Load contacts from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    self.contacts = json.load(file)
                print(f"✓ Loaded {len(self.contacts)} contacts from {self.data_file}")
        except Exception as e:
            print(f"Warning: Could not load contacts - {e}")
            self.contacts = []
    
    def save_contacts(self):
        """Save contacts to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.contacts, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving contacts: {e}")
            return False
    
    def create_backup(self):
        """Create a backup of current contacts"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"contacts_backup_{timestamp}.json")
            shutil.copy2(self.data_file, backup_file)
            print(f"✓ Backup created: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None

    def add_contact(self):
        """Add a new contact with enhanced validation"""
        print("\n" + "="*50)
        print("           ADD NEW CONTACT")
        print("="*50)
        
        try:
            # Get name
            name = input("Enter contact name: ").strip()
            if not name:
                print("Error: Name cannot be empty!")
                return
            
            # Get and validate phone
            phone_input = input("Enter phone number: ").strip()
            if not phone_input:
                print("Error: Phone number cannot be empty!")
                return
            
            formatted_phone, phone_error = self.validate_phone(phone_input)
            if phone_error:
                print(f"Error: {phone_error}")
                return
            
            # Get and validate email
            email = input("Enter email address (optional): ").strip()
            if email and not self.validate_email(email):
                print("Error: Invalid email format!")
                return
            
            # Get address and category
            address = input("Enter address (optional): ").strip()
            category = input("Enter category (Family/Friends/Work/Other): ").strip() or "Other"
            
            # Check if contact already exists
            for contact in self.contacts:
                if contact['name'].lower() == name.lower():
                    print("Error: Contact with this name already exists!")
                    return
                if contact['phone'] == formatted_phone:
                    print("Error: Contact with this phone number already exists!")
                    return
            
            # Create new contact
            new_contact = {
                'name': name,
                'phone': formatted_phone,
                'email': email,
                'address': address,
                'category': category,
                'created_date': datetime.now().isoformat()
            }
            
            self.contacts.append(new_contact)
            if self.save_contacts():
                print(f"\n✓ Contact '{name}' added successfully!")
            else:
                print("Warning: Contact added but could not be saved to file!")
            
        except Exception as e:
            print(f"Error adding contact: {e}")
    
    def view_contacts(self, contacts_list=None, show_pagination=True):
        """Display contacts with pagination and sorting options"""
        contacts_to_show = contacts_list if contacts_list is not None else self.contacts
        
        print("\n" + "="*80)
        print("                           CONTACT LIST")
        print("="*80)
        
        if not contacts_to_show:
            print("No contacts found.")
            return
        
        # Show sorting options
        if show_pagination and len(contacts_to_show) > 1:
            print("Sort by: [1] Name [2] Phone [3] Email [4] Category [5] Date Added")
            sort_choice = input("Enter sort option (or press Enter to skip): ").strip()
            
            if sort_choice == '1':
                contacts_to_show = sorted(contacts_to_show, key=lambda x: x['name'].lower())
            elif sort_choice == '2':
                contacts_to_show = sorted(contacts_to_show, key=lambda x: x['phone'])
            elif sort_choice == '3':
                contacts_to_show = sorted(contacts_to_show, key=lambda x: x.get('email', '').lower())
            elif sort_choice == '4':
                contacts_to_show = sorted(contacts_to_show, key=lambda x: x.get('category', 'Other'))
            elif sort_choice == '5':
                contacts_to_show = sorted(contacts_to_show, key=lambda x: x.get('created_date', ''), reverse=True)
        
        # Pagination
        total_contacts = len(contacts_to_show)
        if show_pagination and total_contacts > self.contacts_per_page:
            total_pages = (total_contacts + self.contacts_per_page - 1) // self.contacts_per_page
            current_page = 1
            
            while True:
                start_idx = (current_page - 1) * self.contacts_per_page
                end_idx = min(start_idx + self.contacts_per_page, total_contacts)
                
                print(f"\nPage {current_page} of {total_pages} (Contacts {start_idx + 1}-{end_idx} of {total_contacts})")
                print("-" * 80)
                print(f"{'No.':<3} {'Name':<20} {'Phone':<17} {'Email':<25} {'Category':<12}")
                print("-" * 80)
                
                for i in range(start_idx, end_idx):
                    contact = contacts_to_show[i]
                    email_display = contact.get('email', '')[:24] if contact.get('email') else ''
                    category_display = contact.get('category', 'Other')[:11]
                    print(f"{i+1:<3} {contact['name'][:19]:<20} {contact['phone']:<17} {email_display:<25} {category_display:<12}")
                
                if total_pages > 1:
                    print(f"\n[N]ext page, [P]revious page, [Q]uit viewing")
                    choice = input("Enter choice: ").lower().strip()
                    if choice == 'n' and current_page < total_pages:
                        current_page += 1
                    elif choice == 'p' and current_page > 1:
                        current_page -= 1
                    elif choice == 'q':
                        break
                else:
                    break
        else:
            # Show all contacts without pagination
            print(f"{'No.':<3} {'Name':<20} {'Phone':<17} {'Email':<25} {'Category':<12}")
            print("-" * 80)
            
            for i, contact in enumerate(contacts_to_show, 1):
                email_display = contact.get('email', '')[:24] if contact.get('email') else ''
                category_display = contact.get('category', 'Other')[:11]
                print(f"{i:<3} {contact['name'][:19]:<20} {contact['phone']:<17} {email_display:<25} {category_display:<12}")
    
    def search_contact(self):
        """Enhanced search for contacts by name, phone, email, or address"""
        print("\n" + "="*50)
        print("           SEARCH CONTACT")
        print("="*50)
        
        if not self.contacts:
            print("No contacts found. Please add some contacts first.")
            return
        
        print("Search by:")
        print("1. Name")
        print("2. Phone number")
        print("3. Email")
        print("4. Address")
        print("5. Category")
        print("6. All fields")
        
        search_type = input("\nEnter search type (1-6): ").strip()
        search_term = input("Enter search term: ").strip().lower()
        
        if not search_term:
            print("Error: Search term cannot be empty!")
            return
        
        found_contacts = []
        
        for contact in self.contacts:
            match = False
            
            if search_type == '1':  # Name
                match = search_term in contact['name'].lower()
            elif search_type == '2':  # Phone
                match = search_term in contact['phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            elif search_type == '3':  # Email
                match = search_term in contact.get('email', '').lower()
            elif search_type == '4':  # Address
                match = search_term in contact.get('address', '').lower()
            elif search_type == '5':  # Category
                match = search_term in contact.get('category', '').lower()
            elif search_type == '6':  # All fields
                match = (search_term in contact['name'].lower() or 
                        search_term in contact['phone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '') or
                        search_term in contact.get('email', '').lower() or
                        search_term in contact.get('address', '').lower() or
                        search_term in contact.get('category', '').lower())
            
            if match:
                found_contacts.append(contact)
        
        if found_contacts:
            print(f"\nFound {len(found_contacts)} contact(s):")
            print("-" * 60)
            for contact in found_contacts:
                self.display_contact_details(contact)
        else:
            print("No contacts found matching your search.")
    
    def display_contact_details(self, contact):
        """Display detailed contact information"""
        print(f"Name: {contact['name']}")
        print(f"Phone: {contact['phone']}")
        print(f"Email: {contact.get('email', 'Not provided')}")
        print(f"Address: {contact.get('address', 'Not provided')}")
        print(f"Category: {contact.get('category', 'Other')}")
        if 'created_date' in contact:
            created = datetime.fromisoformat(contact['created_date']).strftime("%Y-%m-%d %H:%M")
            print(f"Added: {created}")
        print("-" * 40)
    
    def update_contact(self):
        """Update an existing contact with enhanced validation"""
        print("\n" + "="*50)
        print("           UPDATE CONTACT")
        print("="*50)
        
        if not self.contacts:
            print("No contacts found. Please add some contacts first.")
            return
        
        self.view_contacts(show_pagination=False)
        
        try:
            choice = int(input("\nEnter contact number to update: "))
            if 1 <= choice <= len(self.contacts):
                contact = self.contacts[choice - 1]
                
                print(f"\nUpdating contact: {contact['name']}")
                print("Press Enter to keep current value:")
                
                # Update name
                new_name = input(f"Name ({contact['name']}): ").strip()
                if new_name:
                    contact['name'] = new_name
                
                # Update phone with validation
                new_phone = input(f"Phone ({contact['phone']}): ").strip()
                if new_phone:
                    formatted_phone, phone_error = self.validate_phone(new_phone)
                    if phone_error:
                        print(f"Error: {phone_error}")
                        return
                    contact['phone'] = formatted_phone
                
                # Update email with validation
                current_email = contact.get('email', '')
                new_email = input(f"Email ({current_email}): ").strip()
                if new_email != '' and new_email != current_email:
                    if not self.validate_email(new_email):
                        print("Error: Invalid email format!")
                        return
                    contact['email'] = new_email
                
                # Update address
                current_address = contact.get('address', '')
                new_address = input(f"Address ({current_address}): ").strip()
                if new_address != '':
                    contact['address'] = new_address
                
                # Update category
                current_category = contact.get('category', 'Other')
                new_category = input(f"Category ({current_category}): ").strip()
                if new_category:
                    contact['category'] = new_category
                
                if self.save_contacts():
                    print(f"\n✓ Contact '{contact['name']}' updated successfully!")
                else:
                    print("Warning: Contact updated but could not be saved to file!")
                
            else:
                print("Error: Invalid contact number!")
                
        except ValueError:
            print("Error: Please enter a valid number!")
        except Exception as e:
            print(f"Error updating contact: {e}")
    
    def delete_contact(self):
        """Delete a contact with enhanced safety"""
        print("\n" + "="*50)
        print("           DELETE CONTACT")
        print("="*50)
        
        if not self.contacts:
            print("No contacts found. Please add some contacts first.")
            return
        
        self.view_contacts(show_pagination=False)
        
        try:
            choice = int(input("\nEnter contact number to delete: "))
            if 1 <= choice <= len(self.contacts):
                contact = self.contacts[choice - 1]
                
                # Show contact details before deletion
                print(f"\nContact to delete:")
                self.display_contact_details(contact)
                
                confirm = input(f"Are you sure you want to delete '{contact['name']}'? (yes/no): ").lower()
                if confirm in ['yes', 'y']:
                    # Create backup before deletion
                    self.create_backup()
                    
                    deleted_contact = self.contacts.pop(choice - 1)
                    if self.save_contacts():
                        print(f"\n✓ Contact '{deleted_contact['name']}' deleted successfully!")
                    else:
                        # Restore contact if save failed
                        self.contacts.insert(choice - 1, deleted_contact)
                        print("Error: Could not save changes. Contact deletion cancelled.")
                else:
                    print("Delete operation cancelled.")
            else:
                print("Error: Invalid contact number!")
                
        except ValueError:
            print("Error: Please enter a valid number!")
        except Exception as e:
            print(f"Error deleting contact: {e}")
    
    def export_contacts(self):
        """Export contacts to CSV or text file"""
        print("\n" + "="*50)
        print("           EXPORT CONTACTS")
        print("="*50)
        
        if not self.contacts:
            print("No contacts to export.")
            return
        
        print("Export formats:")
        print("1. CSV file")
        print("2. Text file")
        print("3. JSON file")
        
        format_choice = input("Choose export format (1-3): ").strip()
        filename = input("Enter filename (without extension): ").strip()
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"contacts_export_{timestamp}"
        
        try:
            if format_choice == '1':  # CSV
                filename += '.csv'
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['name', 'phone', 'email', 'address', 'category', 'created_date']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for contact in self.contacts:
                        writer.writerow(contact)
                
            elif format_choice == '2':  # Text
                filename += '.txt'
                with open(filename, 'w', encoding='utf-8') as txtfile:
                    txtfile.write("CONTACT LIST EXPORT\n")
                    txtfile.write("=" * 50 + "\n\n")
                    for i, contact in enumerate(self.contacts, 1):
                        txtfile.write(f"Contact {i}:\n")
                        txtfile.write(f"Name: {contact['name']}\n")
                        txtfile.write(f"Phone: {contact['phone']}\n")
                        txtfile.write(f"Email: {contact.get('email', 'Not provided')}\n")
                        txtfile.write(f"Address: {contact.get('address', 'Not provided')}\n")
                        txtfile.write(f"Category: {contact.get('category', 'Other')}\n")
                        if 'created_date' in contact:
                            created = datetime.fromisoformat(contact['created_date']).strftime("%Y-%m-%d %H:%M")
                            txtfile.write(f"Added: {created}\n")
                        txtfile.write("-" * 40 + "\n\n")
                        
            elif format_choice == '3':  # JSON
                filename += '.json'
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(self.contacts, jsonfile, indent=2, ensure_ascii=False)
            
            else:
                print("Invalid format choice!")
                return
            
            print(f"✓ Contacts exported successfully to {filename}")
            
        except Exception as e:
            print(f"Error exporting contacts: {e}")
    
    def import_contacts(self):
        """Import contacts from JSON or CSV file"""
        print("\n" + "="*50)
        print("           IMPORT CONTACTS")
        print("="*50)
        
        filename = input("Enter filename to import from: ").strip()
        
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found!")
            return
        
        try:
            imported_count = 0
            skipped_count = 0
            
            if filename.lower().endswith('.json'):
                with open(filename, 'r', encoding='utf-8') as file:
                    imported_contacts = json.load(file)
                    
            elif filename.lower().endswith('.csv'):
                imported_contacts = []
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        imported_contacts.append(row)
            else:
                print("Error: Unsupported file format! Use .json or .csv files.")
                return
            
            # Process imported contacts
            for contact in imported_contacts:
                # Check if contact already exists
                exists = False
                for existing_contact in self.contacts:
                    if (existing_contact['name'].lower() == contact['name'].lower() or
                        existing_contact['phone'] == contact['phone']):
                        exists = True
                        break
                
                if not exists:
                    # Ensure required fields
                    if 'category' not in contact:
                        contact['category'] = 'Other'
                    if 'created_date' not in contact:
                        contact['created_date'] = datetime.now().isoformat()
                    
                    self.contacts.append(contact)
                    imported_count += 1
                else:
                    skipped_count += 1
            
            if self.save_contacts():
                print(f"✓ Import completed!")
                print(f"  - Imported: {imported_count} contacts")
                print(f"  - Skipped (duplicates): {skipped_count} contacts")
            else:
                print("Error: Could not save imported contacts!")
                
        except Exception as e:
            print(f"Error importing contacts: {e}")
    
    def manage_backups(self):
        """Manage backup files"""
        print("\n" + "="*50)
        print("           BACKUP MANAGEMENT")
        print("="*50)
        
        print("1. Create new backup")
        print("2. List all backups")
        print("3. Restore from backup")
        print("4. Delete old backups")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '1':
            backup_file = self.create_backup()
            if backup_file:
                print("Backup created successfully!")
                
        elif choice == '2':
            try:
                backup_files = [f for f in os.listdir(self.backup_dir) if f.startswith('contacts_backup_')]
                if backup_files:
                    print("\nAvailable backups:")
                    for i, backup in enumerate(sorted(backup_files, reverse=True), 1):
                        file_path = os.path.join(self.backup_dir, backup)
                        timestamp = os.path.getmtime(file_path)
                        date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{i}. {backup} (Created: {date_str})")
                else:
                    print("No backup files found.")
            except Exception as e:
                print(f"Error listing backups: {e}")
                
        elif choice == '3':
            self.restore_from_backup()
            
        elif choice == '4':
            self.cleanup_old_backups()
    
    def restore_from_backup(self):
        """Restore contacts from a backup file"""
        try:
            backup_files = [f for f in os.listdir(self.backup_dir) if f.startswith('contacts_backup_')]
            if not backup_files:
                print("No backup files found.")
                return
            
            print("\nAvailable backups:")
            for i, backup in enumerate(sorted(backup_files, reverse=True), 1):
                file_path = os.path.join(self.backup_dir, backup)
                timestamp = os.path.getmtime(file_path)
                date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                print(f"{i}. {backup} (Created: {date_str})")
            
            choice = int(input(f"\nEnter backup number (1-{len(backup_files)}): "))
            if 1 <= choice <= len(backup_files):
                backup_file = sorted(backup_files, reverse=True)[choice - 1]
                backup_path = os.path.join(self.backup_dir, backup_file)
                
                confirm = input(f"Are you sure you want to restore from {backup_file}? This will replace all current contacts! (yes/no): ").lower()
                if confirm in ['yes', 'y']:
                    with open(backup_path, 'r', encoding='utf-8') as file:
                        self.contacts = json.load(file)
                    
                    if self.save_contacts():
                        print(f"✓ Contacts restored successfully from {backup_file}")
                    else:
                        print("Error: Could not save restored contacts!")
                else:
                    print("Restore operation cancelled.")
            else:
                print("Invalid backup number!")
                
        except Exception as e:
            print(f"Error restoring backup: {e}")
    
    def cleanup_old_backups(self):
        """Delete old backup files"""
        try:
            backup_files = [f for f in os.listdir(self.backup_dir) if f.startswith('contacts_backup_')]
            if len(backup_files) <= 5:
                print("No cleanup needed. Only keeping latest 5 backups.")
                return
            
            # Sort by creation time and keep only the latest 5
            backup_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.backup_dir, x)), reverse=True)
            files_to_delete = backup_files[5:]  # Keep latest 5, delete the rest
            
            print(f"Found {len(files_to_delete)} old backup files to delete.")
            confirm = input("Delete old backups? (yes/no): ").lower()
            
            if confirm in ['yes', 'y']:
                for backup_file in files_to_delete:
                    os.remove(os.path.join(self.backup_dir, backup_file))
                print(f"✓ Deleted {len(files_to_delete)} old backup files.")
            else:
                print("Cleanup cancelled.")
                
        except Exception as e:
            print(f"Error cleaning up backups: {e}")
    
    def filter_by_category(self):
        """Filter and display contacts by category"""
        print("\n" + "="*50)
        print("           FILTER BY CATEGORY")
        print("="*50)
        
        if not self.contacts:
            print("No contacts found.")
            return
        
        # Get unique categories
        categories = set(contact.get('category', 'Other') for contact in self.contacts)
        categories = sorted(list(categories))
        
        print("Available categories:")
        for i, category in enumerate(categories, 1):
            count = sum(1 for contact in self.contacts if contact.get('category', 'Other') == category)
            print(f"{i}. {category} ({count} contacts)")
        
        try:
            choice = int(input(f"\nEnter category number (1-{len(categories)}): "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                filtered_contacts = [contact for contact in self.contacts 
                                   if contact.get('category', 'Other') == selected_category]
                
                print(f"\nContacts in category '{selected_category}':")
                self.view_contacts(filtered_contacts, show_pagination=False)
            else:
                print("Invalid category number!")
                
        except ValueError:
            print("Error: Please enter a valid number!")
        except Exception as e:
            print(f"Error filtering contacts: {e}")

    def display_menu(self):
        """Display the enhanced main menu"""
        print("\n" + "="*60)
        print("                ADVANCED CONTACT MANAGER")
        print("="*60)
        print("1.  Add Contact")
        print("2.  View All Contacts")
        print("3.  Search Contacts")
        print("4.  Update Contact")
        print("5.  Delete Contact")
        print("6.  Filter by Category")
        print("7.  Export Contacts")
        print("8.  Import Contacts")
        print("9.  Backup Management")
        print("10. Contact Statistics")
        print("11. Exit")
        print("="*60)
    
    def show_statistics(self):
        """Display contact statistics"""
        print("\n" + "="*50)
        print("           CONTACT STATISTICS")
        print("="*50)
        
        if not self.contacts:
            print("No contacts found.")
            return
        
        total_contacts = len(self.contacts)
        
        # Category statistics
        categories = {}
        emails_provided = 0
        addresses_provided = 0
        
        for contact in self.contacts:
            category = contact.get('category', 'Other')
            categories[category] = categories.get(category, 0) + 1
            
            if contact.get('email'):
                emails_provided += 1
            if contact.get('address'):
                addresses_provided += 1
        
        print(f"Total Contacts: {total_contacts}")
        print(f"Contacts with Email: {emails_provided}")
        print(f"Contacts with Address: {addresses_provided}")
        
        print(f"\nContacts by Category:")
        for category, count in sorted(categories.items()):
            percentage = (count / total_contacts) * 100
            print(f"  {category}: {count} ({percentage:.1f}%)")
        
        # Recent additions
        recent_contacts = [c for c in self.contacts if 'created_date' in c]
        if recent_contacts:
            recent_contacts.sort(key=lambda x: x['created_date'], reverse=True)
            print(f"\nRecently Added (Last 5):")
            for contact in recent_contacts[:5]:
                created = datetime.fromisoformat(contact['created_date']).strftime("%Y-%m-%d")
                print(f"  {contact['name']} - {created}")

    def run(self):
        """Enhanced main program loop"""
        print("🌟 Welcome to Advanced Contact Manager! 🌟")
        print(f"Loaded {len(self.contacts)} existing contacts.")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (1-11): ").strip()
                
                if choice == '1':
                    self.add_contact()
                elif choice == '2':
                    self.view_contacts()
                elif choice == '3':
                    self.search_contact()
                elif choice == '4':
                    self.update_contact()
                elif choice == '5':
                    self.delete_contact()
                elif choice == '6':
                    self.filter_by_category()
                elif choice == '7':
                    self.export_contacts()
                elif choice == '8':
                    self.import_contacts()
                elif choice == '9':
                    self.manage_backups()
                elif choice == '10':
                    self.show_statistics()
                elif choice == '11':
                    # Create final backup before exit
                    if self.contacts:
                        self.create_backup()
                    print("\n🌟 Thank you for using Advanced Contact Manager! 🌟")
                    print("Your contacts have been saved automatically.")
                    print("Goodbye!")
                    break
                else:
                    print("❌ Error: Invalid choice! Please select 1-11.")
                
                # Pause before showing menu again
                if choice != '11':
                    input("\n⏸️  Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Program interrupted. Creating backup...")
                if self.contacts:
                    self.create_backup()
                print("Goodbye!")
                break
            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}")
                print("Please try again.")

# Run the Contact Manager
if __name__ == "__main__":
    contact_manager = ContactManager()
    contact_manager.run()