# payment_config.py - Stripe Configuration

# ============================================
# STRIPE SETTINGS (TEST MODE)
# ============================================

# Your Stripe Test Keys from the dashboard
STRIPE_PUBLISHABLE_KEY = "pk_test_51Ttq5TCMxcX1Mn3B5yphIT6B00nFcetD5YsFL3rUw5Ikmo1H8IN7DrzB07hj3QuvIGD0gKMpIZwFoSeo5qXy1QNP0@poNc0Sgx"

STRIPE_SECRET_KEY = "sk_test_51Ttq5TCMxcX1Mn3BjnnowyIAnTKE1G995F1DjEpUMDQist81kDF5tBaQGQ1dELi5WevLvvi9y0JZBCZTnPMPm0@qmLAcPXf"

# ============================================
# PRICING PLANS
# ============================================

PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "features": [
            "5 analyses/month",
            "Basic ATS Score",
            "Community Support"
        ]
    },
    "pro": {
        "name": "Pro",
        "price": 999,  # $9.99 in cents
        "features": [
            "Unlimited analyses",
            "Advanced AI Analysis",
            "Detailed Reports",
            "Email Support",
            "Resume Builder"
        ]
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 4999,  # $49.99 in cents
        "features": [
            "Team Management",
            "Career Coach Access",
            "API Access",
            "Dedicated Support",
            "Custom Solutions"
        ]
    }
}