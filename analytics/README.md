# Analytics Module

## Module 2 - Data Analytics, Exploratory Data Analysis & Machine Learning

---

## Overview

The Analytics module performs exploratory data analysis (EDA) and statistical analysis on the Titanic dataset available through Seaborn. It demonstrates a complete analytics workflow beginning with dataset profiling, followed by data preprocessing, statistical analysis, visualization, multivariate storytelling, and feature standardization.

The module has been implemented as a modular Python application following software engineering best practices. Each analytical task has been separated into an independent service class to improve readability, maintainability, and reusability.

The implementation strictly follows the IIT Patna Capstone Project Module 2 (Part A) requirements.

---

## Objectives

The objectives of this module are:

- Load the Titanic dataset using `sns.load_dataset("titanic")`.
- Perform exploratory data analysis.
- Profile the dataset.
- Handle missing values using rule-based preprocessing.
- Perform univariate statistical analysis.
- Perform bivariate relationship analysis.
- Build a multivariate data story using multiple visualizations.
- Demonstrate feature standardization using z-score normalization.
- Generate reproducible reports and visualizations.

---

# Technology Stack

The project was implemented using the following technologies.

## Programming Language

- Python 3

## Data Processing

- Pandas
- NumPy

## Visualization

- Matplotlib

## Machine Learning

- Scikit-Learn
- Imbalanced-Learn

## Model Serialization

- Joblib

## Development Environment

- Visual Studio Code
- Git
- GitHub

---

---

## Project Structure

```text
analytics/
│
├── config/
├── datasets/
├── outputs/
│   ├── figures/
│   ├── logs/
│   ├── models/
│   └── reports/
├── services/
│   ├── eda.py
│   ├── preprocessing.py
│   ├── univariate_analysis.py
│   ├── bivariate_analysis.py
│   ├── multivariate_analysis.py
│   ├── standardization_check.py
│   ├── model_preparation.py
│   ├── preprocessing_pipeline.py
│   ├── classification_models.py
│   ├── model_evaluation.py
│   ├── imbalance_analysis.py
│   ├── hyperparameter_tuning.py
│   ├── regression_analysis.py
│   ├── model_comparison.py
│   └── pipeline_validation.py
│
├── utils/
│   └── exception.py
│
├── main.py
├── README.md
└── requirements.txt
```

---

# Dataset

This project uses the Titanic dataset provided by the Seaborn library.

```python
import seaborn as sns

dataframe = sns.load_dataset("titanic")
```

The dataset is downloaded automatically by Seaborn during the first execution and subsequently loaded from the local cache. No manual dataset download is required.

### Dataset Summary

| Property | Value |
|----------|------:|
| Records | 891 |
| Features | 15 |
| Target Variable | survived |
| Missing Values | Present |
| Numerical Features | age, fare, sibsp, parch, pclass |
| Categorical Features | sex, embarked, class, deck, embark_town |

---

# Running the Project

Clone the repository.

```bash
git clone <repository-url>
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Execute the analytics pipeline.

```bash
python analytics/main.py
```

Upon successful execution, all reports, processed datasets, and visualizations are generated inside the `outputs` directory.

---

# Task A.1 - Dataset Profiling

## Objective

The first task focuses on understanding the Titanic dataset before performing any preprocessing or statistical analysis. Dataset profiling provides insights into the dataset's structure, data types, descriptive statistics, and missing values, enabling informed preprocessing decisions.

---

## Implementation

The Titanic dataset is loaded using Seaborn's built-in dataset loader.

```python
import seaborn as sns

