# DisasterAlert 🚀
Real-time Disaster Monitoring & Alerts 🌍

DisasterAlert is a platform that fetches real-time disaster-related data from the Reddit API and displays it on an interactive dashboard. It provides insights on various disaster events and allows users to explore detailed posts associated with them.

## Features ✨

✅ Fetches real-time disaster data using the Reddit API 🔄
✅ Monitors disasters like Earthquakes 🌍, Tornadoes 🌪, Hurricanes 🌀, Floods 🌊, Road Accidents 🚗💥, and Industrial Accidents 🏭🔥
✅ Displays disaster events as interactive cards 🃏 on the website
✅ Clicking on a card shows related posts & discussions 🗣
✅ Built using Flask for API handling & MongoDB for database storage 🗄
🛠 Tech Stack
🔹 Frontend: React.js ⚛
🔹 Backend: Flask 🐍
🔹 Database: MongoDB 🍃
🔹 API Integration: Reddit API 🛜



## Installation & Setup 📥 

### 1. Clone the repository
git clone https://github.com/KaustubhAnerao/DisasterAlert.git
cd DisasterAlert

### 2. Set up a Reddit API credential 
create a new directory src/config 
create a new .env file - save all the API credentials here.
required credentials - CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT 

### 3. set up MongooDB connection
server bydefault run on mongodb://localhost:27017/ if virtual env not setup
server connection setup: 
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "DisasterAlert")

### 4. Run the Flask backend
python app.py

### 5. Run the frontend/index.html


## Future Enhancements 🎯
🔹 Improved filtering options for disaster types 📌
🔹 Maps integration for Enhanced UI/UX experience 🌍