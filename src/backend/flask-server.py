from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "DisasterAlert")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
posts_collection = db["posts"]
events_collection = db["events"]

@app.route('/api/top-alerts', methods=['GET'])
# def debug_mongo():
#     """Debug MongoDB connection and data"""
#     try:
#         # Check if posts collection has data
#         count = posts_collection.count_documents({})
#         print(f"Total posts in DB: {count}")
        
#         # Fetch first 5 records for testing
#         sample_data = list(posts_collection.find({}, {"_id": 0}).limit(5))
#         print("Sample Data from MongoDB:", sample_data)
        
#         return jsonify({"status": "success", "total_posts": count, "sample_data": sample_data})
#     except Exception as e:
#         print(f"Error accessing MongoDB: {e}")
#         return jsonify({"error": f"Failed to access MongoDB: {str(e)}"}), 500
def get_top_alerts():
    """Get top 3 alerts based on credibility score and recency"""
    try:
        
        # Get current time
        current_time = datetime.datetime.now().timestamp()
        # 24 hours in seconds
        time_window = 1745412028 + 24 * 777
        
        # Find posts within the last 24 hours with high credibility
        recent_posts = list(posts_collection.find(
            {"created_utc": {"$gte": current_time - time_window}},
            {"_id": 0}  # Exclude MongoDB _id field
        ).sort([("credibility_score", -1), ("created_utc", -1)]).limit(3))
        
        # If not enough recent posts, just get top posts by credibility
        if len(recent_posts) < 3:
            additional_posts = list(posts_collection.find(
                {"_id": {"$nin": [post.get("_id") for post in recent_posts if "_id" in post]}},
                {"_id": 0}
            ).sort([("credibility_score", -1), ("created_utc", -1)]).limit(3 - len(recent_posts)))
            recent_posts.extend(additional_posts)
        print (jsonify(recent_posts))
        return jsonify(recent_posts)
    except Exception as e:
        app.logger.error(f"Error fetching top alerts: {e}")
        return jsonify({"error": "Failed to fetch top alerts"}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events with their summary information"""
    try:
        # Get query parameters for filtering if any
        disaster_type = request.args.get('type')
        location = request.args.get('location')
        query = {}
        
        if disaster_type:
            query["disaster_type"] = {"$regex": disaster_type, "$options": "i"}
        if location:
            query["location"] = {"$regex": location, "$options": "i"}
        
        # Get events summaries
        events = list(events_collection.find(query, {"_id": 0}))
        return jsonify(events)
    except Exception as e:
        app.logger.error(f"Error fetching events: {e}")
        return jsonify({"error": "Failed to fetch events"}), 500

@app.route('/api/events/<event_name>', methods=['GET'])
def get_event_details(event_name):
    """Get detailed information about a specific event including all related posts"""
    try:
        # Get all posts for this event
        posts = list(posts_collection.find(
            {"event_name": event_name},
            {"_id": 0}
        ).sort("created_utc", -1))
        
        # Get event summary
        event = events_collection.find_one({"event_name": event_name}, {"_id": 0})
        
        if not event:
            return jsonify({"error": "Event not found"}), 404
            
        return jsonify({
            "event": event,
            "posts": posts
        })
    except Exception as e:
        app.logger.error(f"Error fetching event details: {e}")
        return jsonify({"error": f"Failed to fetch event details: {str(e)}"}), 500

@app.route('/api/search', methods=['GET'])
def search_events():
    """Search events and posts by keyword"""
    try:
        keyword = request.args.get('q', '')
        if not keyword:
            return jsonify([])
            
        # Search both events and posts collections
        events = list(events_collection.find(
            {"$or": [
                {"event_name": {"$regex": keyword, "$options": "i"}},
                {"disaster_type": {"$regex": keyword, "$options": "i"}},
                {"location": {"$regex": keyword, "$options": "i"}}
            ]},
            {"_id": 0}
        ))
        
        return jsonify(events)
    except Exception as e:
        app.logger.error(f"Error searching: {e}")
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

# Scheduled job endpoint (for testing purposes)
@app.route('/api/refresh-data', methods=['POST'])
def refresh_data():
    """Endpoint to manually trigger data refresh (normally handled by scheduler)"""
    try:
        # This would normally be called by a scheduler
        # For now, it's just a placeholder
        return jsonify({"status": "Data refresh initiated"})
    except Exception as e:
        return jsonify({"error": f"Data refresh failed: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
