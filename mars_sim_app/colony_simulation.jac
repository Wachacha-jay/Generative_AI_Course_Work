"""
Complete Mars Colony Simulation with Streamlit Integration
Enhanced with position tracking, real-time updates, and interactive features
"""

import streamlit as st;
import plotly.graph_objects as go;
import random;
import from datetime { datetime }

# ==================== NODE DEFINITIONS ====================

node ColonyHub {
    has name: str;
    has x: float = 0.0;
    has y: float = 0.0;
    has power: int = 100;
    has oxygen: int = 100;
    has population: int = 5;
    has food: int = 50;
    has morale: int = 75;
    has water: int = 60;
    has medicine: int = 30;
    has faction_loyalty: str = "united";
    has trade_goods: dict = {"tech": 5, "tools": 10, "fuel": 20};
}

node Habitat {
    has name: str;
    has x: float;
    has y: float;
    has capacity: int = 10;
    has occupied: int = 0;
    has comfort: int = 50;
    has dispute_level: int = 0;
}

node PowerPlant {
    has name: str;
    has x: float;
    has y: float;
    has output: int = 50;
    has efficiency: int = 100;
    has fuel: int = 100;
}

node Greenhouse {
    has name: str;
    has x: float;
    has y: float;
    has food_production: int = 20;
    has water_usage: int = 10;
    has crops_growing: list = [];
}

node MiningStation {
    has name: str;
    has x: float;
    has y: float;
    has resources: dict = {"iron": 0, "water": 0, "minerals": 0};
    has mining_rate: int = 5;
}

node ResearchLab {
    has name: str;
    has x: float;
    has y: float;
    has projects: list = [];
    has tech_level: int = 1;
}

node MediationCenter {
    has name: str;
    has x: float;
    has y: float;
    has active_disputes: list = [];
    has resolved_disputes: int = 0;
    has peace_treaties: list = [];
}

node TradePost {
    has name: str;
    has x: float;
    has y: float;
    has inventory: dict = {"food": 20, "water": 15, "medicine": 10, "tech": 5};
    has prices: dict = {"food": 2, "water": 3, "medicine": 5, "tech": 10};
    has recent_trades: list = [];
}

node RebelCamp {
    has name: str;
    has x: float;
    has y: float;
    has population: int = 8;
    has ideology: str;
    has resources: dict = {"food": 15, "water": 20, "weapons": 5, "salvage": 30};
    has hostility: int = 50;
    has demands: list = [];
}

node ScavengerOutpost {
    has name: str;
    has x: float;
    has y: float;
    has scavengers: int = 5;
    has salvage_quality: str = "mixed";
    has discovered_items: list = [];
    has trade_preference: str;
}

node NeutralZone {
    has name: str;
    has x: float;
    has y: float;
    has safety_level: int = 70;
    has factions_present: list = [];
}

# ==================== EDGE DEFINITIONS ====================

edge PowerLine {
    has capacity: int = 25;
    has active: bool = True;
}

edge SupplyRoute {
    has distance: int;
    has condition: str = "good";
    has danger_level: int = 10;
}

edge DataLink {
    has bandwidth: int = 100;
}

edge TradeRoute {
    has established: bool = False;
    has trust_level: int = 50;
    has tariff: int = 0;
}

# ==================== WALKER DEFINITIONS ====================

