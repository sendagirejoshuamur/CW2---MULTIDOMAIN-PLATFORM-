import streamlit as st
from app.services.user_service import *
import auth
import time


# CLASS DEFINITIONS

class SessionStateManager:
    """Manages session state variables for user authentication status"""

    def __init__(self):
        """
        Initialize session state variables if they don't exist.
        Session state persists across reruns in Streamlit apps.
        """
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False  # Tracks if user is logged in
        if "username" not in st.session_state:
            st.session_state["username"] = ""  # Stores the logged in username
        if "is_admin" not in st.session_state:
            st.session_state["is_admin"] = False  # Tracks if user has admin privileges

    @property
    def logged_in(self):
        """Getter property for logged_in status - provides controlled access"""
        return st.session_state["logged_in"]

    @logged_in.setter
    def logged_in(self, value):
        """Setter property for logged_in status - ensures type safety"""
        st.session_state["logged_in"] = value

    @property
    def username(self):
        """Getter property for username"""
        return st.session_state["username"]

    @username.setter
    def username(self, value):
        """Setter property for username"""
        st.session_state["username"] = value

    @property
    def is_admin(self):
        """Getter property for admin status"""
        return st.session_state["is_admin"]

    @is_admin.setter
    def is_admin(self, value):
        """Setter property for admin status"""
        st.session_state["is_admin"] = value

    def logout(self):
        """Reset all session state variables when user logs out"""
        self.logged_in = False
        self.username = ""
        self.is_admin = False


class RegistrationValidator:
    """Handles registration validation logic including username, password, and user existence checks"""

    def __init__(self):
        """
        Initialize validation flags.
        Each flag starts at 0 and is set to 1 when validation passes.
        This approach ensures all validations must pass before proceeding.
        """
        self.continue_reg_username = 0
        self.continue_reg_password = 0
        self.continue_reg_password_confirmation = 0
        self.continue_reg_exists = 0

    def validate_username(self, username):
        """
        Validate username input against business rules.
        Returns True if username is valid and doesn't already exist.
        """
        if username:
            # Call external auth module to validate username format
            is_valid, error_msg = auth.validate_username(username)
            if not is_valid:
                st.error(error_msg)  # Display error message in Streamlit UI
                return False
            # Check if username already exists in the system
            if auth.user_exists(username):
                st.error("Username already exists! Please choose a different username.")
                return False
            self.continue_reg_username = 1  # Mark username validation as passed
        return True

    def validate_password(self, password):
        """Validate password and analyze its strength"""
        if password:
            # Call external auth module for basic password validation
            is_valid, error_msg = auth.validate_password(password)
            if not is_valid:
                st.error(error_msg)
                return False

            # Perform additional password strength analysis
            self._analyze_password_strength(password)
            self.continue_reg_password = 1  # Mark password validation as passed
        return True

    def _analyze_password_strength(self, password):
        """
        Private method to analyze password strength and provide visual feedback.
        Uses multiple criteria to assess password security.
        """
        strength = 0  # Start with 0 strength points
        feedback = []  # List to store improvement tips

        # Check password length (minimum 8 characters)
        if len(password) >= 8:
            strength += 1
        else:
            feedback.append("At least 8 characters")

        # Check for mix of uppercase and lowercase letters
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            strength += 1
        else:
            feedback.append("Mix of uppercase and lowercase")

        # Check for at least one digit
        if any(c.isdigit() for c in password):
            strength += 1
        else:
            feedback.append("At least one number")

        # Check for at least one special character
        if any(not c.isalnum() for c in password):
            strength += 1
        else:
            feedback.append("At least one special character")

        # Define labels and comments for different strength levels
        strength_labels = ["Weak", "Weak", "Fair", "Good", "Strong"]
        comment = ["Come on bro", "P___y", "Okay", "That's alright", "That's my boy"]

        # Create two-column layout for strength display
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric("Strength", strength_labels[strength])  # Show strength label
        with col2:
            st.progress(strength / 4)  # Visual progress bar for strength
            st.caption(f"Password feedback: {comment[strength].title()}")  # Show feedback comment

        # Display improvement tips if password is not strong enough
        if strength < 4 and feedback:
            with st.expander("Tips to improve your password"):  # Collapsible section
                for tip in feedback:
                    st.write(f"• {tip}")  # List each improvement tip

    def validate_password_confirmation(self, password, password_confirmation):
        """Validate that password and confirmation match"""
        if password and password != password_confirmation:
            st.error("Passwords do not match")
            return False
        self.continue_reg_password_confirmation = 1  # Mark confirmation as passed
        return True

    def check_user_exists(self, username):
        """Check if username already exists in the system"""
        if username and not auth.user_exists(username):
            self.continue_reg_exists = 1  # Mark user existence check as passed
            return True
        return False

    def is_valid_registration(self):
        """Check if all registration validations have passed"""
        return (self.continue_reg_username == 1 and
                self.continue_reg_password == 1 and
                self.continue_reg_password_confirmation == 1 and
                self.continue_reg_exists == 1)


