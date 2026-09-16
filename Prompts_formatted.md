# How to Use These Prompts

Follow this exact process:

1. Open Claude or ChatGPT

2. Paste Prompt 1

3. Get the code

4. Copy into your file

5. Read it — understand what it did

6. Run it — check for errors

7. Only then paste Prompt 2

Never paste all prompts at once. Each prompt builds on the previous one.

# FILE 1 — analysis.py

Give these prompts ONE BY ONE in order. Don't give all at once.

## Prompt 1 — Load Data and Feature Engineering

I am building a Student Academic Risk Intelligence System

using UCI Student Performance dataset (Maths.csv).

The CSV has these columns:

school, sex, age, address, famsize, Pstatus, Medu, Fedu,

Mjob, Fjob, reason, guardian, traveltime, studytime, failures,

schoolsup, famsup, paid, activities, nursery, higher, internet,

romantic, famrel, freetime, goout, Dalc, Walc, health, absences,

G1, G2, G3

Write a Python function called load_and_prepare_data(filepath)

using Pandas that:

1. Loads the CSV from the given filepath

2. Creates these new columns:

- Result: if G3=0 → "Dropout", G3 1-9 → "Fail", G3 10-20 → "Pass"

- Percentage: G3/20*100

- avg_alcohol: (Dalc + Walc) / 2

- parent_edu_avg: (Medu + Fedu) / 2

- grade_trend: G3 - G1

- total_support: count of "yes" values across schoolsup, famsup, paid

- risk_score: (failures*2) + (absences/10) + avg_alcohol - studytime

- g1_g2_avg: (G1 + G2) / 2

3. Returns the complete DataFrame

**Important rules:**

- G3 = 0 means Dropout, NOT a zero score

- No missing values in this dataset

- Add clear comments explaining each step

Only write this one function. Nothing else yet.

## Prompt 2 — NumPy Analysis

Continue the same analysis.py file.

Now write a function called calculate_statistics(df)

that takes the prepared DataFrame and uses NumPy to calculate:

1. class_avg_g3: mean of G3 excluding dropouts (G3 != 0)

2. pass_rate: percentage of students who passed

out of non-dropout students only

3. dropout_count: total students where G3 = 0

4. at_risk_count: students where G3 is between 1 and 9 inclusive

5. correlation_matrix: numpy corrcoef of G1, G2, G3

(excluding dropouts)

Return all these as a dictionary.

Add clear comments.

Only this function. Nothing else.

## Prompt 3 — Matplotlib Charts

Continue the same analysis.py file.

Write a function called generate_static_charts(df)

using Matplotlib that creates and SAVES two charts:

### Chart 1 - Bar chart:

- X axis: studytime levels (1, 2, 3, 4)

- Y axis: average G3 for each studytime level

- Title: "Average G3 by Study Time"

- X label: "Study Time (1=<2hrs, 2=2-5hrs, 3=5-10hrs, 4=>10hrs)"

- Y label: "Average G3"

- Save as: output/avg_g3_by_studytime.png

### Chart 2 - Pie chart:

- Show distribution of Pass, Fail, Dropout

- Title: "Student Result Distribution"

- Show percentages on each slice

- Save as: output/pass_fail_dropout_pie.png

**Important:**

- Create output/ folder if it does not exist

- Close each chart after saving (plt.close())

- Add comments explaining each step

Only this function. Nothing else.

## Prompt 4 — Plotly Charts

Continue the same analysis.py file.

Write a function called generate_interactive_charts(df)

using Plotly that creates two interactive charts:

### Chart 1 - Scatter plot:

- X axis: studytime

- Y axis: G3

- Color: Result column (Pass=green, Fail=red, Dropout=grey)

- Hover data: absences, G1, G2

- Title: "Study Time vs Final Grade (G3)"

### Chart 2 - Bar chart:

- X axis: internet (yes/no)

- Y axis: average G3 for each group

- Title: "Average G3 by Internet Access"

- Color: internet column

Both charts should use fig.show() to display.

Add comments explaining each step.

Only this function. Nothing else.

## Prompt 5 — Summary Table and Main Block

Continue the same analysis.py file.

1. Write a function called print_summary(stats) that takes

the stats dictionary from calculate_statistics() and prints

a clean formatted summary table like this:

================================================

STUDENT ACADEMIC RISK INTELLIGENCE SYSTEM

ANALYSIS SUMMARY

================================================

Total Students        : 395

Class Average G3      : 10.42

Pass Rate             : 66.84%

At-Risk Count         : 68

Dropout Count         : 38

================================================

2. Write the main block at the bottom:

if __name__ == "__main__":

- Call load_and_prepare_data("data/Maths.csv")

- Call calculate_statistics(df)

- Call generate_static_charts(df)

- Call generate_interactive_charts(df)

- Call print_summary(stats)

- Print "Analysis complete. Charts saved to output/ folder"

Add comments. Only these two things.

# FILE 2 — main.py (FastAPI)

## Prompt 6 — Setup and Data Loading

I am building a FastAPI REST API for a Student Academic Risk

Intelligence System.

Write the initial setup for main.py:

1. Import all necessary libraries

(FastAPI, Pydantic, Pandas, NumPy, uvicorn)

2. Create the FastAPI app with:

- title: "Student Academic Risk Intelligence System API"

- description: "API for analyzing student performance data"

- version: "1.0.0"

3. Write a function called load_data() that:

- Loads Maths.csv from data/ folder

- Applies same feature engineering as analysis.py

(Result, Percentage, avg_alcohol, parent_edu_avg,

grade_trend, total_support, risk_score, g1_g2_avg)

- Returns prepared DataFrame

4. Call load_data() at startup and store in a variable called df

