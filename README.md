Personal Cash Management
=======================

Brief
-----
A compact Django application for tracking personal income and expenses. It provides user authentication, simple CRUD for transactions, and a dashboard with aggregated totals and visualizations.

Key Features
------------
- User registration and authentication
- Add / edit / delete income and expense records
- Dashboard with totals, recent transactions and charts

Quick start
-----------
1. Create and activate a virtual environment:

	```bash
	python3 -m venv venv
	source venv/bin/activate
	```

2. Install dependencies and run migrations:

	```bash
	python3 -m pip install -r requirements.txt
	python3 manage.py migrate
	```

3. Start the development server:

	```bash
	python3 manage.py runserver
	```

Configuration notes
-------------------
- Set `DEBUG=False` and configure `ALLOWED_HOSTS` for production.
- Keep `SECRET_KEY` and other secrets out of source control (use environment variables).

Where to look
-------------
- Models: `ManageCash/models.py`
- Views: `ManageCash/views.py` (dashboard aggregation and context)
- Templates: `ManageCash/templates/pages/dashboard.html`
- Static JS: `hasan_wadp_19_ManageCash/static/js/dashboard.js`

Commands
--------
- System checks: `python3 manage.py check`
- Run tests: `python3 manage.py test`



