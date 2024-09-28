import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # You can send initial data when a client connects
        self.send(text_data=json.dumps({
            'message': 'You are connected!',
            'data': self.get_realtime_data()
        }))

    def disconnect(self, close_code):
        pass

    def get_realtime_data(self):
        # Fetch your real-time data from the database
        # Example: Return some statistics or other live data
        return {
            'requests_count': 42,  # Fetch from database
            'active_users': 10,    # Fetch from database
        }

    def receive(self, text_data):
        # Handle incoming messages if needed
        pass
