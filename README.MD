# EgyCrowd — Crowdfunding Platform for Egypt

EgyCrowd is a full-stack crowdfunding web platform built with Django, designed
to help Egyptians launch and support fundraising campaigns for education,
health, community, and other causes. Inspired by GoFundMe and Kickstarter,
tailored for the Egyptian market.

---

##  Full Feature List

### Authentication & User Management
- **Registration** with: first name, last name, email, password, password
  confirmation, mobile phone number (validated against Egyptian phone
  number formats), and an optional profile picture.
- **In-browser image cropping** (via Cropper.js) when uploading a profile
  picture, so the user can frame their photo before it's saved (avoids the
  face getting cut off by automatic center-cropping).
- **Mandatory email activation**: a new account cannot log in until the
  activation link sent to their email is clicked. The link **expires after
  24 hours**.
- **Login** with email + password (via django-allauth).
- **Logout** with a confirmation page before ending the session.
- **Forgot Password**: users can request a password reset link sent to
  their email.
- **Facebook Login** *(in progress)*: social sign-in via Facebook.
- **Twitter/X Login** *(in progress)*: social sign-in via Twitter/X.
- **Profile page** with two tabs:
  - **My Projects** — every project the user has created, with a visual
    "Cancelled" badge on cancelled ones.
  - **My Donations** — a table of every donation made, with project name,
    amount, status, and date.
- **Edit profile**: update all fields (name, phone, picture, birthdate,
  Facebook profile link, country) — **email cannot be changed**.
- **Delete account**: requires a confirmation step **and re-entering the
  account password** before deletion is allowed.

### Projects
- **Create a project** with:
  - Title, details/description
  - Category (selected from admin-managed categories)
  - **Ability to add a brand-new category on the fly** via a modal/AJAX
    popup, without leaving the create-project page or needing admin access
  - Multiple tags
  - Multiple photos (uploaded via an inline formset)
  - Total funding target (in EGP)
  - Start date/time and end date/time
- **Edit an existing project**: update any field, add new photos, or
  remove existing ones — restricted to the project's creator only
  (enforced server-side, not just hidden in the UI).
- **Project detail page** includes:
  - An **image slider/carousel** cycling through all uploaded photos
  - **Average star rating**, computed from all user ratings
  - Ability to **rate** the project (1–5 stars), **update** your existing
    rating, or **remove** your rating entirely
  - **Comments**, including **threaded replies** (a comment can have
    replies nested underneath it)
  - **Report** button for both the project itself and individual comments
    (inappropriate content flagged for admin review)
  - **4 similar projects** shown, matched by shared tags
  - Creator-only controls: **Edit Project** and **Cancel Project**
    (cancellation is only allowed while donations remain **below 25%** of
    the funding target — enforced in the model logic, not just the UI)
- **Donate to a project** via an AJAX modal with a simulated realistic
  payment flow:
  1. Enter/select a donation amount (with quick-select presets)
  2. Choose a payment method: Visa/Mastercard, Vodafone Cash, or Mobile
     Wallet — each with its own input fields and basic client-side
     validation (card number formatting, expiry format, Egyptian phone
     format for wallets)
  3. A simulated "Verifying payment..." processing step
  4. Confirmation, with the raised amount and progress bar **updating live
     without a page reload**

### Homepage
- Hero section with a photo showcase.
- Slider highlighting the **5 highest-rated, currently running** projects.
- **Latest 5** projects listing.
- **Latest 5 featured** projects (curated/selected by admins).
- Full list of categories, each linking to a dedicated page showing only
  that category's projects.
- **Search bar** allowing users to search projects by title or by tag.

### AI Chatbot
- A floating chat widget available across the whole site.
- Powered by **Google Gemini** (`google-genai` SDK) using **function
  calling / tool use** — the model decides on its own when it needs to
  query real platform data rather than guessing.
