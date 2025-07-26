# Resume Reviewer AI - Instructions

## Setup and Run the Application

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```
   python init_db.py
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Using the Application

1. **Home Page**: View information about the application
2. **Upload Resume**: 
   - Select a job role from the dropdown
   - Upload your PDF resume using the drag-and-drop interface
   - If you have issues with the upload, use the "Try the simple upload form" link
3. **Analysis**: The system will analyze your resume and provide feedback
4. **Results**: View detailed feedback on your resume
5. **History**: If logged in, you can view your previously uploaded resumes
6. **Export**: Download your feedback as a text file

## OpenAI Integration (Optional)

The application includes mock AI suggestions by default. If you want to use real AI-powered suggestions:

1. Create a `.env` file in the root directory
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Update the `utils/ai_integration.py` file to use the OpenAI API

Note: The application works perfectly fine without an OpenAI API key, providing mock AI suggestions instead.

## Troubleshooting Upload Issues

If you're having trouble uploading files:

1. Try the simple upload form by clicking the link below the upload form
2. Make sure your file is in PDF format
3. Ensure the file size is under 16MB
4. Check that the uploads directory exists and is writable
5. If using the drag-and-drop interface, try a different browser

## File Structure

- `/static` - CSS, JavaScript, and assets
- `/templates` - HTML templates
- `/routes` - Route handlers
- `/utils` - Utility functions for resume parsing and analysis
- `/models` - Database models
- `app.py` - Main application file
- `config.py` - Configuration settings
- `init_db.py` - Database initialization script

## Test Accounts

You can register a new account or use these credentials:
- Username: test@example.com
- Password: password123 