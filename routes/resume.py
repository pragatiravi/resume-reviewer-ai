import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Resume, Feedback
from utils.resume_parser import extract_text_from_pdf, parse_resume_sections
from utils.analyzer import analyze_resume
from utils.ai_integration import get_ai_suggestions, generate_ai_summary
import json

resume = Blueprint('resume', __name__)

def allowed_file(filename):
    """Check if file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@resume.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle resume upload"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'resume' not in request.files:
            flash('No file part. Please try the simple upload form.')
            return redirect(url_for('resume.simple_upload'))
            
        file = request.files['resume']
        job_role = request.form.get('job_role')
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if not job_role:
            flash('Please select a job role')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Create uploads directory if it doesn't exist
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Generate unique filename
            original_filename = secure_filename(file.filename)
            file_ext = original_filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save the file
            file.save(file_path)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create resume record
            user_id = current_user.id if current_user.is_authenticated else None
            resume = Resume(
                filename=unique_filename,
                original_filename=original_filename,
                file_path=file_path,
                job_role=job_role,
                user_id=user_id,
                file_size=file_size
            )
            
            db.session.add(resume)
            db.session.commit()
            
            # Redirect to analysis page
            return redirect(url_for('resume.analyze', resume_id=resume.id))
            
        else:
            flash('Only PDF files are allowed')
            return redirect(request.url)
            
    # GET request - show upload form
    job_roles = current_app.config['JOB_ROLES']
    return render_template('resume/upload.html', job_roles=job_roles)

@resume.route('/simple-upload', methods=['GET', 'POST'])
def simple_upload():
    """Handle resume upload with a simpler form"""
    if request.method == 'POST':
        # Process the form submission (same as in upload route)
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['resume']
        job_role = request.form.get('job_role')
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if not job_role:
            flash('Please select a job role')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Create uploads directory if it doesn't exist
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Generate unique filename
            original_filename = secure_filename(file.filename)
            file_ext = original_filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save the file
            file.save(file_path)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create resume record
            user_id = current_user.id if current_user.is_authenticated else None
            resume = Resume(
                filename=unique_filename,
                original_filename=original_filename,
                file_path=file_path,
                job_role=job_role,
                user_id=user_id,
                file_size=file_size
            )
            
            db.session.add(resume)
            db.session.commit()
            
            # Redirect to analysis page
            return redirect(url_for('resume.analyze', resume_id=resume.id))
            
        else:
            flash('Only PDF files are allowed')
            return redirect(request.url)
    
    # GET request - show simple upload form
    job_roles = current_app.config['JOB_ROLES']
    return render_template('resume/simple_upload.html', job_roles=job_roles)

@resume.route('/analyze/<int:resume_id>')
def analyze(resume_id):
    """Analyze uploaded resume"""
    # Get resume record
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if feedback already exists
    if resume.feedback:
        return redirect(url_for('resume.results', resume_id=resume_id))
    
    # Extract text from PDF
    resume_text = extract_text_from_pdf(resume.file_path)
    
    if not resume_text:
        flash('Could not extract text from the PDF. Please try again with a different file.')
        return redirect(url_for('resume.upload'))
    
    # Parse resume sections
    sections = parse_resume_sections(resume_text)
    
    # Get job role keywords
    job_role = resume.job_role
    job_keywords = current_app.config['JOB_ROLE_KEYWORDS'].get(
        job_role, current_app.config['DEFAULT_KEYWORDS']
    )
    
    # Analyze resume
    analysis_results = analyze_resume(resume_text, sections, job_role, job_keywords)
    
    # Get AI suggestions
    ai_suggestions = get_ai_suggestions(
        resume_text, 
        job_role, 
        analysis_results["keyword_matches"], 
        analysis_results["section_feedback"]
    )
    
    # Add AI suggestions to the results
    analysis_results["suggestions"].extend(ai_suggestions)
    
    # Create feedback record
    feedback = Feedback(
        resume_id=resume_id,
        overall_score=analysis_results["overall_score"],
        summary=analysis_results["summary"],
        ats_compatible=analysis_results["ats_compatible"],
        section_feedback=analysis_results["section_feedback"],
        keyword_matches=analysis_results["keyword_matches"],
        suggestions=analysis_results["suggestions"]
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    # Redirect to results page
    return redirect(url_for('resume.results', resume_id=resume_id))

@resume.route('/results/<int:resume_id>')
def results(resume_id):
    """Display resume analysis results"""
    # Get resume record
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if feedback exists
    if not resume.feedback:
        flash('Resume has not been analyzed yet')
        return redirect(url_for('resume.analyze', resume_id=resume_id))
    
    # Get feedback
    feedback = resume.feedback
    
    return render_template(
        'resume/results_new.html',
        resume=resume,
        feedback=feedback,
        job_role=resume.job_role
    )

@resume.route('/history')
@login_required
def history():
    """Display user's resume history"""
    resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.upload_date.desc()).all()
    return render_template('resume/history.html', resumes=resumes)