dataframe = sns.load_dataset("titanic")
```

The following exploratory checks are performed:

- Dataset shape
- Dataset information (`info()`)
- Summary statistics (`describe(include="all")`)
- Missing value percentage for each column
- Backup of the original dataset

---

## Dataset Profile

| Property | Value |
|----------|------:|
| Number of Records | 891 |
| Number of Features | 15 |
| Target Variable | survived |
| Numeric Features | age, fare, sibsp, parch, pclass |
| Categorical Features | sex, embarked, class, deck, embark_town |

---

## Missing Value Analysis

The percentage of missing values was calculated for every column.

| Column | Missing (%) |
|---------|------------:|
| age | 19.87 |
| embarked | 0.22 |
| embark_town | 0.22 |
| deck | 77.22 |

These statistics were later used to determine the preprocessing strategy implemented in Task A.2.

---

## Outputs Generated

### Dataset Backup

```
outputs/titanic.csv
```

### Console Output

The analytics pipeline prints:

- Dataset shape
- Dataset information
- Summary statistics
- Missing value percentages

This provides immediate visibility into the characteristics of the dataset before any preprocessing.

---

## Key Findings

- The Titanic dataset contains **891 passenger records**.
- Four columns contain missing values.
- The `deck` column has a very high percentage of missing values (77.22%), making direct imputation unreliable.
- The `age` column has moderate missing values (19.87%), making it suitable for statistical imputation.
- The remaining missing values occur in less than 1% of the records.

---

# Task A.2 - Missing Value Handling

## Objective

The purpose of this task is to preprocess missing values using a rule-based strategy defined by the assignment rubric.

Rather than applying a single imputation technique to every feature, each column is treated independently according to its percentage of missing values.

---

## Missing Value Strategy

The following threshold-based strategy was implemented.

| Missing Percentage | Strategy |
|-------------------:|----------|
| Less than 5% | Drop rows containing missing values |
| Between 5% and 30% | Median imputation |
| Greater than 30% | Drop the column |

---

## Column-wise Decisions

### Age

- Missing Percentage: **19.87%**
- Strategy: **Median Imputation**

**Justification**

The missing percentage falls within the 5% to 30% threshold specified in the rubric. Median imputation preserves the dataset size while minimizing the influence of extreme age values.

---

### Embarked

- Missing Percentage: **0.22%**
- Strategy: **Drop Rows**

**Justification**

Since the missing percentage is significantly below 5%, removing the affected rows has a negligible impact on the dataset while avoiding unnecessary imputation.

---

### Embark Town

- Missing Percentage: **0.22%**
- Strategy: **Drop Rows**

**Justification**

The proportion of missing records is extremely small. Dropping these rows maintains data quality without affecting statistical validity.

---

### Deck

- Missing Percentage: **77.22%**
- Strategy: **Drop Column**

**Justification**

More than three-quarters of the values are missing. Imputing such a large proportion would introduce significant uncertainty and could distort subsequent analyses. Therefore, the column was removed from the cleaned dataset.

---

## Outputs Generated

### Cleaned Dataset

```
outputs/cleaned_titanic.csv
```

### Missing Value Report

```
outputs/reports/missing_value_handling_report.csv
```

The report records:

- Column name
- Missing percentage
- Selected preprocessing strategy
- Justification for the chosen strategy

---

## Execution Summary

The preprocessing module logs the measured missing percentage for every affected column before applying the selected strategy.

Example:

```
Column 'age' has 19.87% missing values.
Strategy selected: Median Imputation.

Column 'deck' has 77.22% missing values.
Strategy selected: Drop Column.
```

This ensures that every preprocessing decision is transparent and directly traceable to the assignment's threshold-based rules.

---

## Key Findings

- Missing values were handled independently for each column.
- The preprocessing strategy strictly followed the rubric-defined thresholds.
- The cleaned dataset retained the maximum amount of reliable information while avoiding inappropriate imputation.
- All preprocessing decisions were documented in a dedicated report for reproducibility.

---

# Task A.3 - Univariate Analysis

## Objective

The objective of this task is to analyze individual numerical variables independently to understand their central tendency, dispersion, distribution, and presence of outliers.

The analysis was performed on the following numerical features:

- Age
- Fare

For each feature, descriptive statistics and graphical visualizations were generated.

---

## Statistical Measures

The following statistics were calculated for each feature.

- Mean
- Median
- Mode
- First Quartile (Q1)
- Third Quartile (Q3)
- Interquartile Range (IQR)
- Lower Bound
- Upper Bound
- Number of Outliers
- Distribution Type

Outliers were identified using the IQR rule.

```
Lower Bound = Q1 − 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR
```

---

## Age Analysis

### Statistical Summary

| Statistic | Value |
|-----------|------:|
| Mean | 29.32 |
| Median | 28.00 |
| Mode | 28.00 |
| Q1 | 22.00 |
| Q3 | 35.00 |
| IQR | 13.00 |
| Lower Bound | 2.50 |
| Upper Bound | 54.50 |
| Number of Outliers | 65 |
| Distribution | Right Skewed |

### Histogram

![Age Histogram](outputs/figures/age_histogram.png)

### Box Plot

![Age Box Plot](outputs/figures/age_boxplot.png)

### Interpretation

The age distribution is positively skewed, indicating a larger concentration of younger passengers with fewer elderly passengers. The box plot identifies several passengers above the upper whisker as outliers, representing unusually old ages. Although outliers exist, they represent valid observations and were retained for analysis.

---

## Fare Analysis

### Statistical Summary

| Statistic | Value |
|-----------|------:|
| Mean | 32.10 |
| Median | 14.45 |
| Mode | 8.05 |
| Q1 | 7.90 |
| Q3 | 31.00 |
| IQR | 23.10 |
| Lower Bound | -26.76 |
| Upper Bound | 65.66 |
| Number of Outliers | 114 |
| Distribution | Right Skewed |

### Histogram

![Fare Histogram](outputs/figures/fare_histogram.png)

### Box Plot

![Fare Box Plot](outputs/figures/fare_boxplot.png)

### Interpretation

The fare distribution is highly right skewed with several high-value ticket prices appearing as outliers. The large difference between the mean and median indicates that a small number of expensive tickets increase the average fare considerably. These observations are expected because first-class passengers paid significantly higher fares.

---

## Outputs Generated

### Figures

```
outputs/figures/

