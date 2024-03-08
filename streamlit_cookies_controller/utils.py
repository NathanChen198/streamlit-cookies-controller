# Author    : Nathan Chen
# Date      : 08-Mar-2024


import streamlit as st

def RemoveEmptyElementContainer():
    st.markdown(
        f""" 
            <style>
                .element-container:has(iframe[height="0"]) {{ display: none; }}
            </style>
        """, unsafe_allow_html=True
    )
