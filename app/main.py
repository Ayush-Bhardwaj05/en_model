# import streamlit as st
# import pickle
# import numpy as np
# import pandas as pd
# import plotly.graph_objects as go

# # Function to load and preprocess the data
# def get_clean_data():
#     data = pd.read_csv("data/data.csv")
#     # Dropping unnecessary columns
#     data = data.drop(['Unnamed: 32', 'id'], axis=1)
#     # Encoding diagnosis column: Malignant ('M') as 1, Benign ('B') as 0
#     data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
#     return data

# # Function to create the sidebar for user input
# def add_sidebar():
#     st.sidebar.header("Cell Nuclei Measurements")
#     data = get_clean_data()

#     # List of features for sliders with corresponding column names
#     slider_labels = [
#         ("Radius (mean)", "radius_mean"),
#         ("Texture (mean)", "texture_mean"),
#         ("Perimeter (mean)", "perimeter_mean"),
#         ("Area (mean)", "area_mean"),
#         ("Smoothness (mean)", "smoothness_mean"),
#         ("Compactness (mean)", "compactness_mean"),
#         ("Concavity (mean)", "concavity_mean"),
#         ("Concave points (mean)", "concave points_mean"),
#         ("Symmetry (mean)", "symmetry_mean"),
#         ("Fractal dimension (mean)", "fractal_dimension_mean"),
#         ("Radius (se)", "radius_se"),
#         ("Texture (se)", "texture_se"),
#         ("Perimeter (se)", "perimeter_se"),
#         ("Area (se)", "area_se"),
#         ("Smoothness (se)", "smoothness_se"),
#         ("Compactness (se)", "compactness_se"),
#         ("Concavity (se)", "concavity_se"),
#         ("Concave points (se)", "concave points_se"),
#         ("Symmetry (se)", "symmetry_se"),
#         ("Fractal dimension (se)", "fractal_dimension_se"),
#         ("Radius (worst)", "radius_worst"),
#         ("Texture (worst)", "texture_worst"),
#         ("Perimeter (worst)", "perimeter_worst"),
#         ("Area (worst)", "area_worst"),
#         ("Smoothness (worst)", "smoothness_worst"),
#         ("Compactness (worst)", "compactness_worst"),
#         ("Concavity (worst)", "concavity_worst"),
#         ("Concave points (worst)", "concave points_worst"),
#         ("Symmetry (worst)", "symmetry_worst"),
#         ("Fractal dimension (worst)", "fractal_dimension_worst"),
#     ]

#     # Collect user input via sliders
#     input_dict = {}
#     for label, key in slider_labels:
#         input_dict[key] = st.sidebar.slider(
#             label,
#             min_value=float(0),
#             max_value=float(data[key].max()),
#             value=float(data[key].mean())
#         )
#     return input_dict

# # Function to scale the user inputs to a 0-1 range
# def get_scaled_values(input_dict):
#     data = get_clean_data()
#     X = data.drop(['diagnosis'], axis=1)

#     # Normalize inputs using min-max scaling
#     scaled_dict = {}
#     for key, value in input_dict.items():
#         max_val = X[key].max()
#         min_val = X[key].min()
#         scaled_value = (value - min_val) / (max_val - min_val)
#         scaled_dict[key] = scaled_value
#     return scaled_dict

# # Function to generate a radar chart for visualization
# def get_radar_chart(input_data):
#     input_data = get_scaled_values(input_data)
#     categories = ['Radius', 'Texture', 'Perimeter', 'Area',
#                   'Smoothness', 'Compactness',
#                   'Concavity', 'Concave Points',
#                   'Symmetry', 'Fractal Dimension']

#     fig = go.Figure()

#     # Add traces for mean, standard error, and worst values
#     fig.add_trace(go.Scatterpolar(
#         r=[input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
#            input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
#            input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
#            input_data['fractal_dimension_mean']],
#         theta=categories,
#         fill='toself',
#         name='Mean Value'
#     ))
#     fig.add_trace(go.Scatterpolar(
#         r=[input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'], input_data['area_se'],
#            input_data['smoothness_se'], input_data['compactness_se'], input_data['concavity_se'],
#            input_data['concave points_se'], input_data['symmetry_se'], input_data['fractal_dimension_se']],
#         theta=categories,
#         fill='toself',
#         name='Standard Error'
#     ))
#     fig.add_trace(go.Scatterpolar(
#         r=[input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
#            input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
#            input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
#            input_data['fractal_dimension_worst']],
#         theta=categories,
#         fill='toself',
#         name='Worst Value'
#     ))

#     # Customize layout for radar chart
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 1]
#             )),
#         showlegend=True
#     )
#     return fig

