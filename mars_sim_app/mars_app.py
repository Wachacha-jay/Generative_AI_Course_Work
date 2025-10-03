"""
Mars Colony Streamlit Application
Connects to Jac backend and provides interactive UI
Run: streamlit run mars_app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from jaclang import jac
import sys
import os

# Page configuration
st.set_page_config(
    page_title="Mars Colony Control Center",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #1a0f0f;
    }
    .stApp {
        background: linear-gradient(to bottom, #2d1b1b, #1a0f0f);
    }
    h1, h2, h3 {
        color: #ff6b4a;
    }
    .stMetric {
        background-color: rgba(45, 27, 27, 0.5);
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ff6b4a;
    }
    .stButton>button {
        background-color: #ff6b4a;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff8566;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Jac module
@st.cache_resource
def load_jac_module():
    """Load the Jac colony simulation module"""
    try:
        # Import the Jac module - adjust path as needed
        jac_module = jac.load_module("colony_simulation.jac")
        return jac_module
    except Exception as e:
        st.error(f"Failed to load Jac module: {e}")
        return None

# Initialize colony state
def initialize_colony(jac_module):
    """Initialize the colony graph"""
    if 'colony_initialized' not in st.session_state:
        # The Jac entry point builds the colony
        st.session_state.colony_initialized = True
        st.session_state.day = 1
        st.session_state.events_log = []
    return True

# Extract state from Jac graph
def get_colony_state(jac_module):
    """Extract current colony state from Jac graph"""
    try:
        # Create and spawn state extractor walker
        extractor = jac_module.StateExtractor()
        # The walker traverses the graph and collects data
        state = extractor.colony_state
        return state
    except Exception as e:
        st.error(f"Failed to extract state: {e}")
        return None

# Execute actions via Jac walkers
def execute_action(jac_module, action_type, params=None):
    """Execute a game action using Jac walkers"""
    try:
        if action_type == "advance_day":
            walker = jac_module.DaySimulator()
            # Spawn walker to simulate a day
            events = walker.events if hasattr(walker, 'events') else []
            st.session_state.day += 1
            st.session_state.events_log.extend(events)
            return True
        
        elif action_type == "send_diplomat":
            target = params.get('target', 'Freedom Crater')
            walker = jac_module.DiplomatAction(target_camp=target)
            # Walker negotiates with rebel camp
            success = walker.success if hasattr(walker, 'success') else False
            if success:
                st.session_state.events_log.append(f"🕊️ Diplomat reduced tension with {target}")
            return success
        
        elif action_type == "trade":
            trade_type = params.get('trade_type', 'food')
            walker = jac_module.TradeAction(trade_type=trade_type, amount=10)
            success = walker.success if hasattr(walker, 'success') else False
            if success:
                st.session_state.events_log.append(f"💱 Traded for {trade_type}")
            return success
        
        elif action_type == "resolve_dispute":
            habitat = params.get('habitat', 'Habitat Alpha')
            walker = jac_module.DisputeResolver(target_habitat=habitat)
            resolved = walker.resolved if hasattr(walker, 'resolved') else False
            if resolved:
                st.session_state.events_log.append(f"✅ Resolved dispute at {habitat}")
            return resolved
        
        elif action_type == "mine":
            walker = jac_module.MiningAction()
            gained = walker.resource_gained if hasattr(walker, 'resource_gained') else 0
            if gained > 0:
                st.session_state.events_log.append(f"⛏️ Mined {gained} units of water ice")
            return True
        
        return False
    except Exception as e:
        st.error(f"Action failed: {e}")
        return False

# Create Mars map visualization
def create_mars_map(state):
    """Create interactive Plotly map of Mars colony"""
    fig = go.Figure()
    
    # Add Mars surface texture
    fig.add_shape(
        type="circle",
        x0=-10, y0=-10, x1=10, y1=10,
        fillcolor="rgba(139, 69, 19, 0.1)",
        line=dict(color="rgba(255, 107, 74, 0.2)", width=2)
    )
    
    # Colony Hub (center)
    hub = state.get('hub', {})
    if hub:
        fig.add_trace(go.Scatter(
            x=[hub.get('x', 0)],
            y=[hub.get('y', 0)],
            mode='markers+text',
            name='Colony Hub',
            text=['🏛️'],
            textfont=dict(size=30),
            textposition='middle center',
            marker=dict(
                size=50,
                color='#4a90e2',
                symbol='star',
                line=dict(width=3, color='white')
            ),
            hovertemplate=f'<b>Olympus Base</b><br>' +
                         f'Power: {hub.get("power", 0)}%<br>' +
                         f'Food: {hub.get("food", 0)}<br>' +
                         f'Morale: {hub.get("morale", 0)}%<extra></extra>'
        ))
    
    # Habitats
    habitats = state.get('habitats', [])
    if habitats:
        hab_x = [h['x'] for h in habitats]
        hab_y = [h['y'] for h in habitats]
        hab_disputes = [h['dispute_level'] for h in habitats]
        hab_names = [h['name'] for h in habitats]
        
        fig.add_trace(go.Scatter(
            x=hab_x, y=hab_y,
            mode='markers+text',
            name='Habitats',
            text=['🏠' for _ in habitats],
            textfont=dict(size=20),
            textposition='top center',
            marker=dict(
                size=30,
                color=hab_disputes,
                colorscale=[[0, '#4ade80'], [0.5, '#fbbf24'], [1, '#ef4444']],
                showscale=True,
                colorbar=dict(title="Dispute<br>Level", x=1.15),
                line=dict(width=2, color='white'),
                cmin=0,
                cmax=100
            ),
            customdata=hab_names,
            hovertemplate='<b>%{customdata}</b><br>Dispute: %{marker.color:.0f}%<extra></extra>'
        ))
        
        # Connect habitats to hub
        for hab in habitats:
            fig.add_trace(go.Scatter(
                x=[0, hab['x']],
                y=[0, hab['y']],
                mode='lines',
                line=dict(color='rgba(74, 144, 226, 0.3)', width=2, dash='dot'),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Facilities
    facility_icons = {
        'power': '⚡',
        'food': '🌱',
        'mining': '⛏️',
        'research': '🔬',
        'mediation': '🕊️'
    }
    
    facilities = state.get('facilities', [])
    for facility in facilities:
        icon = facility_icons.get(facility.get('type', ''), '🏭')
        fig.add_trace(go.Scatter(
            x=[facility['x']],
            y=[facility['y']],
            mode='markers+text',
            name=facility['name'],
            text=[icon],
            textfont=dict(size=18),
            textposition='top center',
            marker=dict(size=25, color='#a78bfa', line=dict(width=2, color='white')),
            hovertemplate=f'<b>{facility["name"]}</b><br>Type: {facility.get("type", "unknown")}<extra></extra>'
        ))
        
        # Connect to hub
        fig.add_trace(go.Scatter(
            x=[0, facility['x']],
            y=[0, facility['y']],
            mode='lines',
            line=dict(color='rgba(167, 139, 250, 0.3)', width=1, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Rebel Camps
    rebels = state.get('rebel_camps', [])
    if rebels:
        rebel_x = [r['x'] for r in rebels]
        rebel_y = [r['y'] for r in rebels]
        rebel_names = [r['name'] for r in rebels]
        rebel_hostility = [r['hostility'] for r in rebels]
        
        fig.add_trace(go.Scatter(
            x=rebel_x, y=rebel_y,
            mode='markers+text',
            name='Rebel Camps',
            text=['🏴' for _ in rebels],
            textfont=dict(size=20),
            textposition='top center',
            marker=dict(
                size=30,
                color=rebel_hostility,
                colorscale='Reds',
                symbol='diamond',
                line=dict(width=2, color='white'),
                cmin=0,
                cmax=100
            ),
            customdata=rebel_names,
            hovertemplate='<b>%{customdata}</b><br>Hostility: %{marker.color:.0f}%<extra></extra>'
        ))
    
    # Scavenger Outposts
    scavengers = state.get('scavenger_outposts', [])
    if scavengers:
        scav_x = [s['x'] for s in scavengers]
        scav_y = [s['y'] for s in scavengers]
        
        fig.add_trace(go.Scatter(
            x=scav_x, y=scav_y,
            mode='markers+text',
            name='Scavenger Outposts',
            text=['🔍' for _ in scavengers],
            textfont=dict(size=18),
            textposition='top center',
            marker=dict(size=25, color='#f59e0b', symbol='square', line=dict(width=2, color='white')),
            hovertemplate='<b>Rust Valley</b><br>Scavengers: 5<extra></extra>'
        ))
    
    # Neutral Zones
    neutral = state.get('neutral_zones', [])
    if neutral:
        neutral_x = [n['x'] for n in neutral]
        neutral_y = [n['y'] for n in neutral]
        
        fig.add_trace(go.Scatter(
            x=neutral_x, y=neutral_y,
            mode='markers+text',
            name='Neutral Zones',
            text=['🤝' for _ in neutral],
            textfont=dict(size=20),
            textposition='top center',
            marker=dict(size=30, color='#10b981', symbol='hexagon', line=dict(width=2, color='white')),
            hovertemplate='<b>Deimos Trading Post</b><br>Safety: 75%<extra></extra>'
        ))
    
    # Layout
    fig.update_layout(
        title=dict(
            text=f'🔴 Mars Colony Map - Sol {st.session_state.day}',
            font=dict(size=26, color='#ff6b4a'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#0f0505',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 107, 74, 0.1)',
            zeroline=False,
            showticklabels=False,
            range=[-10, 10]
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 107, 74, 0.1)',
            zeroline=False,
            showticklabels=False,
            range=[-10, 10],
            scaleanchor='x',
            scaleratio=1
        ),
        height=650,
        hovermode='closest',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(45, 27, 27, 0.8)',
            bordercolor='#ff6b4a',
            borderwidth=2,
            font=dict(color='white'),
            x=1.02,
            y=1
        )
    )
    
    return fig

# Main Application
def main():
    """Main Streamlit application"""
    
    # Load Jac module
    jac_module = load_jac_module()
    if not jac_module:
        st.error("❌ Failed to load Jac module. Please check the file path.")
        return
    
    # Initialize colony
    initialize_colony(jac_module)
    
    # Title
    st.title("🔴 Mars Colony Control Center")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Colony Operations")
        st.markdown(f"**Sol (Day):** {st.session_state.day}")
        
        st.markdown("---")
        st.subheader("🕹️ Time Controls")
        
        if st.button("▶️ Advance Day", use_container_width=True, type="primary"):
            execute_action(jac_module, "advance_day")
            st.rerun()
        
        if st.button("🔄 Reset Colony", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.subheader("🎯 Colony Actions")
        
        action = st.selectbox("Select Action", [
            "Send Diplomat",
            "Trade with Rebels",
            "Resolve Dispute",
            "Mine Resources",
            "Research Technology"
        ])
        
        # Action-specific parameters
        params = {}
        if action == "Send Diplomat":
            params['target'] = st.selectbox("Target Camp", ["Freedom Crater", "Survivor's Ridge"])
        elif action == "Trade with Rebels":
            params['trade_type'] = st.selectbox("Trade For", ["food", "medicine", "tech"])
        elif action == "Resolve Dispute":
            params['habitat'] = st.selectbox("Target Habitat", ["Habitat Alpha", "Habitat Beta"])
        
        if st.button("🚀 Execute Action", use_container_width=True, type="secondary"):
            success = False
            if action == "Send Diplomat":
                success = execute_action(jac_module, "send_diplomat", params)
            elif action == "Trade with Rebels":
                success = execute_action(jac_module, "trade", params)
            elif action == "Resolve Dispute":
                success = execute_action(jac_module, "resolve_dispute", params)
            elif action == "Mine Resources":
                success = execute_action(jac_module, "mine")
            elif action == "Research Technology":
                st.session_state.events_log.append("🔬 Research project initiated")
                success = True
            
            if success:
                st.success("✅ Action completed!")
            else:
                st.warning("⚠️ Action had no effect")
            st.rerun()
        
        st.markdown("---")
        st.subheader("📖 Quick Guide")
        st.caption("""
        **Map Legend:**
        - 🏛️ Colony Hub (Center)
        - 🏠 Habitats (Green=Peaceful, Red=Conflict)
        - ⚡ Power Plants
        - 🌱 Greenhouses
        - ⛏️ Mining Stations
        - 🔬 Research Labs
        - 🏴 Rebel Camps
        - 🔍 Scavenger Outposts
        - 🤝 Neutral Zones
        """)
    
    # Get current state
    state = get_colony_state(jac_module)
    if not state:
        st.error("❌ Failed to retrieve colony state")
        return
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗺️ Interactive Colony Map")
        st.plotly_chart(create_mars_map(state), use_container_width=True)
    
    with col2:
        st.subheader("📊 Colony Status")
        
        hub = state.get('hub', {})
        
        # Resource metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("👥 Population", hub.get('population', 0))
            st.metric("⚡ Power", f"{hub.get('power', 0)}%")
            st.metric("🍖 Food", hub.get('food', 0))
        
        with col_b:
            st.metric("💧 Water", hub.get('water', 0))
            st.metric("💊 Medicine", hub.get('medicine', 0))
            st.metric("😊 Morale", f"{hub.get('morale', 0)}%")
        
        # Critical alerts
        st.markdown("---")
        st.subheader("🚨 Status Alerts")
        
        alerts = []
        if hub.get('power', 100) < 30:
            alerts.append("🔴 **CRITICAL:** Power levels dangerously low!")
        if hub.get('food', 100) < 20:
            alerts.append("🟠 **WARNING:** Food shortage imminent!")
        if hub.get('morale', 100) < 40:
            alerts.append("🟡 **ALERT:** Morale crisis - rebellion risk!")
        if hub.get('water', 100) < 25:
            alerts.append("🔵 **CAUTION:** Water reserves running low!")
        
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("✅ All systems nominal")
        
        # Faction status
        st.markdown("---")
        st.subheader("🏴 Faction Relations")
        
        rebels = state.get('rebel_camps', [])
        for rebel in rebels:
            hostility = rebel.get('hostility', 0)
            if hostility < 40:
                threat = "🟢 Low"
                color = "normal"
            elif hostility < 70:
                threat = "🟡 Medium"
                color = "normal"
            else:
                threat = "🔴 High"
                color = "normal"
            
            st.write(f"**{rebel.get('name', 'Unknown')}:** {threat}")
            st.progress(hostility / 100)
            st.caption(f"Ideology: {rebel.get('ideology', 'unknown')}")
    
    # Bottom section - Events and Detailed Info
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📰 Recent Events", "🏘️ Facilities", "👥 Population"])
    
    with tab1:
        st.subheader("📰 Colony Event Log")
        events = st.session_state.events_log[-10:] if st.session_state.events_log else ["No events recorded yet"]
        for i, event in enumerate(reversed(events)):
            st.text(f"Sol {max(1, st.session_state.day - i)}: {event}")
    
    with tab2:
        st.subheader("🏘️ Facility Status")
        
        facilities = state.get('facilities', [])
        if facilities:
            for facility in facilities:
                with st.expander(f"{facility.get('name', 'Unknown')} - {facility.get('type', 'unknown').upper()}"):
                    if facility.get('type') == 'power':
                        st.metric("Output", f"{facility.get('output', 0)}W")
                        st.metric("Efficiency", f"{facility.get('efficiency', 0)}%")
                        st.metric("Fuel", f"{facility.get('fuel', 0)} units")
                    elif facility.get('type') == 'food':
                        st.metric("Production", f"{facility.get('production', 0)} units/day")
                        st.metric("Crops Growing", facility.get('crops', 0))
                    elif facility.get('type') == 'mining':
                        st.write("**Resources Extracted:**")
                        resources = facility.get('resources', {})
                        for resource, amount in resources.items():
                            st.text(f"  • {resource.capitalize()}: {amount}")
                    elif facility.get('type') == 'research':
                        st.metric("Tech Level", facility.get('tech_level', 1))
                        st.metric("Active Projects", facility.get('projects', 0))
        else:
            st.info("No facilities data available")
        
        # Habitats
        st.markdown("---")
        st.subheader("🏠 Habitat Conditions")
        habitats = state.get('habitats', [])
        for habitat in habitats:
            dispute = habitat.get('dispute_level', 0)
            if dispute < 30:
                status = "✅ Peaceful"
            elif dispute < 70:
                status = "⚠️ Tense"
            else:
                status = "🚨 Critical Conflict"
            
            with st.expander(f"{habitat.get('name', 'Unknown')} - {status}"):
                st.metric("Occupancy", f"{habitat.get('occupied', 0)}/{habitat.get('capacity', 10)}")
                st.metric("Comfort Level", f"{habitat.get('comfort', 0)}%")
                st.progress(dispute / 100, text=f"Dispute Level: {dispute}%")
    
    with tab3:
        st.subheader("👥 Population Overview")
        
        col_pop1, col_pop2, col_pop3 = st.columns(3)
        
        with col_pop1:
            st.metric("Total Population", hub.get('population', 0))
            occupied = sum(h.get('occupied', 0) for h in state.get('habitats', []))
            st.metric("Living in Habitats", occupied)
        
        with col_pop2:
            rebel_pop = sum(r.get('population', 0) for r in state.get('rebel_camps', []))
            st.metric("Rebels", rebel_pop)
            scav_pop = sum(s.get('scavengers', 0) for s in state.get('scavenger_outposts', []))
            st.metric("Scavengers", scav_pop)
        
        with col_pop3:
            total = hub.get('population', 0) + rebel_pop + scav_pop
            st.metric("Total Mars Population", total)
            loyalty = hub.get('faction_loyalty', 'united')
            st.metric("Colony Loyalty", loyalty.capitalize())
        
        st.markdown("---")
        st.write("**Faction Distribution:**")
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Colony', 'Rebels', 'Scavengers'],
            values=[hub.get('population', 0), rebel_pop, scav_pop],
            hole=.3,
            marker=dict(colors=['#4a90e2', '#ef4444', '#f59e0b'])
        )])
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.caption("🚀 Mars Colony Simulation | Powered by Jac Language | Interactive Graph-Based Gaming")

if __name__ == "__main__":
    main()