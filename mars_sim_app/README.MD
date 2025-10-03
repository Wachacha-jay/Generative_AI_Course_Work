# 🚀 Mars Colony Simulation - Complete Setup Guide

## 📦 Installation & Setup

### Step 1: Install Dependencies
```bash
# Create a virtual environment (recommended)
python -m venv mars_venv
source mars_venv/bin/activate  # On Windows: mars_venv\Scripts\activate

# Install required packages
pip install jaclang streamlit plotly
```

### Step 2: Project Structure
Create the following directory structure:

```
mars_colony_project/
│
├── colony_simulation.jac          # Main Jac game logic
├── mars_app.py                    # Streamlit frontend
├── requirements.txt               # Python dependencies
└── README.md                      # Documentation
```

### Step 3: Create Files

#### `requirements.txt`
```
jaclang>=0.7.0
streamlit>=1.28.0
plotly>=5.17.0
```

#### `colony_simulation.jac`
Use the complete Jac code provided in the "Complete Jac-Streamlit Mars Colony" artifact.

#### `mars_app.py`
Use the complete Python code provided in the "Streamlit App (mars_app.py)" artifact.

---

## 🎮 Running the Application

### Method 1: Standard Launch
```bash
# From your project directory
streamlit run mars_app.py
```

### Method 2: With Custom Port
```bash
streamlit run mars_app.py --server.port 8501
```

### Method 3: Development Mode
```bash
# Auto-reload on file changes
streamlit run mars_app.py --server.runOnSave true
```

---

## 🗺️ How It Works: The Jac-Streamlit Bridge

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  USER INTERFACE                         │
│                  (Streamlit Web App)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Controls │  │   Map    │  │ Metrics  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
           ┌─────────────────┐
           │  Jac Import     │ (jac_import)
           │  Python Bridge  │
           └────────┬────────┘
                    │
                    ▼
      ┌─────────────────────────────┐
      │    JAC GRAPH ENGINE         │
      │                             │
      │  ┌─────┐    ┌─────┐        │
      │  │Node │◄──►│Node │        │
      │  └─────┘    └─────┘        │
      │     ▲          ▲            │
      │     │          │            │
      │  ┌──┴──────────┴──┐        │
      │  │   Walkers      │        │
      │  │  (Game Logic)  │        │
      │  └────────────────┘        │
      └─────────────────────────────┘
```

### Data Flow Example

#### 1. **User Clicks "Send Diplomat"**
```python
# Streamlit button clicked
if st.button("Send Diplomat"):
    execute_action(jac_module, "send_diplomat", {'target': 'Freedom Crater'})
```

#### 2. **Python Calls Jac Walker**
```python
def execute_action(jac_module, action_type, params):
    walker = jac_module.DiplomatAction(target_camp=params['target'])
    # Walker is spawned and traverses the graph
    success = walker.success
    return success
```

#### 3. **Jac Walker Traverses Graph**
```jac
walker DiplomatAction {
    has target_camp: str;
    has success: bool = False;

    can negotiate with entry {
        visit [-->];  # Visit all connected nodes
    }

    can reduce_hostility with RebelCamp entry {
        if here.name == self.target_camp {
            here.hostility -= 15;  # Modify node state
            self.success = True;
        }
    }
}
```

#### 4. **State Extracted Back to Streamlit**
```python
# Extract updated state
extractor = jac_module.StateExtractor()
new_state = extractor.colony_state

