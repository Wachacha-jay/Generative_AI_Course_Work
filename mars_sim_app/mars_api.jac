"""
Mars Colony API Server using JAC Serve
Provides REST API endpoints for Streamlit frontend
"""

import walkers
import json

# ==================== API WALKERS ====================

walker ColonyAPI {
    has response: dict = {};
    
    can get_colony_state with entry {
        # Extract current state
        extractor = walkers.StateExtractor();
        root spawn extractor;
        self.response = {
            "status": "success",
            "data": extractor.colony_state
        };
    }
    
    can advance_day with entry {
        # Simulate a day
        simulator = walkers.DaySimulator();
        root spawn simulator;
        self.response = {
            "status": "success",
            "events": simulator.events,
            "message": "Day advanced successfully"
        };
    }
    
    can send_diplomat with entry {
        target = ctx.request.get("target", "Freedom Crater");
        diplomat = walkers.DiplomatAction(target_camp=target);
        root spawn diplomat;
        self.response = {
            "status": "success" if diplomat.success else "failed",
            "message": f"Diplomat {'successfully' if diplomat.success else 'failed to'} negotiate with {target}"
        };
    }
    
    can trade_resources with entry {
        trade_type = ctx.request.get("trade_type", "food");
        amount = ctx.request.get("amount", 10);
        trader = walkers.TradeAction(trade_type=trade_type, amount=amount);
        root spawn trader;
        self.response = {
            "status": "success" if trader.success else "failed",
            "message": f"Trade {'successful' if trader.success else 'failed'}: {trade_type}"
        };
    }
    
    can resolve_dispute with entry {
        habitat = ctx.request.get("habitat", "Habitat Alpha");
        resolver = walkers.DisputeResolver(target_habitat=habitat);
        root spawn resolver;
        self.response = {
            "status": "success" if resolver.resolved else "failed",
            "message": f"Dispute at {habitat} {'resolved' if resolver.resolved else 'not resolved'}"
        };
    }
    
    can mine_resources with entry {
        miner = walkers.MiningAction();
        root spawn miner;
        self.response = {
            "status": "success",
            "resources_gained": miner.resource_gained,
            "message": f"Mined {miner.resource_gained} units of resources"
        };
    }
}

# ==================== API ROUTES ====================

walker APIRouter {
    can route with entry {
        endpoint = ctx.request.get("endpoint", "");
        method = ctx.request.get("method", "GET");
        
        api = ColonyAPI();
        
        if endpoint == "state" and method == "GET":
            api.get_colony_state();
        elif endpoint == "advance_day" and method == "POST":
            api.advance_day();
        elif endpoint == "diplomat" and method == "POST":
            api.send_diplomat();
        elif endpoint == "trade" and method == "POST":
            api.trade_resources();
        elif endpoint == "dispute" and method == "POST":
            api.resolve_dispute();
        elif endpoint == "mine" and method == "POST":
            api.mine_resources();
        else:
            api.response = {
                "status": "error",
                "message": f"Unknown endpoint: {endpoint}"
            };
        
        # Return JSON response
        ctx.response = json.dumps(api.response);
    }
}

# ==================== SERVER CONFIGURATION ====================

walker MarsServer {
    can serve with entry {
        print("🔴 Mars Colony API Server Starting...");
        print("="*50);
        print("Available endpoints:");
        print("  GET  /state        - Get colony state");
        print("  POST /advance_day  - Advance simulation by one day");
        print("  POST /diplomat     - Send diplomat to rebel camp");
        print("  POST /trade        - Trade resources");
        print("  POST /dispute      - Resolve habitat dispute");
        print("  POST /mine         - Mine resources");
        print("="*50);
        
        # Initialize colony if not exists
        if not walkers.st_initialized {
            builder = walkers.ColonyBuilder();
            root spawn builder;
            walkers.st_initialized = True;
        }
        
        # Start API server
        router = APIRouter();
        root spawn router;
    }
}

with entry {
    server = MarsServer();
    root spawn server;
}