# # Function to make predictions and display results
# def add_predictions(input_data):
#     # Load the ensemble model, scaler, and PCA transformer
#     model = pickle.load(open("model/ensemble_model.pkl", "rb"))
#     scaler = pickle.load(open("model/scaler.pkl", "rb"))
#     pca = pickle.load(open("model/pca.pkl", "rb"))

#     # Transform user input for prediction
#     input_array = np.array(list(input_data.values())).reshape(1, -1)
#     input_array_scaled = scaler.transform(input_array)

#     # Apply PCA transformation
#     input_array_pca = pca.transform(input_array_scaled)

#     # Make predictions with the ensemble model
#     ensemble_pred = model.predict(input_array_pca)
#     ensemble_probabilities = model.predict_proba(input_array_pca)

#     # Get probabilities from individual models in the ensemble
#     individual_probs = []
#     for model_instance in model.estimators_:
#         prob = model_instance.predict_proba(input_array_pca)
#         individual_probs.append(prob)

#     # Print individual model probabilities (for debugging or further analysis)
#     print("Individual model probabilities:")
#     for i, prob in enumerate(individual_probs):
#         print(f"Model {i + 1} - Benign Probability: {prob[0][0]:.4f} | Malignant Probability: {prob[0][1]:.4f}")

#     # Display results in Streamlit
#     st.subheader("Cell cluster prediction")
#     if ensemble_pred[0] == 0:
#         st.write("<span class='diagnosis benign'>Benign</span>", unsafe_allow_html=True)
#     else:
#         st.write("<span class='diagnosis malignant'>Malignant</span>", unsafe_allow_html=True)

#     st.write(f"Probability of being benign: {ensemble_probabilities[0][0]:.4f}")
#     st.write(f"Probability of being malignant: {ensemble_probabilities[0][1]:.4f}")

# # Main function to structure the app
# def main():
#     st.set_page_config(page_title="Breast Cancer Predictor", layout="wide", initial_sidebar_state="expanded")
#     with open("assets/style.css") as f:
#         st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

#     input_data = add_sidebar()

#     # Display title and description
#     st.title("Breast Cancer Predictor")
#     st.write("This project uses Machine Learning to predict whether a tumor is benign or malignant.")

#     # Split layout into columns
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         radar_chart = get_radar_chart(input_data)
#         st.plotly_chart(radar_chart)
#     with col2:
#         add_predictions(input_data)

# if __name__ == '__main__':
#     main()

import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

# Function to load and preprocess the data
def get_clean_data():
    data_path = os.path.join(os.getcwd(), "data", "data.csv")
    data = pd.read_csv(data_path)
    data = data.drop(['Unnamed: 32', 'id'], axis=1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    return data

# Function to create the sidebar for user input
def add_sidebar():
    st.sidebar.header("Cell Nuclei Measurements")
    data = get_clean_data()

    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}
    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(
            label,
            min_value=float(0),
            max_value=float(data[key].max()),
            value=float(data[key].mean())
        )
    return input_dict

# Function to scale user inputs
def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data.drop(['diagnosis'], axis=1)

    scaled_dict = {}
    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value
    return scaled_dict

# Radar chart generation
def get_radar_chart(input_data):
    input_data = get_scaled_values(input_data)
    categories = ['Radius', 'Texture', 'Perimeter', 'Area',
                  'Smoothness', 'Compactness',
                  'Concavity', 'Concave Points',
                  'Symmetry', 'Fractal Dimension']

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
           input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
           input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
           input_data['fractal_dimension_mean']],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))
    return fig

# Prediction function
def add_predictions(input_data):
    model_path = os.path.join(os.getcwd(), "model", "ensemble_model.pkl")
    scaler_path = os.path.join(os.getcwd(), "model", "scaler.pkl")
    pca_path = os.path.join(os.getcwd(), "model", "pca.pkl")

    model = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
    pca = pickle.load(open(pca_path, "rb"))

    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)
    input_array_pca = pca.transform(input_array_scaled)

    ensemble_pred = model.predict(input_array_pca)
    ensemble_probabilities = model.predict_proba(input_array_pca)

    st.subheader("Cell cluster prediction")
    if ensemble_pred[0] == 0:
        st.write("Benign")
    else:
        st.write("Malignant")

    st.write(f"Probability of being benign: {ensemble_probabilities[0][0]:.4f}")
    st.write(f"Probability of being malignant: {ensemble_probabilities[0][1]:.4f}")

# Main app function
def main():
    st.set_page_config(page_title="Breast Cancer Predictor", layout="wide")
    input_data = add_sidebar()

    st.title("Breast Cancer Predictor")
    st.write("This project uses Machine Learning to predict whether a tumor is benign or malignant.")

    col1, col2 = st.columns([4, 1])
    with col1:
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart)
    with col2:
        add_predictions(input_data)

if __name__ == '__main__':
    main()
