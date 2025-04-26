# Smart Real Estate Investment Dashboard

## 🗄️ Project Overview
The **Smart Real Estate Investment Dashboard** is an open-source web application built with **Python** and **Streamlit**. It allows users to explore real estate listings with dynamic filters and offers additional insights through real-time data integrations.

The app combines:
- **1 local dataset** (`real_estate.csv`)
- **3 APIs**:
  - [Open-Meteo API](https://open-meteo.com/) - for live weather updates
  - [Foursquare Places API](https://location.foursquare.com/developer/) - for nearby restaurants
  - [Chicago Crime API](https://data.cityofchicago.org/) - for crime snapshots

This project blends static and live data to create a smart, dynamic, and user-friendly property search experience.

---

## 🔹 Features
- Search real estate listings by **state**, **city**, and **ZIP code**
- Apply filters for **price**, **bedrooms**, **home type**, and **rent/buy** options
- View **weather information** for selected cities
- Discover **nearby restaurants** powered by Foursquare
- Access **latest crime reports** for Chicago
- Interactive visualizations like **price distribution by home type**

---

## 💻 Tech Stack
- **Frontend**: Streamlit
- **Backend/Data Handling**: Python (Pandas, Requests)
- **APIs**: Open-Meteo, Foursquare Places, Chicago Crime Data
- **Environment Management**: Python-dotenv
- **Version Control**: Git, GitHub

---

## 🗂️ Project Structure
```bash
├── app.py                   # Streamlit web app
├── main.py                  # CLI-based data exploration tool
├── real_estate.csv          # Local real estate dataset
├── .env                     # Environment variables for API keys
├── launch.json              # VS Code launch configuration (optional)
├── Earned Value Management.pdf   # Project EVM documentation
├── Project Management Plan.pdf   # Full project plan document
```

---

## 🔧 Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-real-estate-dashboard.git
cd smart-real-estate-dashboard
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up the `.env` file:
```env
FOURSQUARE_API_KEY=your_foursquare_api_key
CENSUS_API_KEY=your_census_api_key
```

4. Run the Streamlit app:
```bash
streamlit run app.py
```

---

## 💼 Project Management Highlights
- **Earned Value Management (EVM)** used to track project performance.
- **Risk Management** strategies defined and applied.
- **Quality Assurance** through unit, integration, and usability testing.
- **Version Control** using GitHub branches and pull requests.

---

## 🔒 License
This project is open-source and available under the [MIT License](LICENSE).

---

## 👏 Acknowledgments
- [Open-Meteo API Documentation](https://open-meteo.com/)
- [Foursquare Developer Documentation](https://location.foursquare.com/developer/)
- [City of Chicago Open Data Portal](https://data.cityofchicago.org/)
- [Streamlit Official Docs](https://docs.streamlit.io/)
- [Pandas and Plotly Official Guides]

---

## 👤 Authors
- Aryan Deshmukh
- Tanishq Joglekar
- Mayur Koli
- Sudhanshu Panda

Supervised by **Prof. Dr. Maurice Dawson Jr.**, Illinois Institute of Technology.

