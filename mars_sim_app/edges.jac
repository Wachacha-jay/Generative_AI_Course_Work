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