walker StateExtractor {
    has colony_state: dict = {
        "hub": {},
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
    };

    can extract with entry {
        visit [-->];
    }

    can extract_hub with ColonyHub entry {
        self.colony_state["hub"] = {
            "name": here.name,
            "x": here.x,
            "y": here.y,
            "power": here.power,
            "oxygen": here.oxygen,
            "food": here.food,
            "water": here.water,
            "medicine": here.medicine,
            "morale": here.morale,
            "population": here.population,
            "faction_loyalty": here.faction_loyalty
        };
    }

    can extract_habitat with Habitat entry {
        self.colony_state["habitats"].append({
            "name": here.name,
            "x": here.x,
            "y": here.y,
            "occupied": here.occupied,
            "capacity": here.capacity,
            "dispute_level": here.dispute_level,
            "comfort": here.comfort
        });
    }

    can extract_power with PowerPlant entry {
        self.colony_state["facilities"].append({
            "name": here.name,
            "type": "power",
            "x": here.x,
            "y": here.y,
            "output": here.output,
            "efficiency": here.efficiency,
            "fuel": here.fuel
        });
    }

    can extract_greenhouse with Greenhouse entry {
        self.colony_state["facilities"].append({
            "name": here.name,
            "type": "food",
            "x": here.x,
            "y": here.y,
            "production": here.food_production,
            "crops": len(here.crops_growing)
        });
    }

    can extract_mining with MiningStation entry {
        self.colony_state["facilities"].append({
            "name": here.name,
            "type": "mining",
            "x": here.x,
            "y": here.y,
            "resources": here.resources,
            "mining_rate": here.mining_rate
        });
    }

    can extract_lab with ResearchLab entry {
        self.colony_state["facilities"].append({
            "name": here.name,
            "type": "research",
            "x": here.x,
            "y": here.y,
            "tech_level": here.tech_level,
            "projects": len(here.projects)
        });
    }

    can extract_mediation with MediationCenter entry {
        self.colony_state["mediation_centers"].append({
            "name": here.name,
            "x": here.x,
            "y": here.y,
            "active_disputes": len(here.active_disputes),
            "resolved": here.resolved_disputes
        });
    }

    can extract_trade_post with TradePost entry {
        self.colony_state["trade_posts"].append({
            "name": here.name,
            "x": here.x,
            "y": here.y,
            "inventory": here.inventory,
            "recent_trades": len(here.recent_trades)
        });
    }

    can extract_rebels with RebelCamp entry {
        self.colony_state["rebel_camps"].append({
            "name": here.name,
            "x": here.x,
            "y": here.y,
            "population": here.population,
            "hostility": here.hostility,
            "ideology": here.ideology,
            "demands": here.demands
        });
    }

    can extract_scavengers with ScavengerOutpost entry {
        self.colony_state["scavenger_outposts"].append({
            "name": here.name,
            "x": here.x,
            "y": here.y,
            "scavengers": here.scavengers,
            "items": len(here.discovered_items)
        });
    }

    can extract_neutral with NeutralZone entry {
        self.colony_state["neutral_zones"].append({
            "name": here.name,
            "x": here.x,
            "y": here.y,
            "safety": here.safety_level,
            "factions": len(here.factions_present)
        });
    }
}

walker DaySimulator {
    has events: list = [];

    can simulate with entry {
        visit [-->];
    }

    can update_hub with ColonyHub entry {
        # Resource consumption
        here.food -= 5;
        here.water -= 3;
        here.power = max(0, min(100, here.power - 2));
        
        # Check critical levels
        if here.food < 20 {
            here.morale -= 5;
            self.events.append("⚠️ Low food supplies affecting morale");
        }
        
        if here.power < 30 {
            self.events.append("🚨 CRITICAL: Power levels dangerously low!");
        }
        
        # Random events
        if here.food < 25 and here.morale < 50 {
            self.events.append("⚡ Unrest brewing due to resource scarcity");
        }
    }

    can update_greenhouse with Greenhouse entry {
        # Food production
        here.food_production += 2;
        here.crops_growing.append("crop_" + str(len(here.crops_growing)));
    }

    can update_habitats with Habitat entry {
        # Random disputes
        rand_val = 75;  # Simulating random
        if rand_val > 70 and here.dispute_level < 80 {
            here.dispute_level += 10;
            self.events.append(f"⚡ Dispute at {here.name}");
        }
    }

    can update_rebels with RebelCamp entry {
        # Rebel activity fluctuates
        if here.hostility > 60 {
            here.hostility += 3;
            self.events.append(f"🏴 {here.name} increasing hostility");
        } else {
            here.hostility = max(0, here.hostility - 2);
        }
    }
}

walker DiplomatAction {
    has target_camp: str;
    has success: bool = False;

    can negotiate with entry {
        visit [-->];
    }

    can reduce_hostility with RebelCamp entry {
        if here.name == self.target_camp {
            reduction = 15;
            here.hostility = max(0, here.hostility - reduction);
            self.success = True;
        }
    }
}

walker TradeAction {
    has trade_type: str;  # "food", "medicine", "tech"
    has amount: int = 10;
    has success: bool = False;

    can trade with entry {
        visit [-->];
    }

    can trade_with_hub with ColonyHub entry {
        if self.trade_type == "food" {
            here.food += self.amount;
            here.medicine -= 5;
            self.success = True;
        } elif self.trade_type == "medicine" {
            here.medicine += self.amount;
            here.food -= 8;
            self.success = True;
        }
    }
}

walker DisputeResolver {
    has target_habitat: str;
    has resolved: bool = False;

    can resolve with entry {
        visit [-->];
    }

    can reduce_tension with Habitat entry {
        if here.name == self.target_habitat {
            reduction = 30;
            here.dispute_level = max(0, here.dispute_level - reduction);
            here.comfort += 10;
            self.resolved = True;
        }
    }
}

