![Screenshot 2025-04-30 101816](https://github.com/user-attachments/assets/7f92c1cd-08ea-4874-b130-359a1521bdbf)# AI-Based Interview Preparation Platform

A web application to help users prepare for job interviews by generating interview questions based on their resumes or selected job roles, analyzing their answers (text or voice), and providing AI-based feedback along with performance reports. This platform aims to simulate real-time interview environments, giving users valuable insights and helping them improve over time.

## 🚀 Features

- **User Authentication:** Secure login/signup system for personalized experience.

- **Resume Analyzer:** Upload and parse resumes to extract relevant keywords (skills, experiences).

- **Question Generator:** Dynamic interview questions based on user role or resume.

- **Mock Interview System:** Users answer questions (text or voice) in a simulated interview environment.

- **AI Answer Analysis:** Automated analysis of user responses, including grammar and content check.

- **Speech-to-Text Conversion:** Voice-based answers converted to text for analysis.

- **Performance Dashboard:** Track progress, scores, and improvement over time.

- **Weekly Reports:** Receive email summaries of performance, trends, and improvement.




## 🧑‍💻 Technologies Used

- **Backend:** Django, Django Rest Framework

- **Frontend:** HTML, CSS, Bootstrap/Tailwind (or React if advanced)

- **Resume Parsing:** PyPDF2, Spacy

- **AI/NLP:** HuggingFace Transformers, OpenAI GPT API (optional)

- **Voice to Text:** Google Speech-to-Text API

- **Emails:** Django Email Framework

- **Deployment:** Railway, Render, or AWS EC2 for hosting
## 📂 Folder Structure

```
interviewprep/
├── core/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   │   ├── dashboard.css
│   │   │   ├── form.css
│   │   │   └── style.css
│   │   ├── images/
│   │   │   ├── bg_base.jpg (or png)
│   │   │   └── bg_home.jpg (or png)
│   │   └── js/
│   │       ├── dashboard.js
│   │       └── recorder.js
│   ├── templates/
│   │   └── core/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── feedback.html
│   │       ├── generate_questions.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── mock_interview.html
│   │       ├── register.html
│   │       ├── report.html
│   │       ├── reports_summary.html
│   │       ├── thank_you.html
│   │       └── upload_resume.html
│   ├── emails/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── report.html
│   │   ├── settings.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
├── db.sqlite3
├── manage.py
├── requirements.txt
├── venv/

```
## 🛠️ Setup Instructions

**1. Clone the repository:**
```
git clone https://github.com/yourusername/interviewprep.git
cd interviewprep
```
**2. Install dependencies:**
```
pip install -r requirements.txt

```
**3.Set up the database:**
``` 
python manage.py migrate

```
**4.Run the development server:**
```
python manage.py runserver

```
Visit `http://127.0.0.1:8000` to access the app!
## 📈 Features Walkthrough
**1. User Authentication**
- Users can log in or register to save their progress.

**2. Resume Upload & Parsing**
- Upload resumes in PDF format.

- The system extracts skills and keywords using Spacy for job-specific interview questions.

**3. Question Generation**
- Dynamic interview questions are generated based on the uploaded resume or selected job role.

- OpenAI GPT API or predefined templates are used for generating questions.

**4. Mock Interview**
- Users answer interview questions one at a time, either through text or voice input.

**5. AI Analysis**
- Responses are checked for grammar, fluency, and completeness.

- Content analysis ensures keywords and job-relevant details are included.

- Speech-to-text is used for voice answers, and tone analysis is done (optional).

**6. Performance Dashboard**
- View performance statistics and track improvement over time.

**7. Weekly Reports**
- Get weekly email reports summarizing progress and areas for improvement.

![Screenshot 2025-04-30 101816](https://github.com/user-attachments/assets/c0a3808d-8280-45c7-8ccb-9c15be90d075 | width = 100)
![Screenshot 2025-04-30 101833](https://github.com/user-attachments/assets/f4f888f9-efc5-481a-bac7-5d71ac13fa5e)

## 📨 Email Notifications

The system sends weekly progress reports to users. Set up an email backend using Django’s Email Framework for this feature. You can use Celery and Redis for scheduling these reports.
## 👨‍💻 Contributing

Feel free to fork this repository, submit issues, and create pull requests! Contributions are welcome.


