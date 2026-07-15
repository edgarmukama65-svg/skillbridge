# payment.py - Stripe Integration

import streamlit as st
import stripe
import os

# ============================================
# STRIPE CONFIGURATION
# ============================================

# For testing, use test keys
# Get your keys from: https://dashboard.stripe.com/test/apikeys
STRIPE_PUBLISHABLE_KEY = "pk_test_your_test_key"  # CHANGE THIS
STRIPE_SECRET_KEY = "sk_test_your_test_key"      # CHANGE THIS

stripe.api_key = STRIPE_SECRET_KEY

# ============================================
# PRICING PLANS
# ============================================

PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "features": ["5 analyses/month", "Basic ATS Score", "Community Support"]
    },
    "pro": {
        "name": "Pro",
        "price": 999,  # $9.99 in cents
        "price_id": "price_your_price_id",  # Create this in Stripe
        "features": ["Unlimited analyses", "Advanced AI", "Detailed Reports", "Email Support"]
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 4999,  # $49.99 in cents
        "price_id": "price_your_price_id",  # Create this in Stripe
        "features": ["Team Management", "API Access", "Dedicated Support", "Custom Solutions"]
    }
}

# ============================================
# PAYMENT FUNCTIONS
# ============================================

def create_checkout_session(price_id, user_id, email):
    """Create a Stripe checkout session"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=email,
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url="http://localhost:8501?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8501?canceled=true",
            metadata={
                "user_id": user_id
            }
        )
        return session.url, None
    except Exception as e:
        return None, str(e)

def create_payment_intent(amount, currency="usd"):
    """Create a payment intent for one-time payments"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )
        return intent.client_secret, None
    except Exception as e:
        return None, str(e)

# ============================================
# PAYMENT UI
# ============================================

def show_payment_ui():
    """Display payment UI"""
    
    if not st.session_state.user_id:
        st.warning("⚠️ Please login first to subscribe")
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-bottom: 30px;">
        <h1 style="color: white;">💳 Upgrade Your Plan</h1>
        <p style="color: rgba(255,255,255,0.9);">Get access to premium features and accelerate your career</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="border: 2px solid #ddd; border-radius: 20px; padding: 30px; text-align: center; background: white;">
            <h2>Free</h2>
            <h1 style="font-size: 40px;">$0</h1>
            <p style="color: #666;">/month</p>
            <br>
            <p>✅ 5 Analyses/month</p>
            <p>✅ Basic ATS Score</p>
            <p>✅ Community Support</p>
            <br>
            <button style="padding: 10px 40px; background: #4CAF50; color: white; border: none; border-radius: 30px; font-size: 16px;">Current Plan</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="border: 3px solid #667eea; border-radius: 20px; padding: 30px; text-align: center; background: #f8f9ff; box-shadow: 0 10px 30px rgba(102,126,234,0.3);">
            <h2>⭐ Pro</h2>
            <h1 style="font-size: 40px; color: #667eea;">$9.99</h1>
            <p style="color: #666;">/month</p>
            <br>
            <p>✅ Unlimited Analyses</p>
            <p>✅ Advanced AI Analysis</p>
            <p>✅ Detailed Reports</p>
            <p>✅ Email Support</p>
            <p>✅ Resume Builder</p>
            <br>
            <button style="padding: 10px 40px; background: #667eea; color: white; border: none; border-radius: 30px; font-size: 16px;">Subscribe Now</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="border: 2px solid #ddd; border-radius: 20px; padding: 30px; text-align: center; background: white;">
            <h2>🏢 Enterprise</h2>
            <h1 style="font-size: 40px;">$49.99</h1>
            <p style="color: #666;">/month</p>
            <br>
            <p>✅ Team Management</p>
            <p>✅ Career Coach Access</p>
            <p>✅ API Access</p>
            <p>✅ Dedicated Support</p>
            <p>✅ Custom Solutions</p>
            <br>
            <button style="padding: 10px 40px; background: #ff6b6b; color: white; border: none; border-radius: 30px; font-size: 16px;">Contact Sales</button>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.caption("💳 Payments are processed securely by Stripe")