Add clear comments. Only this setup. Nothing else yet.

## Prompt 7 — GET Endpoints

Continue the same main.py file.

Write these 3 GET endpoints:

### Endpoint 1 - GET /summary:

Returns a JSON with:

- total_students (int)

- class_average_g3 (float, rounded to 2 decimals)

- pass_rate_percent (float, rounded to 2 decimals)

- calculated from non-dropout students only

- at_risk_count (int) - G3 between 1 and 9

- dropout_count (int) - G3 = 0

### Endpoint 2 - GET /at-risk:

Returns list of students where G3 is between 1 and 9

Each item has: student_index, G1, G2, G3, absences

Sorted by G3 ascending (worst first)

### Endpoint 3 - GET /top-students:

Returns top 5 students by G3 (excluding dropouts)

Each item has: student_index, G1, G2, G3

Sorted by G3 descending

Add clear comments on each endpoint.

Only these 3 endpoints. Nothing else.

## Prompt 8 — POST Endpoint with Pydantic

Continue the same main.py file.

1. Write a Pydantic model called StudentInput with:

- G1: float, must be between 0 and 20

- G2: float, must be between 0 and 20

- studytime: int, must be between 1 and 4

- absences: int, must be between 0 and 100

- failures: int, must be between 0 and 4

Add validation error messages for each field.

2. Write POST /predict-result endpoint that:

- Accepts StudentInput

- Calculates estimated_g3 using this formula:

estimated_g3 = (G1 * 0.3) + (G2 * 0.6) +

(studytime * 0.3) - (failures * 1.5) -

(absences * 0.05)

- Clamps estimated_g3 between 0 and 20

- Determines prediction:

if estimated_g3 = 0 → "Dropout Risk"

if estimated_g3 < 10 → "Fail"

if estimated_g3 >= 10 → "Pass"

- Determines confidence:

if G1 and G2 both above 12 → "High"

if G1 and G2 both below 8 → "High"

else → "Medium"

- Returns estimated_g3, prediction, confidence

Add clear comments. Only this.

## Prompt 9 — Uvicorn Runner

Continue the same main.py file.

Add the main block at the bottom:

if __name__ == "__main__":

import uvicorn

uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

Also add a root endpoint GET / that returns:

```json
{
```

"message": "Student Academic Risk Intelligence System API",

"docs": "Visit /docs for full API documentation",

"version": "1.0.0"

```json
}
```

Only this. Nothing else.

# FILE 3 — app.py (Streamlit)

## Prompt 10 — KPI Cards and Page Setup

I am building a Streamlit dashboard called

Student Academic Risk Intelligence System.

Write the initial setup for app.py:

1. Import libraries: streamlit, pandas, plotly.express

2. Set page config:

- title: "Student Academic Risk Intelligence System"

- layout: "wide"

- page_icon: "🎓"

3. Load and prepare data:

- Load Maths.csv from data/ folder

- Apply same feature engineering

(Result, Percentage, avg_alcohol, parent_edu_avg,

grade_trend, total_support, risk_score, g1_g2_avg)

4. Show main title: "🎓 Student Academic Risk Intelligence System"

5. Show 4 KPI metric cards in ONE row using st.columns(4):

- Card 1: Total Students

- Card 2: Class Average G3

(mean of G3 excluding dropouts, rounded to 2 decimals)

- Card 3: Pass Rate %

(pass count / non-dropout count * 100, rounded to 1 decimal)

- Card 4: At-Risk Count (G3 between 1 and 9)

Add clear comments. Only this setup and KPI cards. Nothing else.

## Prompt 11 — Charts Side by Side

Continue the same app.py file.

Add a section called "📊 Performance Charts" using st.subheader.

Show 2 Plotly charts SIDE BY SIDE using st.columns(2):

Left chart - Scatter plot:

- X: studytime, Y: G3

- Color: Result (Pass=green, Fail=red, Dropout=grey)

- Hover: absences, G1, G2

- Title: "Study Time vs Final Grade"

- Use st.plotly_chart() with use_container_width=True

Right chart - Bar chart:

- X: internet (yes/no)

- Y: average G3 grouped by internet

- Title: "Average G3 by Internet Access"

- Use st.plotly_chart() with use_container_width=True

Add comments. Only these charts. Nothing else.

## Prompt 12 — Filter and At-Risk Table

Continue the same app.py file.

Add a section called "🚨 Student Analysis Table"

using st.subheader.

1. Add a dropdown using st.selectbox:

- Label: "Filter by Result"

- Options: ["All", "Pass", "Fail", "Dropout"]

2. Filter the DataFrame based on selection:

- "All" → show all students

- "Pass" / "Fail" / "Dropout" → filter by Result column

3. Show filtered DataFrame using st.dataframe() with these

columns only:

G1, G2, G3, Result, Percentage, absences,

studytime, failures, risk_score

4. Below the table, show a separate section:

"⚠️ At-Risk Students" using st.subheader

Show only students where G3 is between 1 and 9

Columns: G1, G2, G3, absences, studytime, failures

Sorted by G3 ascending (worst performing first)

Show count: "Total at-risk students: X"

Add comments. Only this section.

# FILE 4 — requirements.txt

## Prompt 13

Generate a requirements.txt file for a Python project that uses:

- pandas

- numpy

- matplotlib

- plotly

- streamlit

- fastapi

- uvicorn

- pydantic

# After Each File is Complete — Test Prompt

Use this after each file:

Here is my [analysis.py / main.py / app.py] code:

[paste your code]

Review this code for:

1. Are all business rules correct?

(G3=0 is Dropout, pass rate excludes dropouts)

2. Any bugs or edge cases missed?

3. Any missing comments?

4. Anything that would cause an error when run?
