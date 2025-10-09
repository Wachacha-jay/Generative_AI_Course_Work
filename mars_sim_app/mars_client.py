"""
Mars Colony API Client
Communicates with JAC API server for Streamlit frontend
"""

import requests
import json
import subprocess
import time
import os
from typing import Dict, Any, Optional

class MarsColonyClient:
    """Client for communicating with Mars Colony JAC API"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.jac_process = None
        self.start_jac_server()
    
    def start_jac_server(self):
        """Start the JAC API server"""
        try:
            # Start JAC server in background
            self.jac_process = subprocess.Popen([
                'jac', 'serve', 'mars_api.jac', '--port', '8000'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(3)
            print("✅ JAC API Server started on port 8000")
        except Exception as e:
            print(f"❌ Failed to start JAC server: {e}")
            self.jac_process = None
    
    def stop_jac_server(self):
        """Stop the JAC API server"""
        if self.jac_process:
            self.jac_process.terminate()
            self.jac_process.wait()
            print("🛑 JAC API Server stopped")
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Optional[Dict]:
        """Make HTTP request to JAC API"""
        try:
            url = f"{self.api_url}/{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=data or {}, timeout=5)
            else:
                return None
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to JAC API server")
            return None
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def get_colony_state(self) -> Optional[Dict]:
        """Get current colony state"""
        return self._make_request("state", "GET")
    
    def advance_day(self) -> Optional[Dict]:
        """Advance simulation by one day"""
        return self._make_request("advance_day", "POST")
    
    def send_diplomat(self, target: str = "Freedom Crater") -> Optional[Dict]:
        """Send diplomat to rebel camp"""
        return self._make_request("diplomat", "POST", {"target": target})
    
    def trade_resources(self, trade_type: str = "food", amount: int = 10) -> Optional[Dict]:
        """Trade resources"""
        return self._make_request("trade", "POST", {
            "trade_type": trade_type,
            "amount": amount
        })
    
    def resolve_dispute(self, habitat: str = "Habitat Alpha") -> Optional[Dict]:
        """Resolve habitat dispute"""
        return self._make_request("dispute", "POST", {"habitat": habitat})
    
    def mine_resources(self) -> Optional[Dict]:
        """Mine resources"""
        return self._make_request("mine", "POST")
    
    def __del__(self):
        """Cleanup when client is destroyed"""
        self.stop_jac_server()

# Alternative: Direct JAC execution (fallback)
class DirectJacClient:
    """Direct JAC execution client (fallback method)"""
    
    def __init__(self):
        self.colony_state = None
        self.initialize_colony()
    
    def initialize_colony(self):
        """Initialize colony by running JAC file"""
        try:
            result = subprocess.run([
                'jac', 'run', 'colony_simulation.jac'
            ], capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                print("✅ Colony initialized via direct JAC execution")
                # Parse colony state from JAC output if needed
                self.colony_state = self._parse_colony_state()
            else:
                print(f"❌ JAC execution failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Failed to initialize colony: {e}")
    
    def _parse_colony_state(self) -> Dict:
        """Parse colony state from JAC execution"""
        # This would need to be implemented based on JAC output format
        # For now, return a mock state
        return {
            "hub": {
                "name": "Olympus Base",
                "x": 0.0,
                "y": 0.0,
                "power": 100,
                "oxygen": 100,
                "food": 50,
                "water": 60,
                "medicine": 30,
                "morale": 75,
                "population": 5,
                "faction_loyalty": "united"
            },
            "habitats": [],
            "facilities": [],
            "rebel_camps": [],
            "scavenger_outposts": [],
            "neutral_zones": [],
            "trade_posts": [],
            "mediation_centers": [],
            "connections": [],
            "day": 1,
            "events_log": []
        }
    
    def get_colony_state(self) -> Optional[Dict]:
        """Get colony state"""
        return self.colony_state
    
    def advance_day(self) -> Optional[Dict]:
        """Advance day (mock implementation)"""
        if self.colony_state:
            self.colony_state["day"] += 1
            self.colony_state["events_log"].append(f"Sol {self.colony_state['day']}: Day advanced")
        return {"status": "success", "message": "Day advanced"}
    
    def send_diplomat(self, target: str = "Freedom Crater") -> Optional[Dict]:
        """Send diplomat (mock implementation)"""
        return {"status": "success", "message": f"Diplomat sent to {target}"}
    
    def trade_resources(self, trade_type: str = "food", amount: int = 10) -> Optional[Dict]:
        """Trade resources (mock implementation)"""
        return {"status": "success", "message": f"Traded {amount} {trade_type}"}
    
    def resolve_dispute(self, habitat: str = "Habitat Alpha") -> Optional[Dict]:
        """Resolve dispute (mock implementation)"""
        return {"status": "success", "message": f"Dispute resolved at {habitat}"}
    
    def mine_resources(self) -> Optional[Dict]:
        """Mine resources (mock implementation)"""
        return {"status": "success", "message": "Resources mined"}

def get_mars_client(use_api: bool = True) -> MarsColonyClient:
    """Get Mars Colony client (API or direct)"""
    if use_api:
        try:
            return MarsColonyClient()
        except Exception as e:
            print(f"⚠️ API client failed, falling back to direct execution: {e}")
            return DirectJacClient()
    else:
        return DirectJacClient()