age_histogram.png
age_boxplot.png
fare_histogram.png
fare_boxplot.png
```

### Reports

```
outputs/reports/

univariate_statistics.csv
```

---

## Key Findings

- Both Age and Fare exhibit right-skewed distributions.
- Fare contains considerably more extreme values than Age.
- The IQR method successfully identified potential outliers.
- Outliers were retained because they represent genuine passenger records rather than data-entry errors.

---

# Task A.4 - Bivariate Analysis

## Objective

The objective of this task is to investigate relationships between pairs of variables and determine how passenger characteristics influenced survival.

The analysis consisted of two parts:

1. Survival rate analysis using Boolean masking.
2. Correlation analysis of numerical features.

---

## Survival Rate Analysis

Boolean masking using logical operators (`&` and `|`) was used to calculate survival rates for different passenger groups.

The following analyses were performed.

### Survival Rate by Sex

| Sex | Survival Rate (%) |
|-----|------------------:|
| Female | 74.04 |
| Male | 18.89 |

The analysis demonstrates that female passengers experienced substantially higher survival rates than male passengers.

---

### Survival Rate by Passenger Class

| Passenger Class | Survival Rate (%) |
|----------------|------------------:|
| First | 62.62 |
| Second | 47.28 |
| Third | 24.24 |

Passengers travelling in higher classes experienced considerably better survival outcomes.

---

### Survival Rate by Sex and Passenger Class

| Sex | Passenger Class | Survival Rate (%) |
|------|----------------|------------------:|
| Female | First | 96.74 |
| Female | Second | 92.11 |
| Female | Third | 50.00 |
| Male | First | 36.89 |
| Male | Second | 15.74 |
| Male | Third | 13.54 |

This combined analysis highlights the interaction between passenger class and sex. Female passengers travelling in first class had the highest survival probability, while male passengers in third class experienced the lowest survival rate.

---

## Correlation Analysis

A Pearson correlation matrix was computed using the following six numerical variables.

- survived
- pclass
- age
- sibsp
- parch
- fare

The derived Boolean columns (`adult_male` and `alone`) were intentionally excluded because they are redundant features derived from other variables.

---

### Correlation Heatmap

![Correlation Heatmap](outputs/figures/correlation_heatmap.png)

---

## Strongest Correlations

The strongest relationships were identified by ranking the absolute values of the off-diagonal correlation coefficients.

| Rank | Feature Pair | Correlation |
|------|--------------|------------:|
| 1 | pclass ↔ fare | -0.548 |
| 2 | sibsp ↔ parch | 0.415 |

---

### Interpretation

**Passenger Class and Fare**

Passenger class exhibits the strongest negative correlation with fare because lower passenger class numbers represent higher travel classes. First-class passengers generally paid significantly higher fares than passengers travelling in second or third class.

**Siblings/Spouses and Parents/Children**

The positive correlation between `sibsp` and `parch` indicates that passengers travelling with spouses or siblings were also more likely to travel with parents or children, reflecting family travel groups.

---

## Outputs Generated

### Figures

```
outputs/figures/