- Tools available to the chatbot:
  - Top donated projects
  - Lowest donated projects
  - Top rated projects
  - Overall platform statistics (total projects, total raised, total
    donors, total categories)
  - Search projects by keyword
  - List projects by category
  - List all categories
  - **The logged-in user's own info**: name, email, country, their
    projects, and their donation history — securely scoped to the
    authenticated session (`request.user`), never trusting anything typed
    in the chat itself as an identity claim.
- Answers in whichever language the user writes in (Arabic or English).

### Admin Panel
- Custom-branded admin interface via `django-jazzmin` (themed navbar,
  sidebar, and dashboard, distinct from Django's default black admin).
- Custom dashboard homepage with:
  - Stat cards: total users, total projects, total donations raised
  - A bar chart of projects per category (Chart.js)
- Users split into two separate admin sections via proxy models:
  **Regular Users** and **Admin Users**.
- Full moderation tools for categories (mark featured), projects, reports
  (mark resolved), and contact messages (mark read).

### Contact Page
- A contact form (name, email, subject, message).
- Submissions are saved to the database and visible/manageable from the
  admin panel.
- The user automatically receives a confirmation email acknowledging their
  message was received (not an automated reply to the question itself —
  a human still needs to respond from the saved message).

### Site-wide UI/UX
- Custom visual identity: dark green + gold color palette, Cairo + Inter
  fonts, pill-shaped buttons, rounded cards.
- Animated hero sections, hover effects on project cards, scroll-reveal
  animations, and a tilted "photo fan" gallery effect.
- Site-wide **navbar** and **footer** present on every page.
- **Auto-dismissing notifications**: success/error messages fade out and
  disappear automatically after 5 seconds.
- **RTL (Arabic) support** *(in progress)*.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5 |
| Database | **SQLite** (development) |
| Auth | django-allauth (email + Facebook + Twitter/X) |
| Tags | django-taggit |
| Admin theme | django-jazzmin |
| AI Chatbot | Google Gemini (`google-genai`) with function calling |
| Frontend | Django Templates, Bootstrap 5, vanilla CSS/JS |
| Image handling | Pillow, Cropper.js (client-side cropping) |

> **Note:** the project currently runs on SQLite for local development.
> PostgreSQL is recommended before any production deployment, but is not
> yet configured.

---

##  Project Structure

```
egycrowd/
├── config/
│   ├── settings/
│   │   ├── base.py       # shared settings
│   │   └── dev.py        # local development
│   └── urls.py
├── apps/
│   ├── accounts/          # custom User model, auth, profile
│   ├── projects/          # categories, projects, images, tags
│   ├── donations/         # donation flow (simulated payment)
│   ├── interactions/      # comments, replies, ratings, reports
│   ├── core/               # homepage, contact page, admin dashboard stats
│   └── chatbot/            # AI assistant (Gemini + tool calling)
├── templates/
├── static/
├── media/                  # user-uploaded images (not committed)
├── db.sqlite3              # local database (not committed)
├── .env                    # secrets (not committed — see below)
├── requirements.txt
└── manage.py
```

---

##  Getting Started

### 1. Clone and set up the environment

```bash
git clone <repo-url>
cd egycrowd
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key
```

> Get a free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

### 3. Run migrations and start the server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000` — and `/admin/` to add categories and mark
projects as featured.

---

##  Email (development mode)

Activation, password-reset, and contact-confirmation emails are printed to
the console during development (`EMAIL_BACKEND = console`). A real SMTP
provider should replace this before any production deployment.

---

##  Currently in progress

- Facebook Login
- Twitter/X Login
- Arabic / RTL support

##  Possible next steps

- Migrate from SQLite to PostgreSQL for production
- Real payment gateway integration (currently a simulated/sandbox flow)
- Advanced filtering & sorting on the project listing page
- Full responsive design audit across all breakpoints
- Automated test suite
- Production deployment

---

##  Team

Built as a graduation/competition project by:
- **Fatma Shehtat Ewas**
- **Mohamed Ebrahim Salem**
- **Abdelrahman Hassany Abdlelmaged Qenawy**

---

##  License

This project was built for educational purposes.
