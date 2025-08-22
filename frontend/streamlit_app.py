import streamlit as st
import requests

st.set_page_config(page_title="Dynamic Risk-based 2FA — Demo")
st.title('Dynamic Risk-based 2FA — Demo')

API = st.text_input('Backend URL', 'http://localhost:8000')

username = st.text_input('Username')
password = st.text_input('Password', type='password')
lat = st.number_input('Latitude', value=12.9716, format='%f')
lon = st.number_input('Longitude', value=77.5946, format='%f')

st.markdown("**Actions**")
col1, col2 = st.columns(2)

with col1:
    if st.button('Create demo user (alice)'):
        try:
            r = requests.post(API + '/create_demo_user', timeout=5)
            st.success(r.json())
        except Exception as e:
            st.error(f"Request failed: {e}")

with col2:
    if st.button('Login'):
        if not username or not password:
            st.warning("Enter username and password")
        else:
            payload = {
                'username': username,
                'password': password,
                'ip': '1.2.3.4',
                'user_agent': 'demo-agent',
                'lat': float(lat),
                'lon': float(lon),
                'timestamp': 0
            }
            try:
                r = requests.post(API + '/login', json=payload, timeout=5)
                if r.status_code != 200:
                    st.error(f"Error: {r.status_code} {r.text}")
                else:
                    data = r.json()
                    st.json(data)
                    if data.get('next_action') == 'send_otp':
                        otp = st.text_input('Enter OTP')
                        if st.button('Verify OTP'):
                            v = requests.post(API + '/verify_otp', json={'username': username, 'otp': otp})
                            if v.status_code == 200:
                                st.success(v.json())
                            else:
                                st.error(f"OTP verify failed: {v.status_code} {v.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
