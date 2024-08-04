# Job Portal README

## Project Description
A job portal developed with Django connects job seekers with employers. The platform allows users to create profiles, upload resumes, and apply for jobs. Employers can post job listings, specifying details like job title, description, requirements, and company information. Job seekers can search for jobs using various filters such as location, industry, and job type, and save job listings for later reference. The portal also includes a notification system to alert users about new job postings and application status updates. Administrators have a dashboard to manage job postings, applications, and user accounts, ensuring a smooth operation of the platform.

## Features
- **User Authentication**: Registration, login, and profile management for both job seekers and employers.
- **Job Listings**: Post and manage job listings with details like title, description, and requirements.
- **Job Applications**: Submit applications, upload resumes, and track application status.
- **Search and Filters**: Search for jobs using filters like location, industry, and job type.
- **Notifications and Alerts**: Receive email notifications for new job listings and application updates.
- **Admin Dashboard**: Manage job postings, applications, and user accounts.
- **Employer Features**: Employers can log in, register, post job vacancies, and view the candidate list only for their own job postings.

## Installation

### Prerequisites
- Python 3.6+
- Django 3.0+
- PostgreSQL (or any preferred database)

### Setup
1. **Clone the repository**
    ```bash
    https://github.com/ROKAYASURESH/jobportal-.git
    cd jobportal
    ```

2. **Create a own virtual environment**
    ```bash
    python -m venv my_env
    source venv/bin/activate   # On Windows use `./my_env/Scripts/activate`
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup the database**
    - Create a PostgreSQL database and a user with appropriate permissions.
    - Update the `DATABASES` setting in `settings.py` with your database credentials.

5. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**
    ```bash
    python manage.py runserver
    ```

8. **Access the application**
    Open your web browser and go to `http://127.0.0.1:8000/`

## Usage

### User Authentication
- **Registration**: Users (both job seekers and employers) can sign up by providing their details.
- **Login**: Registered users can log in with their credentials.
- **Profile Management**: Users can manage and update their profiles.

### Job Listings
- **Post Job**: Employers can post job listings with details like title, description, requirements, and company information.
- **Manage Listings**: Employers can edit or delete their job listings.

### Job Applications
- **Apply for Jobs**: Job seekers can apply for jobs by submitting applications and uploading resumes.
- **Track Application Status**: Users can track the status of their job applications.

### Search and Filters
- **Search Jobs**: Job seekers can search for jobs using keywords.
- **Filter Jobs**: Jobs can be filtered by location, industry, and job type.

### Notifications and Alerts
- **Email Notifications**: Users receive email notifications for new job listings and application status updates.
- **In-app Notifications**: Users receive in-app notifications for job-related updates.

### Admin Dashboard
- **Manage Job Postings**: Admins can view, edit, and delete job postings.
- **Manage Applications**: Admins can view and manage job applications.
- **Manage User Accounts**: Admins can manage user accounts, including activation and deactivation.

### Employer Features
- **Employer Registration and Login**: Employers can register and log in to the platform.
- **Job Vacancy Posting**: Employers can post job vacancies with necessary details.
- **View Candidate List**: Employers can view the list of candidates who have applied for their job postings only.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## Contact
For any queries or issues, please contact [sureshrokaya761@gmail.com].

---
