import streamlit as st
import awesome_streamlit as ast

import src.pages.home
import src.pages.preprocessing
import src.pages.eda

ast.core.services.other.set_logging_format()

PAGES = {
    "Home": src.pages.home,
    "Preprocessing": src.pages.preprocessing,
    "Explorative data analysis": src.pages.eda,
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)

if __name__ == "__main__":
    main()
