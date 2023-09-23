import getpass
import json
import re
import datetime
import secrets
import bcrypt


user_file = "users.json"
projects_file = "projects.json"
activation_code = secrets.token_hex(16)

def load_data():
    try:
        with open(user_file, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    try:
        with open(projects_file, "r") as file:
            projects = json.load(file)
    except FileNotFoundError:
        projects = []

    return users, projects


def save_data(users,projects):

    with open(user_file,"w") as file:
        json.dump(users, file, indent=4)

    with open(projects_file,"w") as file:
        json.dump(projects, file, indent=4)


    

def authentication():
    print("Registration: ")
    while True:
        first_name = input("First Name: ")
        if first_name.isalpha():
            break
        else:
            print("Please enter a valid first name containing only letters.")
    while True:
        last_name = input("last Name: ")
        if last_name.isalpha():
            break
        else:
            print("Please enter a valid first name containing only letters.")
    while True:
        email = input("Email: ")
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            break
        else:
            print("Please enter a valid email address.")
    while True:
        password = input("Password: ")
        confirm_password = input("Confirm Password: ")

        if password == confirm_password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
            break
        else:
            print("Passwords do not match. Please try again.")
    while True:
        phone_number = input("Mobile Phone (Egyptian): ")

        if re.match(r'^01[0-2]\d{8}$', phone_number):
            break
        else:
            print("Please enter a valid Egyptian mobile phone number.")

    for user in users:
        if user["email"] == email:
            print("User with the same email already exists.")
            return
        elif user["phone_number"] == phone_number:
            print("User with the same phone number already exists.")
            return
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password.decode('utf-8'),  
        "phone_number": phone_number,
        "is_active": False,
    }

    users.append(user)
    save_data(users,[])
    print("Registration successful.")
    


        

users, _ = load_data()


def login():
    print("Login:")
    email = input("Email: ")
    password = getpass.getpass("Password: ")

    for user in users:
        if user["email"] == email and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            print("Login successful!")
            return email
    print("Invalid email or password.")
    return None

def create_project(logged_in_user_email):
    print("Create a Project:")
    title = input("Title: ")
    details = input("Details: ")
    total_target = float(input("Total Target Amount: "))
    start_date_str = input("Start Date (YYYY-MM-DD): ")
    end_date_str = input("End Date (YYYY-MM-DD): ")

    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
        return

    _, projects = load_data()

    project = {
        "title": title,
        "details": details,
        "total_target": total_target,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "created_by": logged_in_user_email  # Associate project with the logged-in user
    }
    projects.append(project)
    save_data([], projects)
    print("Project created successfully!")

def edit_project():
    print("Edit Project:")
    project_title = input("Enter the title of the project you want to edit: ")


    _, projects = load_data()

    for project in projects:
        if project['title'] == project_title:
            print("Enter the new details:")
            project['title'] = input("Title: ")
            project['details'] = input("Details: ")
            project['total_target'] = float(input("Total Target Amount: "))
            project['start_date'] = input("Start Date (YYYY-MM-DD):Sure! Here's the continuation of the code:")

            project['end_date'] = input("End Date (YYYY-MM-DD): ")
            save_data([], projects)
            print("Project updated successfully!")
            return

    print("Project not found.")

def delete_project():
    print("Delete Project:")
    project_title = input("Enter the title of the project you want to delete: ")


    _, projects = load_data()

    for project in projects:
        if project['title'] == project_title:
            projects.remove(project)
            save_data([], projects)
            print("Project deleted successfully!")
            return

    print("Project not found.")

def search_projects():
    print("Search Projects:")
    start_date_str = input("Enter the start date of the projects you want to search (YYYY-MM-DD): ")
    end_date_str = input("Enter the end date of the projects you want to search (YYYY-MM-DD): ")


    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
        return

    print("Matching Projects:")


    _, projects = load_data()

    for project in projects:
        project_start_date = datetime.datetime.strptime(project['start_date'], "%Y-%m-%d")
        if start_date <= project_start_date <= end_date:
            print(f"Title: {project['title']}")
            print(f"Details: {project['details']}")
            print(f"Total Target Amount: {project['total_target']}")
            print(f"Start Date: {project['start_date']}")
            print(f"End Date: {project['end_date']}")
            print("-----------------------")

def view_projects(logged_in_user_email):
    print("View Projects:")

    _, projects = load_data()

    if not projects:
        print("No projects available.")
    else:
        for index, project in enumerate(projects, start=1):
            # Check if the project is associated with the logged-in user
            if project.get("created_by") == logged_in_user_email:
                print("----------------------")
                print(f"Project {index}:")
                print(f"Title: {project['title']}")
                print(f"Details: {project['details']}")
                print(f"Total Target Amount: {project['total_target']} EGP")
                print(f"Start Date: {project['start_date']}")
                print(f"End Date: {project['end_date']}")
                print("-----------------------")




def main_menu():
    logged_in_user_email = None
    while True:
        print("\n--- Crowdfunding Console App ---")
        print("1. Register")
        print("2. Login")
        print("3. Create a Project")
        print("4. View Projects")
        print("5. Edit Project")
        print("6. Delete Project")
        print("7. Search Projects")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            authentication()
        elif choice == "2":
            logged_in_user_email = login()
        elif choice == "3":
            if logged_in_user_email:
                create_project(logged_in_user_email)  # Pass the logged-in user's email
            else:
                print("Please log in to create a project.")
        elif choice == "4":
            if logged_in_user_email:
                view_projects(logged_in_user_email)
            else:
                print("Please log in to view your projects.")
        elif choice == "5":
            edit_project()
        elif choice == "6":
            delete_project()
        elif choice == "7":
            search_projects()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
main_menu()