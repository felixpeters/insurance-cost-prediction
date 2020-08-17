import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import awesome_streamlit as ast

@st.cache
def load_data():
    raw = pd.read_csv("data/insurance.csv")
    raw['charges_bin']= (raw.charges > 10000)
    raw.sex = raw.sex.astype('category')
    raw.age = raw.age.astype('int')
    raw.smoker = raw.smoker.astype('category')
    raw.region = raw.region.astype('category')
    return raw

@st.cache
def filter_data(copy, sex, age, bmi, children, smoker, regions):
    # filter by sex
    if sex == "Male":
        copy = copy[copy.sex == 'male']
    if sex == "Female":
        copy = copy[copy.sex == 'female']

    if smoker == "Smoker":
        copy = copy[copy.smoker == 'yes']
    if smoker == "Non-smoker":
        copy = copy[copy.smoker == 'no']

    if len(regions) > 0:
        regions = [r.lower() for r in regions]
        copy = copy[copy['region'].isin(regions)]
    # filter by age
    copy = copy[(copy.age >= age[0]) & (copy.age <= age[1])]
    copy = copy[(copy.bmi >= bmi[0]) & (copy.bmi <= bmi[1])]
    copy = copy[(copy.children >= children[0]) & (copy.children <= children[1])]
    return copy

def write():

    with st.spinner("Loading Preprocessing ..."):
        raw = load_data()
        copy = raw.copy()

        st.title('Explorative data analysis')

        st.write('## Distribution of target variable')

        sex = st.radio("Filter by sex", ("All", "Male", "Female"))
        smoker = st.radio("Filter by smoker", ("All", "Smoker", "Non-smoker"))
        regions = st.multiselect("Filter by region", ("Northeast", "Northwest", "Southeast", "Southwest"))

        min_age, max_age = int(np.min(raw.age)), int(np.max(raw.age))
        age = st.slider(
                "Filter by age",
                min_value=min_age,
                max_value=max_age,
                value=[min_age, max_age],
        )

        min_bmi, max_bmi = int(np.min(raw.bmi)), int(np.max(raw.bmi))
        bmi = st.slider(
                "Filter by bmi",
                min_value=min_bmi,
                max_value=max_bmi,
                value=[min_bmi, max_bmi],
        )

        min_children, max_children = int(np.min(raw.children)), int(np.max(raw.children))
        children = st.slider(
                "Filter by children",
                min_value=min_children,
                max_value=max_children,
                value=[min_children, max_children],
        )

        copy = filter_data(copy, sex, age, bmi, children, smoker, regions)

        st.write(f'Target variable distribution based on {len(copy)} selected examples:')

        plt.hist(copy.charges, bins=20)
        plt.xlabel('Insurance cost')
        plt.ylabel('Frequency')
        st.pyplot()

        st.write('## Distribution of input variables')

        st.write('### Continuous variables')

        plt.hist(raw.age, bins=20)
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        st.pyplot()

        plt.hist(raw.bmi, bins=20)
        plt.xlabel('Body mass index')
        plt.ylabel('Frequency')
        st.pyplot()

        st.write('### Categorical variables')

        plt.bar(raw.sex.cat.categories, raw.sex.value_counts(sort=False))
        plt.xlabel('Sex')
        plt.ylabel('Frequency')
        st.pyplot()

        plt.hist(raw.children, bins=5)
        plt.xlabel('Number of children')
        plt.ylabel('Frequency')
        st.pyplot()

        plt.bar(raw.smoker.cat.categories, raw.smoker.value_counts(sort=False))
        plt.xlabel('Smoker')
        plt.ylabel('Frequency')
        st.pyplot()

        plt.bar(raw.region.cat.categories, raw.region.value_counts(sort=False))
        plt.xlabel('Region')
        plt.ylabel('Frequency')
        st.pyplot()