# Update visualization
st.plotly_chart(create_mars_map(new_state))
```

---

## 🎯 Key Features & Usage

### 1. **Interactive Map**
- **Hover** over nodes to see detailed stats
- **Color-coded** markers:
  - Green habitats = Low disputes
  - Red habitats = High conflict
  - Red rebels = High hostility
  - Lines show connections between facilities

### 2. **Time Progression**
```python
# Click "Advance Day" button
# Triggers DaySimulator walker which:
# - Consumes resources (food, water, power)
# - Generates random events
# - Updates faction relationships
# - Adds events to log
```

### 3. **Diplomatic Actions**
```python
# Select rebel camp and click "Send Diplomat"
# DiplomatAction walker:
# - Traverses to target rebel camp
# - Reduces hostility by 15%
# - Logs success in event log
```

### 4. **Trading System**
```python
# Select resource type and click "Trade"
# TradeAction walker:
# - Exchanges colony resources for rebel goods
# - Updates both inventories
# - Affects faction relationships
```

### 5. **Dispute Resolution**
```python
# Select habitat and click "Resolve Dispute"
# DisputeResolver walker:
# - Visits target habitat
# - Reduces dispute level by 30%
# - Increases comfort level
```

---

## 🔧 Customization Guide

### Adding New Node Types

**Step 1: Define in Jac**
```jac
node MedicalBay {
    has name: str;
    has x: float;
    has y: float;
    has patients: int = 0;
    has medicine_stock: int = 50;
}
```

**Step 2: Add to State Extractor**
```jac
walker StateExtractor {
    can extract_medical with MedicalBay entry {
        self.colony_state["medical_bays"].append({
            "name": here.name,
            "x": here.x,
            "y": here.y,
            "patients": here.patients
        });
    }
}
```

**Step 3: Visualize in Streamlit**
```python
medical_bays = state.get('medical_bays', [])
for bay in medical_bays:
    fig.add_trace(go.Scatter(
        x=[bay['x']], y=[bay['y']],
        mode='markers+text',
        text=['🏥'],
        marker=dict(size=25, color='#ef4444')
    ))
```

### Adding New Walker Types

**Example: Medical Walker**
```jac
walker MedicWalker {
    has patients_treated: int = 0;

    can treat with entry {
        visit [-->];
    }

    can heal_colonists with MedicalBay entry {
        here.patients -= 2;
        self.patients_treated += 2;
    }
}
```

**Integrate in Streamlit:**
```python
if st.button("Send Medic"):
    walker = jac_module.MedicWalker()
    treated = walker.patients_treated
    st.success(f"Treated {treated} colonists")
```

---

## 📊 Advanced Features

### 1. **Real-Time Animation**
```python
import time

def animate_walker_movement(walker_path):
    placeholder = st.empty()
    for position in walker_path:
        with placeholder:
            fig = create_mars_map(state)
            # Add walker marker
            fig.add_trace(go.Scatter(
                x=[position['x']],
                y=[position['y']],
                marker=dict(size=20, color='yellow'),
                name='Walker'
            ))
            st.plotly_chart(fig)
            time.sleep(0.5)
```

### 2. **Graph Topology View**
```python
import networkx as nx

def show_graph_structure():
    G = nx.Graph()
    
    # Build from Jac graph
    state = get_colony_state(jac_module)
    
    # Add nodes
    G.add_node("Hub")
    for hab in state['habitats']:
        G.add_node(hab['name'])
        G.add_edge("Hub", hab['name'])
    
    # Visualize with Plotly
    pos = nx.spring_layout(G)
    # ... render network graph
```

### 3. **Live Event Stream**
```python
# In sidebar
if st.checkbox("Live Updates"):
    update_placeholder = st.empty()
    
    while True:
        time.sleep(3)
        execute_action(jac_module, "advance_day")
        
        with update_placeholder:
            st.write("Latest Events:")
            for event in st.session_state.events_log[-3:]:
                st.text(event)
```

### 4. **Node Inspector**
```python
selected_node = st.selectbox("Inspect Node", 
    ["Olympus Base", "Habitat Alpha", "Solar Array 1"])

if selected_node:
    # Create specific node finder walker
    finder = jac_module.NodeFinder(target_name=selected_node)
    node_data = finder.found_node
    
    st.json({
        "name": node_data.name,
        "attributes": vars(node_data)
    })
```

---

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
# Solution: Ensure Jac file is in same directory
ls -la colony_simulation.jac

# Or specify full path in mars_app.py:
jac_module = jac_import("colony_simulation", base_path="/full/path/to/file")
```

### Issue: "Walker not executing"
```python
# Add debugging:
try:
    walker = jac_module.DiplomatAction(target_camp="Freedom Crater")
    print(f"Walker created: {walker}")
    print(f"Success: {walker.success}")
except Exception as e:
    st.error(f"Walker failed: {e}")
    import traceback
    st.code(traceback.format_exc())
```

