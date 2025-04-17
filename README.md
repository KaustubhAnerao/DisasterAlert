# DisasterAlert 🚀
Real-time Disaster Monitoring & Alerts 🌍

DisasterAlert is a platform that fetches real-time disaster-related data from the Reddit API and displays it on an interactive dashboard. It provides insights on various disaster events and allows users to explore detailed posts associated with them.

## Features ✨

✅ Fetches real-time disaster data using the Reddit API 🔄  
✅ Monitors disasters like Earthquakes 🌍, Tornadoes 🌪, Hurricanes 🌀, Floods 🌊, Road Accidents 🚗💥, and Industrial Accidents 🏭🔥, Road Accidents 🚗💥, Landslides 🏔, Wildfires 🔥  
✅ Easily extendable: Add more disaster types by editing the clustering_event.ipynb file 📂  
✅ Displays disaster events as interactive cards 🃏 on the website  
✅ Clicking on a card shows related posts & discussions 🗣  
✅ Integrated interactive map for visualizing disaster locations 🗺  
✅ Built using Flask for API handling & MongoDB for database storage 🗄  


## Tech Stack 🛠
🔹 Frontend: React.js ⚛  
🔹 Backend: Flask 🐍  
🔹 Database: MongoDB Atlas🍃  
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
Create an Atlas account at MongoDB Atlas  
Set up a cluster on Atlas and get the connection URI.  
Replace the following in your .env file:  
MONGO_URI = "your_atlas_connection_string"  
DB_NAME = "DisasterAlert"  

### 4. Run the Flask backend
cd src/backend  
python flask-server.py  

### 5. Run the frontend/index.html


## Future Enhancements 🎯
🔹 Improved filtering options for disaster types 📌  
🔹 Real-time push notifications 🔔  
🔹 Support for more data sources beyond Reddit 🌐  
🔹 Heatmaps and cluster views for disaster density visualization 🔥  
