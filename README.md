# Resume-JD Match Check

A FastAPI-based application that uses AI to extract skills from resumes and job descriptions, then calculates a match score to help evaluate candidate suitability.

## 🚀 Features

- **Skill Extraction**: Automatically extract top 5 technical and soft skills from job descriptions and candidate resumes
- **AI-Powered Analysis**: Uses OpenAI's GPT-4 model for intelligent skill extraction
- **Match Scoring**: Calculate percentage match between required and candidate skills
- **PDF Support**: Process PDF files for both job descriptions and resumes
- **RESTful API**: Clean API endpoints for easy integration
- **Rate Limiting**: Built-in retry mechanism for API rate limits

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Resume_JD_Match_Check
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn python-multipart pdfplumber openai python-dotenv
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   PROJECT_NAME=Resume-JD Match Check
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./test.db
   ```

## 🚀 Running the Application

1. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## 📚 API Endpoints

### Health Check
- **GET** `/health` - Check if the service is running

### Skill Extraction
- **POST** `/extract-the-required-skills` - Extract skills from job description PDF
- **POST** `/extract-skills-of-candidate` - Extract skills from candidate resume PDF

### Match Analysis
- **POST** `/match-skill-score` - Compare job description and resume, return match score

## 🔧 Usage Examples

### Extract Skills from Job Description
```bash
curl -X POST "http://localhost:8000/extract-the-required-skills" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@job_description.pdf"
```

### Extract Skills from Resume
```bash
curl -X POST "http://localhost:8000/extract-skills-of-candidate" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@candidate_resume.pdf"
```

### Get Match Score
```bash
curl -X POST "http://localhost:8000/match-skill-score" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "job_description_file=@job_description.pdf" \
     -F "candidate_resume_file=@candidate_resume.pdf"
```

## 📁 Project Structure

```
Resume_JD_Match_Check/
├── app/
│   ├── api/
│   │   └── routes.py          # API route definitions
│   ├── core/
│   │   └── config.py          # Configuration settings
│   ├── services/
│   │   ├── extract_skills.py  # Core business logic
│   │   └── integrate_llm.py   # LLM integration
│   └── main.py                # FastAPI application entry point
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🔍 How It Works

1. **PDF Processing**: Uses `pdfplumber` to extract text from uploaded PDF files
2. **Skill Extraction**: Leverages OpenAI's GPT-4 model to intelligently identify top 5 skills from the extracted text
3. **Match Calculation**: Compares required skills (from job description) with candidate skills (from resume) to calculate a percentage match
4. **API Response**: Returns structured JSON with extracted skills, matched skills, and overall match score

## ⚙️ Configuration

The application uses environment variables for configuration:

- `PROJECT_NAME`: Name of the project (default: "FastAPI App")
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `DATABASE_URL`: Database connection string (default: SQLite)

## 🛡️ Error Handling

- **File Validation**: Only PDF files are accepted
- **Rate Limiting**: Automatic retry mechanism for OpenAI API rate limits
- **Error Responses**: Proper HTTP status codes and error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

## 🔮 Future Enhancements

- [ ] Support for more file formats (DOCX, TXT)
- [ ] Advanced skill matching algorithms
- [ ] User authentication and authorization
- [ ] Database integration for storing results
- [ ] Batch processing capabilities
- [ ] Skill categorization and weighting 