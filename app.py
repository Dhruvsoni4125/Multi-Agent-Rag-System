import streamlit as st
import os
from pipeline import run_research_pipeline
from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv()

# Map Gemini_API_KEY to GOOGLE_API_KEY for LangChain if necessary
if "Gemini_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["Gemini_API_KEY"]

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 Multi-Agent RAG Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter a topic. The system will search the web, scrape articles, compile a report, and critique it.</div>', unsafe_allow_html=True)

topic = st.text_input("What would you like to research?", placeholder="e.g., Advancements in Quantum Computing")

if st.button("Start Agent Collaboration", type="primary"):
    if not topic.strip():
        st.error("Please enter a research topic first.")
    else:
        # Visual collaboration status
        with st.status("Agents are collaborating...", expanded=True) as status_box:
            st.write("🔍 Search Agent: Searching the web via Tavily...")
            
            # Run the research pipeline
            try:
                result = run_research_pipeline(topic)
                status_box.update(label="Research Complete!", state="complete", expanded=False)
                st.success("Research completed successfully!")
                
                # Show results in nice clean tabs
                tab1, tab2, tab3 = st.tabs(["📄 Final Report", "⭐ Critic Review", "🔧 Technical Data"])
                
                with tab1:
                    st.markdown("### Drafted Report")
                    st.markdown(result.get("report", "No report generated."))
                    
                with tab2:
                    st.markdown("### Critic Score and Feedback")
                    st.markdown(result.get("feedback", "No feedback generated."))
                    
                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Web Search Output")
                        st.code(result.get("search_results", "None"))
                    with col2:
                        st.subheader("Scraped Content Summary")
                        st.code(result.get("scraped_content", "None"))
            except Exception as e:
                status_box.update(label="Pipeline Failed", state="error")
                st.error(f"Error executing pipeline: {str(e)}")