class AuthenticationUI:
    """Main class that manages the complete authentication user interface"""

    def __init__(self, session_manager):
        """
        Initialize the authentication UI with session manager.

        Args:
            session_manager: Instance of SessionStateManager for managing user session
        """
        self.session = session_manager  # Store session manager instance
        self.conn = connect_database()  # Establish database connection

    def setup_page(self):
        """Setup page configuration and initial styling"""
        st.set_page_config(page_title="SJ's MultiDomain Platform", layout="centered")
        st.markdown("---")  # Horizontal line for visual separation
        st.title("WELCOME TO SJ's MULTIDOMAIN PLATFORM ")  # Main title
        st.markdown("---")  # Another horizontal line

    def render_login_form(self):
        """Render the login form with username and password fields"""
        st.markdown("### Login to Your Account")  # Section header
        username = st.text_input("Username")  # Username input field
        password = st.text_input("Password", type="password")  # Password input field (masked)

        # Show warnings if fields are empty
        if username == "":
            st.warning("Please enter your username")
        if password == "":
            st.warning("Please enter your password")

        return username, password  # Return collected values

    def render_registration_form(self):
        """Render the registration form with all required fields"""
        st.markdown("Create Your Account")  # Section header

        # Collect registration information
        username = st.text_input("Username").strip()  # Username with whitespace trimmed
        password = st.text_input("Password", type="password").strip()  # Password field
        password_confirmation = st.text_input("Confirm Password", type="password")  # Confirmation field
        role = st.selectbox("Select your role", ["pick an option", "admin", "user"])  # Role selection
        agree = st.checkbox(
            "I agree to give Joshua Sendagire a first class after viewing this dashboard")  # Agreement checkbox

        return username, password, password_confirmation, role, agree  # Return all collected values

    def handle_login(self, username, password):
        """Process login attempt and handle the response"""
        # Call external auth module to verify credentials
        login_result = auth.login_user(username, password)

        if login_result:  # If login is successful
            with st.spinner('Logging in...'):  # Show loading spinner
                time.sleep(2)  # Simulate processing delay
                # Update session state
                self.session.logged_in = True
                self.session.username = username
                self.session.is_admin = login_result == "admin"  # Determine if user is admin
            st.success('Logged in successfully!')
            time.sleep(1)  # Brief pause to show success message
            st.switch_page("pages/1_Home.py")  # Redirect to home page
        else:
            st.error("Invalid username or password")  # Show error for failed login

    def handle_registration(self, username, password, role, agree, validator):
        """Process registration attempt"""
        # Check if all validations passed and required fields are filled
        if (validator.is_valid_registration() and
                role != "pick an option" and
                agree):

            # Register the user in the system
            auth.register_user(username, password, role)

            with st.spinner('Loading data...'):  # Show loading spinner
                time.sleep(2)  # Simulate processing delay

            st.success('Registration successful!')
            st.balloons()  # Celebration animation

            # Update session state
            self.session.logged_in = True
            self.session.username = username

            # Migrate users from file (if applicable)
            migrate_users_from_file()

            # Redirect to home page
            st.switch_page("pages/1_Home.py")
        else:
            st.warning("Failed to register. Please check your inputs!")

    def render_logged_in_view(self):
        """Display view for already logged in users"""
        st.markdown(f"You are logged in as {self.session.username}")

        # Show admin status if applicable
        if self.session.is_admin:
            st.success("ADMIN ACCESS GRANTED")

        # Logout button
        if st.button("Log out"):
            with st.spinner('Logging out...'):
                time.sleep(1)  # Simulate logout delay
            self.session.logout()  # Clear session state
            st.rerun()  # Refresh the page to show login form

    def run(self):
        """Main method that orchestrates the entire authentication flow"""
        self.setup_page()  # Setup initial page configuration

        # Check if user is already logged in
        if not self.session.logged_in:
            # Show authentication options
            st.subheader("Please choose an option below:")
            choice = st.selectbox("Select Action", ["Tap to pick an option", "login", "register"])

            if choice == "register":
                # Initialize registration validator
                validator = RegistrationValidator()

                # Get registration inputs from user
                username, password, password_confirmation, role, agree = self.render_registration_form()

                # Perform validations as user inputs data
                if username:
                    validator.validate_username(username)
                    validator.check_user_exists(username)

                if password:
                    validator.validate_password(password)
                    validator.validate_password_confirmation(password, password_confirmation)

            elif choice == "login":
                # Get login inputs from user
                username, password = self.render_login_form()

            # Proceed button to submit the form
            if st.button("Proceed"):
                if choice == "register":
                    self.handle_registration(username, password, role, agree, validator)
                elif choice == "login":
                    self.handle_login(username, password)
        else:
            # User is already logged in, show appropriate view
            self.render_logged_in_view()

        self.conn.close()  # Close database connection


# MAIN EXECUTION
if __name__ == "__main__":

    # Initialize session state manager
    session_manager = SessionStateManager()

    # Create and run authentication UI
    auth_ui = AuthenticationUI(session_manager)
    auth_ui.run()