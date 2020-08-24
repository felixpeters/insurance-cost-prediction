from joblib import load
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.metrics import roc_auc_score, plot_roc_curve
import matplotlib.pyplot as plt
import awesome_streamlit as ast

@st.cache
def load_data():
    data = pd.read_csv("data/insurance_preprocessed.csv")
    data['charges_bin']= (data.charges > 10000)
    return data


@st.cache(allow_output_mutation=True)
def load_model():
    return load("models/random_forest.joblib")

@st.cache
def filter_data(copy, sex, age, bmi, children, smoker, regions):
    # filter by sex
    if sex == "Male":
        copy = copy[copy.sex == 1]
    if sex == "Female":
        copy = copy[copy.sex == 0]

    if smoker == "Smoker":
        copy = copy[copy.smoker == 1]
    if smoker == "Non-smoker":
        copy = copy[copy.smoker == 0]

    if len(regions) > 0:
        result = pd.DataFrame(columns=copy.columns)
        for region in regions:
            region = region.lower()
            region_results = copy[copy[f'region_{region}'] == 1]
            result = result.append(region_results)
        copy = result
    # filter by age
    copy = copy[(copy.age >= age[0]) & (copy.age <= age[1])]
    copy = copy[(copy.bmi >= bmi[0]) & (copy.bmi <= bmi[1])]
    copy = copy[(copy.children >= children[0]) & (copy.children <= children[1])]
    return copy

@st.cache
def split_data(df):
    X = df.drop(columns=['charges', 'charges_bin'])
    y = df['charges_bin'].astype('int')
    return X, y

def write():
    with st.spinner("Loading Model evaluation ..."):
        st.title("Model evaluation")

        model = load_model()
        data = load_data()
        copy = data.copy()

        st.write('## 1. View model information')

        st.write('''
                **Task:** Predict whether subject will incur insurance cost
                higher than $10,000\n
                **Model:** Random forest\n
                **Hyperparameters:**
                - Number of trees: 100
                - Minimum samples for split: 2
                - Minimum samples per leaf: 1
                - Maximum number of features per tree: 3
                - Maximum depth: None
                ''')

        st.write('## 2. Select subset of data')

        sex = st.radio("Filter by sex", ("All", "Male", "Female"))
        smoker = st.radio("Filter by smoker", ("All", "Smoker", "Non-smoker"))
        regions = st.multiselect("Filter by region", ("Northeast", "Northwest", "Southeast", "Southwest"))

        min_age, max_age = int(np.min(data.age)), int(np.max(data.age))
        age = st.slider(
                "Filter by age",
                min_value=min_age,
                max_value=max_age,
                value=[min_age, max_age],
        )

        min_bmi, max_bmi = int(np.min(data.bmi)), int(np.max(data.bmi))
        bmi = st.slider(
                "Filter by bmi",
                min_value=min_bmi,
                max_value=max_bmi,
                value=[min_bmi, max_bmi],
        )

        min_children, max_children = int(np.min(data.children)), int(np.max(data.children))
        children = st.slider(
                "Filter by children",
                min_value=min_children,
                max_value=max_children,
                value=[min_children, max_children],
        )

        copy = filter_data(copy, sex, age, bmi, children, smoker, regions)

        st.write(f'**{len(copy)} examples** were found based on your selection.')

        st.write('## 3. Examine model performance on subset')

        X, y = split_data(copy)
        preds = model.predict(X)
        probs = model.predict_proba(X)[:, 1]
        auc_score = roc_auc_score(y, probs)
        acc_score = model.score(X, y)

        st.write(f'**Accuracy:** {acc_score:.4f}')
        st.write(f'**ROC AUC Score:** {auc_score:.4f}')
        plot_roc_curve(model, X, y)
        plt.title('ROC curve for selected subset')
        st.pyplot()
