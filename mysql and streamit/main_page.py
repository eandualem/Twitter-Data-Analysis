import page1
import page2
import streamlit as st
PAGES = {
    "Basics": page1,
    "Advanced": page2
}
selection = st.sidebar.radio("Go to page", list(PAGES.keys()))
page = PAGES[selection]
page.app()