walker MiningAction {
    has resource_gained: int = 0;

    can mine with entry {
        visit [-->];
    }

    can extract_resources with MiningStation entry {
        here.resources["water"] += 10;
        here.resources["iron"] += 5;
        here.resources["minerals"] += 3;
        self.resource_gained = 10;
    }
}

# ==================== GRAPH BUILDER ====================

glob colony_graph: ColonyHub = ColonyHub(name="Olympus Base");

walker ColonyBuilder {
    can build with entry {
        # Create main hub
        hub = ColonyHub(name="Olympus Base", x=0.0, y=0.0);
        root ++> hub;
        
        # Create habitats
        hab1 = Habitat(name="Habitat Alpha", x=-2.0, y=1.0, occupied=3, dispute_level=20);
        hab2 = Habitat(name="Habitat Beta", x=2.0, y=1.0, occupied=2, dispute_level=45);
        hub ++> hab1;
        hub ++> hab2;
        
        # Create facilities
        power = PowerPlant(name="Solar Array 1", x=0.0, y=3.0);
        greenhouse = Greenhouse(name="Greenhouse Dome", x=-3.0, y=-2.0);
        mine = MiningStation(name="Mining Outpost Delta", x=4.0, y=-3.0);
        lab = ResearchLab(name="Research Lab Gamma", x=3.0, y=3.0);
        
        hub +[PowerLine(capacity=50)]+> power;
        hub +[SupplyRoute(distance=100)]+> greenhouse;
        hub +[SupplyRoute(distance=500)]+> mine;
        hub +[DataLink(bandwidth=100)]+> lab;
        
        # Peace infrastructure
        mediation = MediationCenter(
            name="Peace Center",
            x=-4.0,
            y=2.0,
            active_disputes=["Food rationing protest", "Work shift conflict"]
        );
        hub ++> mediation;
        
        # Trade post
        trade = TradePost(name="Central Trade Hub", x=1.0, y=-1.0);
        hub +[TradeRoute(established=True, trust_level=70)]+> trade;
        
        # Rebel camps
        rebel1 = RebelCamp(
            name="Freedom Crater",
            x=-8.0,
            y=-5.0,
            population=8,
            ideology="independence",
            hostility=55,
            demands=["Self-governance", "Fair resource share"]
        );
        
        rebel2 = RebelCamp(
            name="Survivor's Ridge",
            x=7.0,
            y=-7.0,
            population=6,
            ideology="survival",
            hostility=70,
            demands=["Medicine access", "Water rights"]
        );
        
        hub +[SupplyRoute(distance=1000, danger_level=60)]+> rebel1;
        hub +[SupplyRoute(distance=1500, danger_level=80)]+> rebel2;
        
        # Scavenger outpost
        scav = ScavengerOutpost(
            name="Rust Valley",
            x=5.0,
            y=6.0,
            scavengers=5,
            trade_preference="food"
        );
        hub +[SupplyRoute(distance=800)]+> scav;
        
        # Neutral zone
        neutral = NeutralZone(name="Deimos Trading Post", x=0.0, y=-6.0, safety_level=75);
        hub +[TradeRoute(established=True)]+> neutral;
        rebel1 +[TradeRoute(established=False, trust_level=30)]+> neutral;
        trade ++> neutral;
        
        # Store hub globally
        global colony_graph = hub;
    }
}

# ==================== STREAMLIT INTEGRATION ====================

glob st_initialized: bool = False;

walker StreamlitApp {
    can run_app with entry {
        # Build colony if not exists
        if not st_initialized {
            builder = ColonyBuilder();
            root spawn builder;
            glob st_initialized = True;
        }
        
        # Extract current state
        extractor = StateExtractor();
        hub spawn extractor;
        state = extractor.colony_state;
        
        # Display in Streamlit
        st.title("🔴 Mars Colony Control Center");
        
        # Create columns
        col1, col2 = st.columns([2, 1]);
        
        with col1 {
            st.subheader("🗺️ Colony Map");
            # Map would be rendered here via Python
        }
        
        with col2 {
            st.subheader("📊 Colony Status");
            hub_data = state["hub"];
            st.metric("Population", hub_data["population"]);
            st.metric("Power", f"{hub_data['power']}%");
            st.metric("Food", hub_data["food"]);
            st.metric("Water", hub_data["water"]);
            st.metric("Morale", f"{hub_data['morale']}%");
        }
    }
}

# ==================== ENTRY POINT ====================

with entry {
    print("🔴 Mars Colony Simulation - Streamlit Integration Ready");
    print("="*60);
    
    # Build the colony
    builder = ColonyBuilder();
    root spawn builder;
    
    print("✅ Colony graph constructed");
    print("✅ Ready for Streamlit connection");
    print("\nRun: streamlit run mars_app.py");
}