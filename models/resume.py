from datetime import datetime
import os
from . import db

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_size = db.Column(db.Integer)  # Size in bytes
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationship with Feedback model
    feedback = db.relationship('Feedback', backref='resume', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, filename, original_filename, file_path, job_role, user_id=None, file_size=None):
        self.filename = filename
        self.original_filename = original_filename
        self.file_path = file_path
        self.job_role = job_role
        self.user_id = user_id
        self.file_size = file_size
    
    def __repr__(self):
        return f'<Resume {self.original_filename} for {self.job_role}>'
    
    @property
    def file_size_kb(self):
        """Return file size in KB"""
        if self.file_size:
            return round(self.file_size / 1024, 2)
        return 0
        
    def delete_file(self):
        """Delete the physical file from storage"""
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                return True
        except Exception as e:
            print(f"Error deleting file: {e}")
        return False 