correlation_heatmap.png
```

### Reports

```
outputs/reports/

survival_rate_by_sex.csv

survival_rate_by_pclass.csv

survival_rate_by_sex_pclass.csv

correlation_matrix.csv

top_correlations.csv
```

---

## Key Findings

- Female passengers had significantly higher survival rates than male passengers.
- First-class passengers were considerably more likely to survive than third-class passengers.
- Passenger class and fare exhibited the strongest statistical relationship.
- Family-related variables (`sibsp` and `parch`) showed a moderate positive correlation, suggesting that family members often travelled together.

---

# Task A.5 - Multivariate Data Story

## Objective

The objective of this task is to construct a coherent multivariate data story using multiple visualizations that collectively explain which passengers were more likely to survive the Titanic disaster and why.

Unlike univariate and bivariate analysis, this task combines multiple variables to identify broader patterns influencing survival.

---

## Visualizations

Four complementary visualizations were created.

### Chart 1 – Survival by Sex

![Survival by Sex](outputs/figures/survival_by_sex.png)

### Interpretation

Female passengers experienced substantially higher survival rates than male passengers. In contrast, the majority of male passengers did not survive. This indicates that passenger sex was one of the strongest factors associated with survival.

---

### Chart 2 – Survival by Passenger Class

![Survival by Passenger Class](outputs/figures/survival_by_passenger_class.png)

### Interpretation

Passengers travelling in first class experienced considerably better survival outcomes than those travelling in second and third class. The number of survivors decreases steadily from first class to third class. Passenger class therefore appears to have played a major role in determining survival.

---

### Chart 3 – Age Distribution by Survival

![Age Distribution](outputs/figures/age_distribution_by_survival.png)

### Interpretation

The age distributions of survivors and non-survivors overlap considerably, although survivors exhibit a slightly lower median age. This suggests that age alone is not a strong predictor of survival. Compared with passenger sex and passenger class, age has a weaker relationship with survival.

---

### Chart 4 – Fare vs Age by Survival

![Fare vs Age](outputs/figures/fare_vs_age_survival.png)

### Interpretation

Passengers paying higher fares were generally more likely to survive, reflecting the relationship between fare and passenger class. Survivors are observed across a wide range of ages, indicating that fare and passenger class are more influential than age alone. Together, these variables provide a clearer explanation of survival patterns than any single variable.

---

## Overall Data Story

The four visualizations collectively demonstrate that passenger sex and passenger class were the strongest determinants of survival. Female passengers and first-class passengers consistently experienced the highest survival rates. Age showed only a modest influence, while fare reinforced the importance of passenger class. Overall, the multivariate analysis indicates that socioeconomic status and passenger demographics played a significant role in survival outcomes.

---

## Outputs Generated

### Figures

```
outputs/figures/

survival_by_sex.png

survival_by_passenger_class.png

age_distribution_by_survival.png

fare_vs_age_survival.png
```

### Report

```
outputs/reports/

multivariate_story.md
```

---

# Task A.6 - Feature Standardization (EDA Sanity Check)

## Objective

The purpose of this task is to demonstrate feature standardization using z-score normalization as an exploratory data analysis (EDA) exercise. This standardization is performed solely to verify the transformation process and is **not** used in the predictive modeling pipeline implemented later.

---

## Standardization Method

The numerical features **Age** and **Fare** were standardized using Scikit-learn's `StandardScaler`.

The transformation applies the z-score formula:

```
z = (x - μ) / σ
```

where:

- μ is the feature mean
- σ is the feature standard deviation

The scaler was applied only to a copy of the cleaned dataset, ensuring that the original dataset remained unchanged.

---

## Before and After Comparison

The mean and standard deviation of each feature were compared before and after standardization.

| Feature | Before Mean | Before Std | After Mean | After Std |
|-----------|------------:|-----------:|-----------:|----------:|
| Age | 29.3152 | 12.9849 | 0.0000 | 1.0006 |
| Fare | 32.0967 | 49.6975 | 0.0000 | 1.0006 |

The transformed features have an approximate mean of **0** and standard deviation of **1**, confirming that standardization was applied successfully. The slight deviation from exactly **1.0000** is expected because `StandardScaler` computes the population standard deviation (`ddof=0`), whereas pandas reports the sample standard deviation (`ddof=1`).

---

## Distribution Comparison

### Age Standardization

![Age Standardization](outputs/figures/age_standardization.png)

---

### Fare Standardization

![Fare Standardization](outputs/figures/fare_standardization.png)

---

## Outputs Generated

### Figures

```
outputs/figures/

