from flask import Blueprint, render_template, current_app
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@main.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@main.route('/contact')
def contact():
    """Render the contact page"""
    return render_template('contact.html')

@main.route('/job-roles')
def job_roles():
    """Return available job roles"""
    return {"job_roles": current_app.config['JOB_ROLES']} 