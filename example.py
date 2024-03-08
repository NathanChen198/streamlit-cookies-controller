# Author    : Nathan Chen
# Date      : 08-Mar-2024


import streamlit as st
from datetime import datetime, timedelta
from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer

st.set_page_config('Cookie Controller Example', '🍪', layout='wide')

RemoveEmptyElementContainer()

# Count how many time the script run
if 'count' not in st.session_state:
    st.session_state['count'] = 0
st.session_state['count'] += 1
count = st.session_state['count']

# declare the cookie controller
controller = CookieController()
brf, test, aft = st.columns([1, 1, 1])

tests = [
    "Set Cookie",
    "Get Cookie",
    "Remove Cookie",
    "Auto Renewal",
]

with brf:
    st.markdown("### Streamlit session state (Before)")
    st.write(st.session_state)

with test:
    selection = st.selectbox("Test", options=tests)
    st.divider()

    if selection == tests[0]:
        st.markdown("### Test set cookie")
        name = st.text_input("Cookie name")
        value = st.text_input("Cookie value")
        set = st.button("Set")
        if set:
            controller.set(name, value)
    elif selection == tests[1]:
        st.markdown("### Test get cookie")
        name = st.text_input("Cookie name")
        get = st.button("Get")
        if get:
            value = controller.get(name)
            st.write(value)
    elif selection == tests[2]:
        st.markdown("### Test remove cookie")
        name = st.text_input("Cookie name")
        remove = st.button("Remove")
        if remove:
            controller.remove(name)
    elif selection == tests[3]:
        # simulate auto authentication renewal
        st.markdown("### Test auto renew cookie expiry")
        name = st.text_input("Cookie name")
        expiry_date = datetime.now() + timedelta(days=1)
        controller.set(name, {
            "value": f"value_{count}",
            "expiry_date": expiry_date.isoformat()
        })
        autorenew = st.button("Auto renew")
        st.write(autorenew)

with aft:    
    st.markdown("### Streamlit session state (After)")
    st.write(st.session_state)