age_standardization.png

fare_standardization.png
```

### Report

```
outputs/reports/

standardization_summary.csv
```

---

## Key Findings

- Feature standardization successfully transformed both numerical variables to approximately zero mean and unit variance.
- The original cleaned dataset remained unchanged throughout the process.
- This exercise served purely as an exploratory validation step and intentionally remained separate from the predictive modeling pipeline.

---

# Overall Conclusions

The exploratory analysis revealed several important insights regarding passenger survival.

- Female passengers experienced significantly higher survival rates than male passengers.
- First-class passengers consistently demonstrated the highest probability of survival.
- Passenger class and fare exhibited the strongest statistical relationship.
- Age showed only a moderate influence on survival compared with passenger class and sex.
- Standardization successfully transformed numerical variables while preserving the original dataset for future predictive modeling.

These findings establish a strong analytical foundation for **Module 2 Part B**, where predictive machine learning models will be developed using the cleaned Titanic dataset.

---

---

---

# Module 2 Part B – Predictive Analytics & Machine Learning

## Overview

Part B extends the exploratory analysis performed in Part A by implementing a complete machine learning workflow using the cleaned Titanic dataset. The workflow follows industry best practices, including train/test separation, reusable preprocessing pipelines, model training, evaluation, hyperparameter optimization, imbalance handling, regression analysis, and deployment-ready pipeline validation.

The primary objectives are to:

- Prepare data for predictive modeling.
- Train and evaluate multiple classification models.
- Compare different imbalance handling techniques.
- Optimize the Random Forest classifier using GridSearchCV.
- Perform multivariate linear regression.
- Compare classification and regression models.
- Save and validate a reusable machine learning pipeline.

---

## Task B.1 – Model Preparation

### Objective

Prepare the cleaned dataset for predictive modeling by creating training and testing datasets while preserving the original class distribution.

### Implementation

The cleaned Titanic dataset was divided into training and testing subsets using an 80:20 stratified train/test split.

Stratification was selected because the target variable (`survived`) is moderately imbalanced.

Overall class distribution:

| Class | Count | Percentage |
|--------|------:|-----------:|
| Not Survived | 549 | 61.75% |
| Survived | 340 | 38.25% |

Training dataset:

- 711 samples (80%)

Testing dataset:

- 178 samples (20%)

The class distribution was successfully preserved in both datasets to ensure representative model evaluation.

Generated outputs:

- `class_distribution.csv`
- `train_test_summary.csv`
- `stratification_justification.txt`

---

## Task B.2 – Machine Learning Preprocessing Pipeline

### Objective

Build a reusable preprocessing pipeline that prevents data leakage during model training.

### Implementation

A Scikit-Learn `ColumnTransformer` was created to preprocess numerical and categorical features separately.

#### Numerical Features

- pclass
- age
- sibsp
- parch
- fare

Processing steps:

- Median Imputation
- StandardScaler

#### Categorical Features

- sex
- embarked

Processing steps:

- Most Frequent Imputation
- One-Hot Encoding

The preprocessing pipeline is intentionally **not fitted** during construction.

Instead, it is fitted only on the training dataset inside each model pipeline, ensuring complete separation between training and testing data.

Generated outputs:

- `preprocessing_summary.txt`

---

## Task B.3 – Classification Model Training

### Objective

Train multiple machine learning classifiers using the same preprocessing pipeline and identical train/test split.

### Models Implemented

- Logistic Regression
- Decision Tree
- Random Forest

Each classifier was implemented as a complete Scikit-Learn Pipeline consisting of:

- ColumnTransformer
- Classifier

This design guarantees that preprocessing is performed identically during both training and prediction.

A visualization of the trained Decision Tree was also generated using `plot_tree()`.

Generated outputs:

- `logistic_regression_pipeline.pkl`
- `decision_tree_pipeline.pkl`
- `random_forest_pipeline.pkl`
- `decision_tree.png`

---

## Task B.4 – Model Evaluation

### Objective

Evaluate the performance of all trained classification models using a common testing dataset and compare their predictive capabilities using standard classification metrics.

### Evaluation Metrics

The following evaluation metrics were computed for each classifier:

- Accuracy
- Precision
- Recall
- F1 Score
- Area Under the ROC Curve (AUC)
- Confusion Matrix

A Receiver Operating Characteristic (ROC) curve was also generated to compare the classification performance across all models.

### Results

| Model | Accuracy | Precision | Recall | F1 Score | AUC |
|--------|---------:|----------:|--------:|---------:|----:|
| Logistic Regression | 0.8090 | 0.7833 | 0.6912 | 0.7344 | 0.8610 |
| Decision Tree | 0.7697 | 0.6901 | 0.7206 | 0.7050 | 0.7541 |
| Random Forest | **0.8202** | 0.7813 | **0.7353** | **0.7576** | 0.8179 |

### Observations

- Random Forest achieved the highest Accuracy and F1 Score.
- Logistic Regression achieved the highest ROC-AUC score, indicating strong ranking capability.
- Decision Tree produced competitive Recall but lower overall predictive performance compared to the ensemble models.

Generated outputs:

- `classification_model_comparison.csv`
- `roc_curve_comparison.png`
- `confusion_matrix_logistic_regression.png`
- `confusion_matrix_decision_tree.png`
- `confusion_matrix_random_forest.png`

---

## Task B.5 – Imbalance Handling Comparison

### Objective

Investigate the impact of different class imbalance handling techniques on classification performance.

### Class Distribution

| Class | Count | Percentage |
|--------|------:|-----------:|
| Not Survived | 439 | 61.74% |
| Survived | 272 | 38.26% |

Three imbalance handling strategies were evaluated using the Random Forest classifier:

1. Baseline (No imbalance handling)
2. Class Weight (`class_weight='balanced'`)
3. SMOTE (Synthetic Minority Over-sampling Technique)

### Results

| Strategy | Precision | Recall | F1 Score |
|-----------|----------:|--------:|---------:|
| Baseline | **0.7812** | **0.7353** | **0.7576** |
| Class Weight | 0.7692 | 0.7353 | 0.7519 |
| SMOTE | 0.7460 | 0.6912 | 0.7176 |

### Conclusion

Although the dataset exhibits moderate class imbalance, the baseline Random Forest classifier achieved the highest F1 Score. Applying class weighting produced only a marginal decrease in performance, while SMOTE resulted in lower Precision, Recall, and F1 Score on the test dataset. Consequently, no additional imbalance handling technique was adopted for the final model.

Generated outputs:

- `class_balance_before_smote.csv`
- `imbalance_comparison.csv`
- `imbalance_conclusion.txt`

---

## Task B.6 – Hyperparameter Tuning

### Objective

Optimize the Random Forest classifier using GridSearchCV to identify the best-performing hyperparameter combination.

### Hyperparameters Tuned

The following parameters were evaluated:

- `n_estimators`
- `max_depth`
- `max_features`

Five-fold cross-validation was used during the search process.

### Best Parameters

| Parameter | Value |
|------------|------|
| n_estimators | 300 |
| max_depth | 5 |
| max_features | sqrt |

### Performance

| Metric | Value |
|---------|------:|
| Best Cross Validation Accuracy | 0.8200 |
| Out-of-Bag Score | 0.8214 |

The optimized Random Forest model was saved as a reusable Scikit-Learn pipeline containing both the preprocessing steps and the trained classifier.

Generated outputs:

- `best_random_forest_pipeline.pkl`
- `best_random_forest_parameters.csv`
- `hyperparameter_tuning_summary.txt`

---

## Task B.7 – Regression Analysis

### Objective

Perform a multivariate linear regression analysis using the Titanic dataset to predict passenger fare from the remaining available features.

### Target Variable

- `fare`

### Regression Model

A Linear Regression model was trained using the same train/test split methodology adopted throughout the classification tasks. The preprocessing pipeline handled missing values, categorical encoding, and feature scaling before fitting the regression model.

### Evaluation Metrics

| Metric | Value |
|---------|------:|
| Mean Absolute Error (MAE) | 21.0986 |
| Root Mean Squared Error (RMSE) | 41.7021 |
| R² Score | 0.3482 |
| Adjusted R² | 0.3213 |

### Residual Analysis

A residual plot was generated to assess the assumptions of linear regression.

**Observation**

The residuals are reasonably scattered around zero without a strong systematic pattern. Although some variation increases for larger predicted fares, there is no clear evidence of severe heteroscedasticity. The model provides moderate predictive capability, which is reflected by the relatively low R² score.

Generated outputs:

- `regression_metrics.csv`
- `regression_conclusion.txt`
- `regression_residual_plot.png`

---

## Task B.8 – Model Comparison

### Objective

Summarize the performance of all classification and regression models in a single comparison report while keeping their evaluation metrics separate because they represent different learning tasks.

### Classification Models

| Model | Accuracy | Precision | Recall | F1 Score | AUC |
|--------|---------:|----------:|--------:|---------:|----:|
| Logistic Regression | 0.8090 | 0.7833 | 0.6912 | 0.7344 | 0.8610 |
| Decision Tree | 0.7697 | 0.6901 | 0.7206 | 0.7050 | 0.7541 |
| Random Forest | **0.8202** | 0.7813 | **0.7353** | **0.7576** | 0.8179 |

### Regression Model

| Model | MAE | RMSE | R² | Adjusted R² |
|--------|----:|-----:|---:|------------:|
| Linear Regression | 21.0986 | 41.7021 | 0.3482 | 0.3213 |

### Final Recommendation

Among the evaluated classification models, the **Random Forest classifier** is recommended for deployment.

Although Logistic Regression achieved the highest ROC-AUC score (0.8610), the Random Forest classifier delivered the strongest overall predictive performance by achieving the highest Accuracy (0.8202), highest Recall (0.7353), and highest F1 Score (0.7576). These metrics demonstrate a better balance between identifying survivors and minimizing misclassification errors. Additionally, after hyperparameter tuning, the optimized Random Forest achieved an Out-of-Bag (OOB) score of 0.8214, further supporting its robustness and generalization capability.

Generated outputs:

- `final_model_comparison.csv`
- `model_recommendation.txt`

---

## Task B.9 – Pipeline Serialization & Validation

### Objective

Save the best-performing machine learning pipeline as a reusable production-ready artifact and verify that it can perform predictions directly on raw input data.

### Pipeline Serialization

The optimized Random Forest pipeline was serialized using Joblib.

The saved pipeline contains:

- Median Imputer
- StandardScaler
- One-Hot Encoder
- ColumnTransformer
- Optimized Random Forest Classifier

Saving the complete preprocessing and modeling workflow ensures that future predictions require no manual preprocessing.

### Pipeline Validation

The serialized pipeline was reloaded using `joblib.load()` and evaluated using a sample passenger record containing raw, unprocessed feature values.

Example input:

| Feature | Value |
|---------|------|
| Passenger Class | 1 |
| Age | 30 |
| Siblings/Spouses | 1 |
| Parents/Children | 0 |
| Fare | 50.0 |
| Sex | Male |
| Embarked | S |

Prediction Result

| Output | Value |
|--------|------|
| Predicted Class | Not Survived |
| Probability (Not Survived) | 63.96% |
| Probability (Survived) | 36.04% |

The successful prediction confirms that the saved pipeline performs preprocessing and inference seamlessly on raw passenger data without requiring any additional feature engineering.

Generated outputs:

- `best_random_forest_pipeline.pkl`

---

---

# Generated Outputs

The analytics pipeline generates the following artifacts during execution.

## Reports

| Report | Description |
|----------|-------------|
| `eda_summary.txt` | Summary of Exploratory Data Analysis |
| `missing_values_report.csv` | Missing value analysis |
| `summary_statistics.csv` | Descriptive statistics |
| `class_distribution.csv` | Overall target class distribution |
| `train_test_summary.csv` | Train/Test split summary |
| `stratification_justification.txt` | Stratified sampling justification |
| `preprocessing_summary.txt` | Machine learning preprocessing configuration |
| `classification_model_comparison.csv` | Classification evaluation metrics |
| `class_balance_before_smote.csv` | Training class distribution before imbalance handling |
| `imbalance_comparison.csv` | Comparison of imbalance handling strategies |
| `imbalance_conclusion.txt` | Best imbalance handling strategy |
| `best_random_forest_parameters.csv` | Best hyperparameters from GridSearchCV |
| `hyperparameter_tuning_summary.txt` | Hyperparameter tuning summary |
| `regression_metrics.csv` | Linear regression evaluation metrics |
| `regression_conclusion.txt` | Regression analysis interpretation |
| `final_model_comparison.csv` | Combined classification and regression comparison |
| `model_recommendation.txt` | Final model deployment recommendation |

---

## Figures

| Figure | Description |
|----------|-------------|
| `age_distribution.png` | Age distribution |
| `fare_distribution.png` | Fare distribution |
| `survival_distribution.png` | Survival count plot |
| `gender_distribution.png` | Gender distribution |
| `correlation_heatmap.png` | Feature correlation heatmap |
| `pairplot.png` | Pairwise feature relationships |
| `decision_tree.png` | Decision Tree visualization |
| `roc_curve_comparison.png` | ROC curve comparison |
| `confusion_matrix_logistic_regression.png` | Logistic Regression confusion matrix |
| `confusion_matrix_decision_tree.png` | Decision Tree confusion matrix |
| `confusion_matrix_random_forest.png` | Random Forest confusion matrix |
| `regression_residual_plot.png` | Linear Regression residual plot |

---

## Reports

```
outputs/reports/

