import streamlit as st
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

# Load data
@st.cache_data
def load_data():
    data = pd.read_excel("rating_data_modified.xlsx", index_col=9)
    return data

data = load_data()

# Standardization function
def standardize(row):
    new_row = (row - row.mean()) / (row.max() - row.min())
    return new_row

# Create correlation matrix
@st.cache_resource
def create_corr_matrix():
    df_std = data.apply(standardize).T
    sparse_df = sparse.csr_matrix(df_std.values)
    corrMatrix = pd.DataFrame(cosine_similarity(sparse_df), index=data.columns, columns=data.columns)
    return corrMatrix

corrMatrix = create_corr_matrix()

# Recommendation function
def get_similar(item_name, rating):
    similar_score = corrMatrix[item_name] * (rating - 1.5)
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score

# Streamlit UI
st.title("Coffee Product Recommendation System")

# Product selection
product = st.selectbox("Select a product:", data.columns)

# Rating selection
rating = st.slider("Rate the product:", 1, 5, 3)

if st.button("Get Recommendations"):
    recommendations = get_similar(product, rating)
    
    st.subheader(f"Top Recommendations based on {product} (rated {rating}):")
    
    # Display top 5 recommendations
    for i, (prod, score) in enumerate(recommendations.head(6).items(), 1):
        if prod != product:  # Skip the selected product
            st.write(f"{i}. {prod}: {score:.4f}")

    # Visualize recommendations
    st.subheader("Recommendation Scores Visualization")
    chart_data = recommendations.head(11).drop(product, errors='ignore')
    st.bar_chart(chart_data)

st.sidebar.header("About")
st.sidebar.info("This recommendation system suggests coffee products based on the similarity to your selected product and rating. It uses collaborative filtering and cosine similarity to generate personalized recommendations.")