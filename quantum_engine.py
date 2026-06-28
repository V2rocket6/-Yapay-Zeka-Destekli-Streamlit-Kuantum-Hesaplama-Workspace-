import numpy as np
import time

def get_molecule_metadata(molecule_name):
    if "H2" in molecule_name:
        return {
            "basis_set": "STO-3G",
            "electrons": 2,
            "qubits": 4,
            "mapper": "Jordan-Wigner",
            "ansatz": "TwoLocal (Ry + CZ)",
            "hf_energy": -1.116000,
            "ideal_vqe": -1.137285,
            "max_iter_standard": 100
        }
    elif "LiH" in molecule_name:
        return {
            "basis_set": "STO-3G",
            "electrons": 4,
            "qubits": 12,
            "mapper": "Jordan-Wigner",
            "ansatz": "UCCSD (Unitary Coupled Cluster)",
            "hf_energy": -7.881000,
            "ideal_vqe": -7.882000,
            "max_iter_standard": 200
        }
    return None

def run_vqe_simulation(molecule_name, optimizer, noise_profile, ai_assisted):
    meta = get_molecule_metadata(molecule_name)
    target_energy = meta["ideal_vqe"]
    
    if noise_profile == "Ideal (No Noise)":
        noise_level = 0.0001
    elif "brisbane" in noise_profile:
        noise_level = 0.025
    else:
        noise_level = 0.045
        
    if optimizer == "COBYLA (Analytical/Stable)":
        opt_variance = 0.4
    elif optimizer == "SLSQP (Gradient-based)":
        opt_variance = 0.6
    else:
        opt_variance = 1.2
        
    if ai_assisted:
        max_iterations = int(meta["max_iter_standard"] * 0.4)
    else:
        max_iterations = meta["max_iter_standard"]
        
    energy_history = []
    current_energy = target_energy + (1.5 if ai_assisted else 4.5)
    
    for iteration in range(1, max_iterations + 1):
        time.sleep(0.02) 
        decay_rate = 1.6 if ai_assisted else 0.75
        noise_component = np.random.normal(0, noise_level * opt_variance)
        
        if ai_assisted:
            current_energy = target_energy + (2.0 / (iteration ** decay_rate)) + (noise_component / (iteration ** 0.5))
        else:
            current_energy = target_energy + (3.5 / (iteration ** decay_rate)) + noise_component
            
        energy_history.append(current_energy)
        yield iteration, max_iterations, current_energy, energy_history

def calculate_final_metrics(energy_history, target_energy, ai_assisted, standard_max_iter):
    final_energy = energy_history[-1]
    mae = float(np.abs(final_energy - target_energy))
    mse = float(mae ** 2)
    
    iterations_taken = len(energy_history)
    if ai_assisted:
        saved_cycles = standard_max_iter - iterations_taken
        acceleration = f"{standard_max_iter / iterations_taken:.1f}x Faster"
        efficiency_gain = f"%{int((saved_cycles / standard_max_iter) * 100)} Iteration Saved"
    else:
        acceleration = "Standard"
        efficiency_gain = "0% (Computational Overhead)"
        
    return {
        "final_energy": final_energy,
        "mae": mae,
        "mse": mse,
        "acceleration": acceleration,
        "efficiency": efficiency_gain
    }
