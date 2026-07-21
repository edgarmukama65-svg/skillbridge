# payment.py - Stripe Payment Integration (Simplified)

import streamlit as st
import stripe
from payment_config import *
from database import get_user_by_id

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY

# ============================================
# PAYMENT FUNCTIONS
# ============================================

def create_checkout_session(plan_id, user_id, email):
    """
    Create a Stripe checkout session
    Returns: checkout_url or None
    """
    try:
        plan = PLANS.get(plan_id)
        if not plan:
            return None, "Plan not found"
        
        # Get user's name
        user = get_user_by_id(user_id)
        user_name = user[1] if user else "User"
        
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=email,
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"SkillBridge {plan['name']} Plan",
                        "description": "Unlock premium features to accelerate your career",
                    },
                    "unit_amount": plan['price'],
                    "recurring": {
                        "interval": "month",
                    },
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url="http://localhost:8501?payment_success=true&session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8501?payment_canceled=true",
            metadata={
                "user_id": user_id,
                "user_name": user_name,
                "plan": plan_id
            }
        )
        
        return session.url, None
        
    except stripe.error.StripeError as e:
        print(f"❌ Stripe Error: {e}")
        return None, str(e)

def get_session_status(session_id):
    """
    Check the status of a payment session
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.status, session.payment_status
    except Exception as e:
        return None, str(e)

# ============================================
# PAYMENT UI - SIMPLIFIED
# ============================================

def show_payment_page():
    """
    Display the payment page
    """
    
    # Check if user is logged in
    if not st.session_state.user_id:
        st.warning("⚠️ Please login first to upgrade your plan")
        return
    
    # Get user info
    user = get_user_by_id(st.session_state.user_id)
    if not user:
        st.error("❌ User not found")
        return
    
    user_name = user[1]
    user_email = user[2]
    user_role = user[3]
    
    # Show current plan
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 15px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
        <h3 style="color: white; margin: 0;">Current Plan: <strong>{user_role}</strong></h3>
        <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">{user_name} ({user_email})</p>
    </div>
    """, unsafe_allow_html=True)
    
    # If already Pro or Enterprise
    if user_role in ["Pro", "Enterprise"]:
        st.success(f"✅ You are already on the **{user_role}** plan!")
        return
    
    # Show pricing plans
    st.subheader("📊 Choose Your Plan")
    
    # Create columns
    col1, col2, col3 = st.columns(3)
    
    # ============================================
    # FREE PLAN
    # ============================================
    with col1:
        st.markdown("""
        <div style="border: 2px solid #e0e0e0; border-radius: 15px; padding: 20px; text-align: center; background: white; height: 100%;">
            <h2 style="color: #333; margin-bottom: 5px;">Free</h2>
            <h1 style="font-size: 36px; color: #333; margin: 0;">$0</h1>
            <p style="color: #888; margin-top: 0;">/month</p>
            <hr>
            <div style="text-align: left; padding: 0 5px;">
                <p style="margin: 5px 0;">✅ 5 Analyses/month</p>
                <p style="margin: 5px 0;">✅ Basic ATS Score</p>
                <p style="margin: 5px 0;">✅ Community Support</p>
            </div>
            <br>
            <div style="background: #4CAF50; color: white; padding: 8px; border-radius: 25px; font-weight: bold; font-size: 14px;">
                Current Plan
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # PRO PLAN
    # ============================================
    with col2:
        st.markdown("""
        <div style="border: 3px solid #667eea; border-radius: 15px; padding: 20px; text-align: center; background: #f8f9ff; height: 100%;">
            <h2 style="color: #667eea; margin-bottom: 5px;">⭐ Pro</h2>
            <h1 style="font-size: 36px; color: #667eea; margin: 0;">$9.99</h1>
            <p style="color: #888; margin-top: 0;">/month</p>
            <hr>
            <div style="text-align: left; padding: 0 5px;">
                <p style="margin: 5px 0;">✅ Unlimited Analyses</p>
                <p style="margin: 5px 0;">✅ Advanced AI Analysis</p>
                <p style="margin: 5px 0;">✅ Detailed Reports</p>
                <p style="margin: 5px 0;">✅ Email Support</p>
                <p style="margin: 5px 0;">✅ Resume Builder</p>
            </div>
            <br>
        </div>
        """, unsafe_allow_html=True)
        
        # Pro button
        if st.button("⭐ Upgrade to Pro", use_container_width=True, key="upgrade_pro"):
            with st.spinner("Redirecting to payment..."):
                url, error = create_checkout_session("pro", st.session_state.user_id, user_email)
                if url:
                    st.markdown(f'<meta http-equiv="refresh" content="0;URL={url}">', unsafe_allow_html=True)
                    st.success("Redirecting to payment...")
                else:
                    st.error(f"❌ {error}")
    
    # ============================================
    # ENTERPRISE PLAN
    # ============================================
    with col3:
        st.markdown("""
        <div style="border: 2px solid #ff6b6b; border-radius: 15px; padding: 20px; text-align: center; background: #fff5f5; height: 100%;">
            <h2 style="color: #ff6b6b; margin-bottom: 5px;">🏢 Enterprise</h2>
            <h1 style="font-size: 36px; color: #ff6b6b; margin: 0;">$49.99</h1>
            <p style="color: #888; margin-top: 0;">/month</p>
            <hr>
            <div style="text-align: left; padding: 0 5px;">
                <p style="margin: 5px 0;">✅ Team Management</p>
                <p style="margin: 5px 0;">✅ Career Coach Access</p>
                <p style="margin: 5px 0;">✅ API Access</p>
                <p style="margin: 5px 0;">✅ Dedicated Support</p>
                <p style="margin: 5px 0;">✅ Custom Solutions</p>
            </div>
            <br>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📧 Contact Sales", use_container_width=True, key="contact_sales"):
            st.info("Email: sales@skillbridge.com")
    
    # ============================================
    # TEST CARD INFO
    # ============================================
    st.divider()
    
    with st.expander("💳 Test Card Numbers", expanded=True):
        st.markdown("""
        **Test Mode** - No real payments will be processed
        
        | Card Number | Result |
        | :--- | :--- |
        | `4242 4242 4242 4242` | ✅ Payment Success |
        | `4000 0000 0000 0002` | ❌ Payment Declined |
        | `4000 0025 0000 3155` | 🔄 3D Secure Required |
        
        **Any future expiry date and any 3-digit CVC will work**
        """)

def handle_payment_callback():
    """
    Handle payment success/cancel callbacks
    """
    query_params = st.query_params
    
    if "payment_success" in query_params:
        session_id = query_params.get("session_id", "")
        if session_id:
            status, payment_status = get_session_status(session_id)
            if status == "complete" and payment_status == "paid":
                st.success("🎉 **Payment Successful!** You've been upgraded to Pro!")
                st.balloons()
                if st.session_state.user_id:
                    from database import update_user_role_admin
                    update_user_role_admin(st.session_state.user_id, "Pro")
                st.info("✅ Your account has been upgraded. Enjoy the Pro features!")
            else:
                st.info("⏳ Payment is being processed...")
    
    elif "payment_canceled" in query_params:
        st.warning("⚠️ Payment was canceled. You can try again anytime.")

# ============================================
# TEST FUNCTIONS
# ============================================

def test_stripe_connection():
    """
    Test Stripe API connection
    """
    try:
        stripe.Product.list(limit=1)
        print("✅ Stripe connection successful!")
        return True
    except Exception as e:
        print(f"❌ Stripe connection failed: {e}")
        return False

if __name__ == "__main__":
    test_stripe_connection()