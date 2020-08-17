import streamlit as st
import pandas as pd
import awesome_streamlit as ast

@st.cache
def load_data():
    raw = pd.read_csv("data/insurance.csv")
    proc = pd.read_csv("data/insurance_preprocessed.csv")
    proc.charges = (proc.charges > 10000).astype('int')
    cols = ['age', 'bmi', 'children', 'sex', 'smoker', 'region_northeast',
    'region_northwest', 'region_southeast', 'region_southwest', 'charges']
    proc = proc[cols]
    return raw, proc

def write():

    with st.spinner("Loading Preprocessing ..."):
        raw, proc = load_data()

        st.title('Data preprocessing')

        st.write("Original dataset (derived from [Kaggle](https://www.kaggle.com/mirichoi0218/insurance)):")
        st.write(raw)

        st.write("""
        Conducted preprocessing steps:
        - Discretize `charges` variable at the threshold of $10,000 to enable
          binary classification
        - One-hot encode `region` variable
        - Recode `sex` variable: 0 = female, 1 = male
        - Recode `smoker` variable: 0 = no, 1 = yes
        """)

        st.write(f"Dataset used for training models ({proc.shape[0]} examples, {proc.shape[1] - 1} features):")
        st.write(proc)

