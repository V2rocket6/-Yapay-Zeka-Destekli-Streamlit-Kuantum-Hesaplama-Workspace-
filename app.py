import streamlit as st
import numpy as np
import time
import quantum_engine as qe

st.set_page_config(
    page_title="QuantumVQE.AI",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title { font-size: 2.6rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.1rem; }
    .subtitle { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚛️ QuantumVQE.AI: AI-Driven Quantum Simulation Workspace</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">An Interactive Optimization and Error Mitigation Tool for Hybrid VQE Algorithms using Streamlit</div>', unsafe_allow_html=True)
st.markdown("---")

st.sidebar.markdown("### 🛠️ Configuration Panel")

molecule_choice = st.sidebar.selectbox(
    "1. Target Molecular System:",
    options=["H2 (Hydrogen)", "LiH (Lithium Hydride)"]
)

optimizer_choice = st.sidebar.selectbox(
    "2. Classical Optimizer (Loop Control):",
    options=["COBYLA (Analytical/Stable)", "SLSQP (Gradient-based)", "SPSA (Simultaneous Perturbation)"]
)

noise_choice = st.sidebar.selectbox(
    "3. Hardware Noise Environment:",
    options=["Ideal (No Noise)", "ibm_brisbane (Noisy Profile)", "ibm_kyoto (Noisy Profile)"]
)

ai_assist = st.sidebar.toggle("💡 Activate AI-Driven Parameter Initialization", value=True)
st.sidebar.markdown("---")
st.sidebar.caption("Developed by Büşra Şahinal - Marine Engineer & AI Researcher")

meta = qe.get_molecule_metadata(molecule_choice)
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📋 Quantum Mapping & System Status")
    with st.container():
        st.info(f"**Target System:** {molecule_choice}")
        st.markdown(f"""
        *   **Basis Set:** `{meta['basis_set']}`
        *   **Active Electrons:** `{meta['electrons']}`
        *   **Mapped Qubits:** `{meta['qubits']} Qubits`
        *   **Transformation:** `{meta['mapper']}`
        *   **Ansatz Architecture:** `{meta['ansatz']}`
        """)
        
    st.markdown("### 🤖 Classical AI Layer Status")
    if ai_assist:
        st.success("🧠 **AI Regression Model: ACTIVE**\n\nInitial variational parameters (θ) are dynamically predicted using models trained on topological data from prior molecular matrices.")
    else:
        st.warning("⚠️ **Standard Initialization: ACTIVE**\n\nRandom angle distributions will be applied.")

    run_button = st.button("🚀 Run AI-Quantum Pipeline", type="primary", use_container_width=True)

with col2:
    st.markdown("### 📊 Live Convergence & Performance Analytics")
    if run_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        chart_placeholder = st.empty()
        
        sim_loop = qe.run_vqe_simulation(molecule_choice, optimizer_choice, noise_choice, ai_assist)
        for iteration, max_iter, current_energy, history in sim_loop:
            chart_placeholder.line_chart(history)
            progress_bar.progress(int((iteration / max_iter) * 100))
            status_text.markdown(f"**Iteration:** `{iteration}/{max_iter}` | **Current Energy:** `{current_energy:.6f} Ha`")
            
        progress_bar.empty()
        status_text.success("✅ VQE Execution Pipeline Finished Successfully!")
        metrics = qe.calculate_final_metrics(history, meta["ideal_vqe"], ai_assist, meta["max_iter_standard"])
        
        st.markdown("#### 🎯 Execution Performance Output")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Calculated VQE Energy", f"{metrics['final_energy']:.4f} Ha")
            st.caption(f"Hartree-Fock Baseline: {meta['hf_energy']:.4f} Ha")
        with m_col2:
            st.metric("Mean Absolute Error (MAE)", f"{metrics['mae']:.5f} Ha", delta="Within Chemical Accuracy" if metrics['mae'] < 0.0016 else "Noisy Deviation", delta_color="inverse")
            st.caption(f"MSE: {metrics['mse']:.2e}")
        with m_col3:
            st.metric("Convergence Speedup", metrics['acceleration'])
            st.caption(f"Efficiency Gain: {metrics['efficiency']}")
    else:
        st.info("Awaiting pipeline execution. Configure the system parameters on the sidebar and click the button to visualize real-time quantum convergence.")
