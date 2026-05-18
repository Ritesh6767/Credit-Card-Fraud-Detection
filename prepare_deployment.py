import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import sqlite3
import os

def prepare_deployment():
    print("Loading huge dataset...")
    df = pd.read_csv('creditcard.csv')
    
    # Save a small sample for the dashboard
    print("Saving a small sample for dashboard visualizations...")
    sample_df = pd.concat([
        df[df['Class'] == 0].sample(1000, random_state=42),
        df[df['Class'] == 1]  # Keep all frauds (there are usually around ~492)
    ]).sample(frac=1, random_state=42) # Shuffle
    
    sample_df.to_csv('creditcard_sample.csv', index=False)
    
    print("Training model...")
    X = sample_df.drop('Class', axis=1)
    y = sample_df['Class']
    
    # Train a quick Random Forest
    model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)
    model.fit(X, y)
    
    print("Saving model...")
    joblib.dump(model, 'fraud_model.pkl')
    
    print("Initializing SQLite Database...")
    conn = sqlite3.connect('fraud_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time REAL,
            amount REAL,
            predicted_class INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
    print("Done!")

if __name__ == "__main__":
    prepare_deployment()
