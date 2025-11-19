# Switch Gear Prediction App

This app uses Streamlit to provide switch gear status predictions and
visualizations. Azure Active Directory authentication now protects the app.

## Installation
- Install dependencies: `pip install -r requirements.txt`
- Run the app: `streamlit run app.py`

## Azure AD setup
1. Create an app registration in Azure AD (example values from this project):
   - Application (client) ID: `17639821-2f6e-46c8-a843-e20c2edd9845`
   - Directory (tenant) ID: `495a670b-aaeb-4daf-9c9f-283d21bc59fd`
   - Redirect URI: `https://mullermu-swg-streamlit-2-app-zv97wo.streamlit.app/`
2. Configure these values before running Streamlit via environment variables or
   Streamlit secrets (either flat keys or an `[azure]` section):
   - `AZURE_CLIENT_ID` / `client_id` – Application (client) ID
   - `AZURE_TENANT_ID` / `tenant_id` – Directory (tenant) ID
   - `AZURE_CLIENT_SECRET` / `client_secret` – Client secret value
   - `AZURE_REDIRECT_URI` / `redirect_uri` – Redirect URI configured in Azure
3. Grant the app the `User.Read` Microsoft Graph permission and enable the
   Authorization Code flow.
4. Start Streamlit as usual (`streamlit run app.py`). When prompted, click
   **Sign in with Microsoft** to authenticate.

### Notes on permissions
- The `User.Read` permission only allows the signed-in user to authenticate and
  read their own basic profile data. It does **not** let the app create or
  register new Azure AD users.
- To add users, use the Azure AD portal or an app with stronger permissions
  (for example `User.ReadWrite.All` or `Directory.AccessAsUser.All`), which
  typically require admin consent.
