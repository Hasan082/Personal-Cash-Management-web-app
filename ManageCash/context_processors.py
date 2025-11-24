def site_info(request):
    """Provide site-wide information for templates.

    Available in templates as `SITE_NAME`, `SITE_DESCRIPTION`, `SUPPORT_EMAIL`,
    `COMPANY_NAME`, and `APP_VERSION`.
    """
    return {
        "SITE_NAME": "Personal Cash Manager",
        "SITE_DESCRIPTION": "A simple app to track personal income and expenses.",
        "SUPPORT_EMAIL": "support@example.com",
        "COMPANY_NAME": "Your Company",
        "APP_VERSION": "1.0.0",
    }