@resume.route('/download/<int:resume_id>')
def download_resume(resume_id):
    """Download original resume"""
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if user is authorized to download this resume
    if resume.user_id and current_user.is_authenticated and resume.user_id != current_user.id:
        flash('You are not authorized to download this resume')
        return redirect(url_for('main.index'))
    
    return send_file(
        resume.file_path,
        as_attachment=True,
        download_name=resume.original_filename
    )

@resume.route('/export/<int:resume_id>')
def export_feedback(resume_id):
    """Export feedback as text file"""
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if feedback exists
    if not resume.feedback:
        flash('Resume has not been analyzed yet')
        return redirect(url_for('resume.analyze', resume_id=resume_id))
    
    # Check if user is authorized to export this feedback
    if resume.user_id and current_user.is_authenticated and resume.user_id != current_user.id:
        flash('You are not authorized to export this feedback')
        return redirect(url_for('main.index'))
    
    # Get feedback
    feedback = resume.feedback
    
    # Create feedback text
    feedback_text = f"""Resume Review for {resume.original_filename} - {resume.job_role} Position
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Overall Score: {feedback.overall_score}/100

Summary:
{feedback.summary}

ATS Compatibility: {"Yes" if feedback.ats_compatible else "No"}

Section Feedback:
"""
    
    # Add section feedback
    for section, section_feedback in feedback.section_feedback.items():
        feedback_text += f"- {section.capitalize()}: {section_feedback}\n"
    
    feedback_text += "\nKeyword Analysis:\n"
    
    # Add matched keywords
    feedback_text += "Matched Keywords:\n"
    for match in feedback.keyword_matches.get("matched", []):
        feedback_text += f"- {match['keyword']} (Importance: {match['importance']})\n"
    
    # Add missing keywords
    feedback_text += "\nMissing Keywords:\n"
    for missing in feedback.keyword_matches.get("missing", []):
        feedback_text += f"- {missing['keyword']} (Importance: {missing['importance']})\n"
    
    feedback_text += f"\nKeyword Match Percentage: {feedback.keyword_matches.get('match_percentage', 0)}%\n"
    
    # Add suggestions
    feedback_text += "\nSuggestions for Improvement:\n"
    for i, suggestion in enumerate(feedback.suggestions, 1):
        feedback_text += f"{i}. {suggestion}\n"
    
    # Create a temporary file
    filename = f"resume_feedback_{resume_id}.txt"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    with open(filepath, 'w') as f:
        f.write(feedback_text)
    
    return send_file(
        filepath,
        as_attachment=True,
        download_name=f"Resume_Feedback_{resume.job_role.replace(' ', '_')}.txt"
    )

@resume.route('/delete/<int:resume_id>', methods=['POST'])
@login_required
def delete_resume(resume_id):
    """Delete resume and associated feedback"""
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if user is authorized to delete this resume
    if resume.user_id != current_user.id:
        flash('You are not authorized to delete this resume')
        return redirect(url_for('resume.history'))
    
    # Delete physical file
    resume.delete_file()
    
    # Delete from database (cascade will delete feedback too)
    db.session.delete(resume)
    db.session.commit()
    
    flash('Resume deleted successfully')
    return redirect(url_for('resume.history')) 