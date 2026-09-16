# Import the required libraries
import streamlit as st
import pandas as pd
import plotly.express as px


# Set the Streamlit page configuration
st.set_page_config(
    page_title="Student Academic Risk Intelligence System",
    layout="wide",
    page_icon="🎓"
)


# Load the Maths dataset from the data folder
df = pd.read_csv("Maths.csv")


# Create Result based on the final grade (G3)
# G3 = 0 means Dropout
# G3 = 1 to 9 means Fail
# G3 = 10 to 20 means Pass
df["Result"] = df["G3"].apply(
    lambda x: "Dropout" if x == 0 else ("Fail" if 1 <= x <= 9 else "Pass")
)


# Calculate the final grade percentage
df["Percentage"] = (df["G3"] / 20) * 100


# Calculate average alcohol consumption
df["avg_alcohol"] = (df["Dalc"] + df["Walc"]) / 2


# Calculate average education level of both parents
df["parent_edu_avg"] = (df["Medu"] + df["Fedu"]) / 2


# Calculate the grade trend from G1 to G3
df["grade_trend"] = df["G3"] - df["G1"]


# Count the number of "yes" values across support columns
df["total_support"] = (
    df[["schoolsup", "famsup", "paid"]]
    .eq("yes")
    .sum(axis=1)
)


# Calculate the academic risk score
df["risk_score"] = (
    (df["failures"] * 2)
    + (df["absences"] / 10)
    + df["avg_alcohol"]
    - df["studytime"]
)


# Calculate the average of G1 and G2
df["g1_g2_avg"] = (df["G1"] + df["G2"]) / 2


# Display the main title of the dashboard
st.title("🎓 Student Academic Risk Intelligence System")


# Exclude dropout students for academic performance calculations
non_dropout_df = df[df["G3"] != 0]


# Calculate the class average G3 excluding dropouts
class_average_g3 = round(non_dropout_df["G3"].mean(), 2)


# Calculate the pass rate among non-dropout students
passed_students = (non_dropout_df["G3"] >= 10).sum()
total_non_dropout = len(non_dropout_df)

pass_rate = round(
    (passed_students / total_non_dropout) * 100,
    1
)


# Calculate the number of at-risk students
# At-risk students have G3 between 1 and 9
at_risk_count = (
    (df["G3"] >= 1) & (df["G3"] <= 9)
).sum()


# Create four KPI cards in one row
col1, col2, col3, col4 = st.columns(4)


# Card 1: Total number of students
with col1:
    st.metric("Total Students", len(df))


# Card 2: Average G3 excluding dropouts
with col2:
    st.metric("Class Average G3", class_average_g3)


# Card 3: Pass rate among non-dropout students
with col3:
    st.metric("Pass Rate %", f"{pass_rate}%")


# Card 4: Number of at-risk students
with col4:
    st.metric("At-Risk Count", at_risk_count)


# Add the Performance Charts section
st.subheader("📊 Performance Charts")


# Create two columns to display the charts side by side
col1, col2 = st.columns(2)


# Left chart: Study Time vs Final Grade
with col1:
    # Create an interactive scatter plot
    fig1 = px.scatter(
        df,
        x="studytime",
        y="G3",
        color="Result",
        hover_data=["absences", "G1", "G2"],
        title="Study Time vs Final Grade",
        color_discrete_map={
            "Pass": "green",
            "Fail": "red",
            "Dropout": "grey"
        }
    )

    # Display the scatter plot using the full column width
    st.plotly_chart(fig1, use_container_width=True)


# Right chart: Average G3 by Internet Access
with col2:
    # Calculate average G3 for each internet access group
    avg_g3_internet = (
        df.groupby("internet")["G3"]
        .mean()
        .reset_index()
    )

    # Create an interactive bar chart
    fig2 = px.bar(
        avg_g3_internet,
        x="internet",
        y="G3",
        color="internet",
        title="Average G3 by Internet Access"
    )

    # Display the bar chart using the full column width
    st.plotly_chart(fig2, use_container_width=True)

# Add the Student Analysis Table section
st.subheader("🚨 Student Analysis Table")


# Create a dropdown to filter students by their result
result_filter = st.selectbox(
    "Filter by Result",
    ["All", "Pass", "Fail", "Dropout"]
)


# Filter the DataFrame based on the selected result
if result_filter == "All":
    filtered_df = df
else:
    filtered_df = df[df["Result"] == result_filter]


# Select only the required columns for the filtered student table
display_columns = [
    "G1",
    "G2",
    "G3",
    "Result",
    "Percentage",
    "absences",
    "studytime",
    "failures",
    "risk_score"
]


# Display the filtered student DataFrame
st.dataframe(
    filtered_df[display_columns],
    use_container_width=True
)


# Add the At-Risk Students section
st.subheader("⚠️ At-Risk Students")


# Select students whose G3 is between 1 and 9
at_risk_df = df[
    (df["G3"] >= 1) & (df["G3"] <= 9)
]


# Sort at-risk students by G3 in ascending order
# Lower G3 means worse academic performance
at_risk_df = at_risk_df.sort_values(
    "G3",
    ascending=True
)


# Select only the required columns for the at-risk table
at_risk_columns = [
    "G1",
    "G2",
    "G3",
    "absences",
    "studytime",
    "failures"
]


# Display the at-risk students table
st.dataframe(
    at_risk_df[at_risk_columns],
    use_container_width=True
)


# Display the total number of at-risk students
st.write(f"Total at-risk students: {len(at_risk_df)}")
