from datetime import datetime
import json
from . import db

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    overall_score = db.Column(db.Integer)  # Score out of 100
    summary = db.Column(db.Text)
    ats_compatible = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Store detailed feedback as JSON
    _section_feedback = db.Column(db.Text)  # JSON string for section feedback
    _keyword_matches = db.Column(db.Text)   # JSON string for keyword matches
    _suggestions = db.Column(db.Text)       # JSON string for suggestions
    
    def __init__(self, resume_id, overall_score, summary, ats_compatible,
                 section_feedback=None, keyword_matches=None, suggestions=None):
        self.resume_id = resume_id
        self.overall_score = overall_score
        self.summary = summary
        self.ats_compatible = ats_compatible
        self.section_feedback = section_feedback or {}
        self.keyword_matches = keyword_matches or {}
        self.suggestions = suggestions or []
    
    @property
    def section_feedback(self):
        """Get section feedback as dictionary"""
        if self._section_feedback:
            return json.loads(self._section_feedback)
        return {}
    
    @section_feedback.setter
    def section_feedback(self, value):
        """Set section feedback from dictionary"""
        self._section_feedback = json.dumps(value)
    
    @property
    def keyword_matches(self):
        """Get keyword matches as dictionary"""
        if self._keyword_matches:
            return json.loads(self._keyword_matches)
        return {}
    
    @keyword_matches.setter
    def keyword_matches(self, value):
        """Set keyword matches from dictionary"""
        self._keyword_matches = json.dumps(value)
    
    @property
    def suggestions(self):
        """Get suggestions as list"""
        if self._suggestions:
            return json.loads(self._suggestions)
        return []
    
    @suggestions.setter
    def suggestions(self, value):
        """Set suggestions from list"""
        self._suggestions = json.dumps(value)
    
    def __repr__(self):
        return f'<Feedback for Resume {self.resume_id}, Score: {self.overall_score}>' 