# 💳 Credit Card Fraud Detection

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Classification-orange)
![Data Imbalance](https://img.shields.io/badge/Handling-Imbalanced%20Data-red)

## 📌 Overview
Credit card fraud is a significant issue in the financial sector. This project builds a robust machine learning classification model to detect fraudulent transactions among highly imbalanced dataset. It focuses heavily on precision and recall to ensure fraudulent transactions are caught without overly penalizing legitimate ones.

## 🚀 Features
- **In-depth EDA:** Comprehensive statistical analysis of transaction features.
- **Imbalanced Data Handling:** Utilizing techniques like SMOTE or undersampling to manage the massive class imbalance.
- **Model Training:** Evaluating multiple classifiers (Random Forest, XGBoost, Logistic Regression, etc.).
- **Performance Metrics:** Focus on Area Under the Precision-Recall Curve (AUPRC), F1-Score, and Confusion Matrix.

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Pandas, NumPy, Scikit-Learn, Imbalanced-Learn, Matplotlib, Seaborn

## 📂 Project Structure
```text
Credit-Card-Fraud-Detection/
├── EDA.ipynb               # Jupyter notebook for Exploratory Data Analysis
├── Modeling.ipynb          # Jupyter notebook for building and evaluating the classifiers
├── creditcard.csv          # The anonymized transaction dataset
└── creditcard_report.html  # Auto-generated profiling report
```

## 💻 How to Run
1. Clone the repository: `git clone <your-repo-url>`
2. Install dependencies: `pip install pandas numpy scikit-learn imbalanced-learn matplotlib seaborn`
3. First, explore the data using `EDA.ipynb`.
4. Then, run `Modeling.ipynb` to train and evaluate the detection models.