# payment_config.py - Stripe Configuration

# ============================================
# STRIPE SETTINGS (TEST MODE)
# ============================================

# Get your test keys from: https://dashboard.stripe.com/test/apikeys
# For production, use environment variables
STRIPE_PUBLISHABLE_KEY = "pk_test_..."  # ← Replace with your publishable key
STRIPE_SECRET_KEY = "sk_test_..."      # ← Replace with your secret key

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

# ============================================
# HOW TO GET STRIPE KEYS
# ============================================
# 1. Go to: https://dashboard.stripe.com/test/apikeys
# 2. Copy your Publishable key (starts with pk_test_)
# 3. Copy your Secret key (starts with sk_test_)
# 4. Paste them above