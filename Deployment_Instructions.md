# 🚀 Deployment Instructions (Streamlit Community Cloud)

You can easily deploy this Fraud Detection Streamlit app for **free** and get a live link for your resume.

## 🌍 How to Deploy

1. **Important - File Size**:
   - The original `creditcard.csv` is 150MB, which might be too large for some free GitHub accounts.
   - Run `python prepare_deployment.py` locally first. This will generate `creditcard_sample.csv` and `fraud_model.pkl`.
   - **Do not commit** `creditcard.csv` to GitHub. Only commit the `creditcard_sample.csv`, `fraud_model.pkl`, `app.py`, and `requirements.txt`.

2. **Push to GitHub**:
   - Push the selected files to a new GitHub repository.

3. **Create a Streamlit Cloud Account**:
   - Go to [share.streamlit.io](https://share.streamlit.io) and sign up using your GitHub account.

4. **Deploy the App**:
   - Click **"New app"**.
   - Select your GitHub repository, the branch (e.g., `main`), and the main file path: `app.py`.

5. **Launch**:
   - Click **"Deploy"**. Streamlit will install the packages from `requirements.txt` and launch your app.
   - Once it's running, you will get a permanent link (e.g., `https://your-fraud-app.streamlit.app/`).

6. **Add to Resume**:
   - Copy the link and add it to your resume's project section!
