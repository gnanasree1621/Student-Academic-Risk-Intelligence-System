# Import FastAPI for creating the REST API
from fastapi import FastAPI

# Import Pydantic for data validation
from pydantic import BaseModel,Field


# Import Pandas for loading and processing the dataset
import pandas as pd

# Import NumPy for numerical calculations
import numpy as np

# Import Uvicorn for running the FastAPI application
import uvicorn


# Create the FastAPI application
app = FastAPI(
    title="Student Academic Risk Intelligence System API",
    description="API for analyzing student performance data",
    version="1.0.0"
)


# Function to load and prepare the student dataset
def load_data():
    # Load Maths.csv from the data folder
    df = pd.read_csv("data/Maths.csv")

    # Create Result based on the final grade (G3)
    # G3 = 0 means Dropout
    # G3 = 1 to 9 means Fail
    # G3 = 10 to 20 means Pass
    df["Result"] = df["G3"].apply(
        lambda x: "Dropout" if x == 0 else ("Fail" if 1 <= x <= 9 else "Pass")
    )

    # Convert G3 into percentage
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

    # Return the prepared DataFrame
    return df


# Load the data when the application starts
df = load_data()

# Endpoint 1: Return overall student performance summary
@app.get("/summary")
def get_summary():
    # Exclude dropout students (G3 = 0) for academic performance calculations
    non_dropout_df = df[df["G3"] != 0]

    # Calculate the total number of students
    total_students = len(df)

    # Calculate average G3 excluding dropout students
    class_average_g3 = round(non_dropout_df["G3"].mean(), 2)

    # Calculate pass rate among non-dropout students
    passed_students = (non_dropout_df["G3"] >= 10).sum()
    pass_rate_percent = round(
        (passed_students / len(non_dropout_df)) * 100, 2
    )

    # Count students at risk (G3 between 1 and 9)
    at_risk_count = int(
        ((df["G3"] >= 1) & (df["G3"] <= 9)).sum()
    )

    # Count dropout students (G3 = 0)
    dropout_count = int((df["G3"] == 0).sum())

    # Return the summary as JSON
    return {
        "total_students": int(total_students),
        "class_average_g3": float(class_average_g3),
        "pass_rate_percent": float(pass_rate_percent),
        "at_risk_count": at_risk_count,
        "dropout_count": dropout_count
    }


# Endpoint 2: Return students who are at risk
@app.get("/at-risk")
def get_at_risk_students():
    # Select students with G3 between 1 and 9
    at_risk_df = df[
        (df["G3"] >= 1) & (df["G3"] <= 9)
    ]

    # Sort by G3 in ascending order (worst performers first)
    at_risk_df = at_risk_df.sort_values("G3", ascending=True)

    # Return the required student information
    return [
        {
            "student_index": int(index),
            "G1": int(row["G1"]),
            "G2": int(row["G2"]),
            "G3": int(row["G3"]),
            "absences": int(row["absences"])
        }
        for index, row in at_risk_df.iterrows()
    ]


# Endpoint 3: Return the top 5 students
@app.get("/top-students")
def get_top_students():
    # Exclude dropout students
    non_dropout_df = df[df["G3"] != 0]

    # Sort students by G3 in descending order
    # and select the top 5 students
    top_students_df = non_dropout_df.sort_values(
        "G3", ascending=False
    ).head(5)

    # Return the required information for each top student
    return [
        {
            "student_index": int(index),
            "G1": int(row["G1"]),
            "G2": int(row["G2"]),
            "G3": int(row["G3"])
        }
        for index, row in top_students_df.iterrows()
    ]

# Pydantic model for validating student input data
class StudentInput(BaseModel):
    # G1 must be between 0 and 20
    G1: float = Field(
        ...,
        ge=0,
        le=20,
        description="G1 must be between 0 and 20"
    )

    # G2 must be between 0 and 20
    G2: float = Field(
        ...,
        ge=0,
        le=20,
        description="G2 must be between 0 and 20"
    )

    # Study time must be between 1 and 4
    studytime: int = Field(
        ...,
        ge=1,
        le=4,
        description="Study time must be between 1 and 4"
    )

    # Absences must be between 0 and 100
    absences: int = Field(
        ...,
        ge=0,
        le=100,
        description="Absences must be between 0 and 100"
    )

    # Failures must be between 0 and 4
    failures: int = Field(
        ...,
        ge=0,
        le=4,
        description="Failures must be between 0 and 4"
    )


# POST endpoint to predict the student's final result
@app.post("/predict-result")
def predict_result(student: StudentInput):
    # Calculate the estimated G3 using the given formula
    estimated_g3 = (
        (student.G1 * 0.3)
        + (student.G2 * 0.6)
        + (student.studytime * 0.3)
        - (student.failures * 1.5)
        - (student.absences * 0.05)
    )

    # Clamp estimated G3 between 0 and 20
    estimated_g3 = max(0, min(20, estimated_g3))

    # Determine the predicted result
    if estimated_g3 == 0:
        prediction = "Dropout Risk"
    elif estimated_g3 < 10:
        prediction = "Fail"
    else:
        prediction = "Pass"

    # Determine confidence based on G1 and G2
    if student.G1 > 12 and student.G2 > 12:
        confidence = "High"
    elif student.G1 < 8 and student.G2 < 8:
        confidence = "High"
    else:
        confidence = "Medium"

    # Return the prediction results
    return {
        "estimated_g3": round(estimated_g3, 2),
        "prediction": prediction,
        "confidence": confidence
    }

# Root endpoint
@app.get("/")
def root():
    # Return basic information about the API
    return {
        "message": "Student Academic Risk Intelligence System API",
        "docs": "Visit /docs for full API documentation",
        "version": "1.0.0"
    }


# Main block to run the FastAPI application using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )