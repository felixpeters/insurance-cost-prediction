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

@st.cache
def get_features(copy):
    features = copy.columns.tolist()
    if 'charges' in features:
        features.remove('charges')
    if 'charges_bin' in features:
        features.remove('charges_bin')
    return features

def write():

    with st.spinner("Loading Preprocessing ..."):
        raw = load_data()
        copy = raw.copy()

        st.title('Explorative data analysis')

        st.write('## 1. Select subset of data')

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

        st.write(f'**{len(copy)} examples** were found based on your selection.')

        st.write('## 2. Examine target variable distribution')

        plt.hist(copy.charges, bins=20)
        plt.xlabel('Insurance cost')
        plt.ylabel('Frequency')
        st.pyplot()

        st.write('## 3. Examine input variable distributions')

        features = get_features(copy)
        copy.children = copy.children.astype('category')
        feature = st.selectbox('Choose an input variable', features)

        if copy[feature].dtype.name == 'category':
            plt.bar(copy[feature].cat.categories, copy[feature].value_counts(sort=False))
            plt.xlabel(feature)
            plt.ylabel('frequency')
            st.pyplot()
        else:
            plt.hist(copy[feature], bins=20)
            plt.xlabel(feature)
            plt.ylabel('frequency')
            st.pyplot()
