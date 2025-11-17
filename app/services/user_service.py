import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table, create_all_tables
from app.data.csv_loaders import load_all_csv_data



def register_user(username, password, role='user'):
    """
    Register new user with password hashing.

    Args:
        username: User's login name
        password: Plain text password
        role: User role (default: 'user')

    Returns:
        tuple: (success: bool, message: str)
    """
    # Hashing password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Insert into database
    try:
        insert_user(username, password_hash, role)
        return True, f"User '{username}' registered successfully."
    except Exception as e:
        return False, f"Registration failed: {str(e)}"


def login_user(username, password):
    """
    Authenticate user.

    Args:
        username: User's login name
        password: Plain text password to verify

    Returns:
        tuple: (success: bool, message: str)
    """
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful! Welcome {username}."
    return False, "Incorrect password."

# DB_PATH = Path(r"C:\Users\senda\Desktop\CW2_M01045908_CST1510\DATA") / "intelligence_platform.db"
# filepath= Path(r"C:\Users\senda\Desktop\CW2_M01045908_CST1510\DATA") / "users.txt"
# filepath='DATA/users.txt'
def migrate_users_from_file(filepath= Path(r"C:\Users\senda\Desktop\CW2_M01045908_CST1510\DATA") / "users.txt"):
    """
    Migrate users from text file to database.

    Args:
        filepath: Path to users.txt file

    Returns:
        int: Number of users migrated
    """
    if not Path(filepath).exists():
        print(f"File not found: {filepath}")
        return 0

    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: username,password_hash,role
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) > 2 else 'user'

                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                        print(f"Migrated user: {username}")
                except Exception as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit()
    conn.close()
    print(f"Migration complete! {migrated_count} users migrated.")
    return migrated_count


def change_user_password(username, old_password, new_password):
    """
    Change user password after verifying old password.

    Args:
        username: User's login name
        old_password: Current password for verification
        new_password: New password to set

    Returns:
        tuple: (success: bool, message: str)
    """
    # First verify old password
    success, message = login_user(username, old_password)
    if not success:
        return False, "Current password is incorrect."

    # Hash new password
    new_password_hash = bcrypt.hashpw(
        new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Update password in database
    conn = connect_database()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (new_password_hash, username)
        )
        conn.commit()
        conn.close()
        return True, "Password changed successfully."
    except Exception as e:
        conn.close()
        return False, f"Password change failed: {str(e)}"


def get_user_role(username):
    """
    Get user role by username.

    Args:
        username: User's login name

    Returns:
        str: User role or None if user not found
    """
    user = get_user_by_username(username)
    if user:
        return user[3]  # role column
    return None


def is_admin(username):
    """
    Check if user has admin role.

    Args:
        username: User's login name

    Returns:
        bool: True if user is admin, False otherwise
    """
    role = get_user_role(username)
    return role == 'admin'


def is_analyst(username):
    """
    Check if user has analyst role.

    Args:
        username: User's login name

    Returns:
        bool: True if user is analyst, False otherwise
    """
    role = get_user_role(username)
    return role == 'analyst'


def validate_password_strength(password):
    """
    Validate password strength.

    Args:
        password: Password to validate

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."

    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."

    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."

    return True, "Password strength is good."


def create_default_admin():
    """
    Create a default admin user if no users exist.

    Returns:
        tuple: (success: bool, message: str)
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Check if any users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        # Create default admin user
        success, message = register_user(
            username="admin",
            password="Admin123!",
            role="admin"
        )
        conn.close()
        return success, f"Default admin created. {message}"

    conn.close()
    return True, "Users already exist in database."


def setup_authentication_system():
    """
    Complete setup for authentication system.

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Ensure users table exists
        conn = connect_database()
        create_users_table(conn)
        conn.close()

        # Migrate existing users
        migrated_count = migrate_users_from_file()

        # Create default admin if no users
        if migrated_count == 0:
            success, message = create_default_admin()
            return success, f"{message} No users migrated from file."

        return True, f"Authentication system ready. {migrated_count} users migrated."

    except Exception as e:
        return False, f"Authentication setup failed: {str(e)}"