dataset_profile.csv
missing_value_handling_report.csv
univariate_statistics.csv
survival_rate_by_sex.csv
survival_rate_by_pclass.csv
survival_rate_by_sex_pclass.csv
correlation_matrix.csv
top_correlations.csv
multivariate_story.md
standardization_summary.csv
```

---

## Saved Models

| Model | Description |
|---------|-------------|
| `logistic_regression_pipeline.pkl` | Complete Logistic Regression pipeline |
| `decision_tree_pipeline.pkl` | Complete Decision Tree pipeline |
| `random_forest_pipeline.pkl` | Complete Random Forest pipeline |
| `best_random_forest_pipeline.pkl` | Tuned production-ready Random Forest pipeline |


# Learning Outcomes

This module demonstrates the complete lifecycle of an analytics and machine learning project, including:

- Exploratory Data Analysis (EDA)
- Data Cleaning and Standardization
- Feature Selection
- Stratified Train/Test Splitting
- Pipeline-Based Data Preprocessing
- Missing Value Imputation
- Feature Scaling
- Categorical Encoding
- Classification Model Development
- Decision Tree Visualization
- Model Evaluation using Standard Classification Metrics
- ROC Curve and AUC Analysis
- Class Imbalance Handling using Class Weights and SMOTE
- Hyperparameter Optimization using GridSearchCV
- Out-of-Bag (OOB) Validation
- Multivariate Linear Regression
- Residual Analysis
- Comparative Model Evaluation
- Pipeline Serialization using Joblib
- End-to-End Pipeline Validation on Raw Data
- Modular and Reusable Machine Learning Architecture

---

# Future Enhancements

The current implementation establishes a strong machine learning foundation. Potential future enhancements include:

- Evaluate additional ensemble models such as XGBoost, LightGBM, and CatBoost.
- Perform automated feature selection and feature importance analysis.
- Introduce nested cross-validation for more robust model evaluation.
- Add model explainability using SHAP or LIME.
- Implement experiment tracking with MLflow.
- Expose trained models through REST APIs using FastAPI.
- Containerize the analytics pipeline using Docker.
- Automate model retraining with CI/CD pipelines.
- Integrate real-time prediction services for deployment.
- Implement model monitoring and drift detection for production environments.

---

# Conclusion

Module 2 successfully implements a complete end-to-end analytics and machine learning workflow using the Titanic dataset. Starting from exploratory data analysis, the project progresses through data preprocessing, feature engineering, predictive modeling, model evaluation, class imbalance analysis, hyperparameter optimization, regression analysis, and production-ready pipeline validation.

The implementation follows industry-standard machine learning practices by preventing data leakage through pipeline-based preprocessing, preserving class distribution using stratified sampling, and evaluating multiple algorithms using consistent performance metrics. The optimized Random Forest classifier demonstrated the strongest overall classification performance and was selected as the recommended deployment model.

By combining statistical analysis with predictive modeling and reusable software architecture, this module provides a scalable, maintainable, and production-oriented analytics solution that serves as a strong foundation for future machine learning applications.
