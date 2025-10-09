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
    has ideology: str;
    has population: int = 8;
    has resources: dict = {"food": 15, "water": 20, "weapons": 5, "salvage": 30};
    has hostility: int = 50;
    has demands: list = [];
}

node ScavengerOutpost {
    has name: str;
    has x: float;
    has y: float;
    has trade_preference: str;
    has scavengers: int = 5;
    has salvage_quality: str = "mixed";
    has discovered_items: list = [];
}

node NeutralZone {
    has name: str;
    has x: float;
    has y: float;
    has safety_level: int = 70;
    has factions_present: list = [];
}