### Issue: "Graph not updating"
```python
# Force rerun after action:
if execute_action(jac_module, "advance_day"):
    st.rerun()  # Forces Streamlit to re-render
```

### Issue: "State extraction returns empty"
```jac
# Check walker is visiting all nodes:
walker StateExtractor {
    can extract with entry {
        print("Visiting:", here);  # Debug output
        visit [-->];
    }
}
```

---

## 🎓 Learning Resources

### Understanding Jac Concepts

1. **Nodes = Game Objects**
   - Persistent state containers
   - Have attributes (food, power, hostility)
   - Connected by edges

2. **Edges = Relationships**
   - Define how nodes connect
   - Can have properties (distance, trust_level)
   - Determine walker traversal paths

3. **Walkers = Actors/Logic**
   - Move through the graph
   - Execute actions at nodes
   - Carry state between nodes

### Example: Complete Action Flow

```jac
// 1. Define the world (nodes)
node City {
    has population: int;
    has resources: int;
}

// 2. Define connections (edges)
edge Road {
    has distance: int;
}

// 3. Define actors (walkers)
walker Trader {
    has goods: int = 10;
    
    can travel with entry {
        visit [-->];  // Move along roads
    }
    
    can trade with City entry {
        here.resources += self.goods;  // Deliver goods
        self.goods = 0;
    }
}

// 4. Build the world
with entry {
    city1 = City(population=100, resources=50);
    city2 = City(population=200, resources=30);
    root ++> city1;
    city1 +[Road(distance=100)]+> city2;
    
    // 5. Spawn actor
    trader = Trader(goods=20);
    root spawn trader;
}
```

---

## 🚀 Next Steps

### Enhancements You Can Add:

1. **Multiplayer Support**
   - Multiple users controlling different factions
   - Real-time updates via WebSockets

2. **Save/Load System**
   - Serialize graph state to JSON
   - Load previous game sessions

3. **AI Opponents**
   - Walkers with decision-making logic
   - Rebel camps that plan raids

4. **Resource Management**
   - Complex supply chains
   - Production buildings

5. **Tech Tree**
   - Unlock new buildings via research
   - Progressive gameplay

6. **Mission System**
   - Objectives and goals
   - Rewards and progression

---

## 📚 Complete Example: Adding a Weather System

### Step 1: Add Weather Node (Jac)
```jac
node WeatherStation {
    has name: str = "Mars Weather Center";
    has x: float = -1.0;
    has y: float = 4.0;
    has current_weather: str = "clear";
    has dust_storm_probability: int = 20;
}
```

### Step 2: Add Weather Walker (Jac)
```jac
walker WeatherSimulator {
    has weather_events: list = [];
    
    can check_weather with WeatherStation entry {
        import:py random;
        if random.randint(1, 100) < here.dust_storm_probability {
            here.current_weather = "dust_storm";
            self.weather_events.append("🌪️ Dust storm detected!");
        } else {
            here.current_weather = "clear";
        }
    }
}
```

### Step 3: Extract in State (Jac)
```jac
walker StateExtractor {
    can extract_weather with WeatherStation entry {
        self.colony_state["weather"] = {
            "current": here.current_weather,
            "storm_risk": here.dust_storm_probability
        };
    }
}
```

### Step 4: Visualize (Python)
```python
# In mars_app.py
def show_weather(state):
    weather = state.get('weather', {})
    current = weather.get('current', 'unknown')
    
    if current == 'dust_storm':
        st.warning("🌪️ DUST STORM IN PROGRESS!")
    else:
        st.success("☀️ Clear skies")
    
    st.metric("Storm Risk", f"{weather.get('storm_risk', 0)}%")
```

### Step 5: Integrate Action (Python)
```python
if st.button("Check Weather"):
    walker = jac_module.WeatherSimulator()
    events = walker.weather_events
    for event in events:
        st.warning(event)
```

---

##  Summary

You now have a complete, interactive Mars colony simulation that demonstrates the power of Jac's graph-based architecture:

- **Nodes** represent all game entities
- **Edges** define relationships and connections
- **Walkers** implement all game logic
- **Streamlit** provides beautiful, interactive visualization

The key insight: **The graph IS your game world**, and walkers bring it to life!

Happy colonizing! 🚀🔴