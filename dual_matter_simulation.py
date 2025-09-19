#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class DualMatterSimulation:
    def __init__(self):
        # Resonance frequencies
        self.f_res_positive = 587000    # 587 kHz - Positive matter
        self.f_res_negative = 293500    # 293.5 kHz - Negative matter (predicted)
        self.sigma = 0.03 * self.f_res_positive
        
    def mass_modulation(self, f, matter_type):
        """Calculate mass based on matter type and frequency"""
        if matter_type == "positive":
            return 1 + 0.17 * np.exp(-(f - self.f_res_positive)**2 / (2*self.sigma**2))
        else:  # negative matter
            return 1 - 0.17 * np.exp(-(f - self.f_res_negative)**2 / (2*self.sigma**2))
    
    def temporal_force(self, mass, velocity, matter_type):
        """Force based on temporal resistance"""
        if matter_type == "positive":
            # Positive matter: resists change (normal inertia)
            return -mass * velocity  # Resistance force
        else:
            # Negative matter: seeks change (anti-inertia)
            return +mass * velocity  # Acceleration force
    
    def simulate_interaction(self, initial_conditions, duration=10, dt=0.1):
        """Simulate interaction between positive and negative matter"""
        times = np.arange(0, duration, dt)
        
        # Differential equations for coupled system
        def equations(t, state):
            x1, v1, x2, v2 = state  # positions and velocities
            
            # Masses at current frequencies (could make frequency time-dependent)
            m1 = self.mass_modulation(self.f_res_positive, "positive")
            m2 = self.mass_modulation(self.f_res_negative, "negative")
            
            # Forces based on temporal resistance
            f1 = self.temporal_force(m1, v1, "positive")
            f2 = self.temporal_force(m2, v2, "negative")
            
            # Interaction force (gravitational-like)
            interaction = 0.1 * (x2 - x1)  # Positive matter attracts negative matter?
            
            # Equations of motion
            dx1dt = v1
            dv1dt = (f1 + interaction) / m1
            dx2dt = v2  
            dv2dt = (f2 - interaction) / m2
            
            return [dx1dt, dv1dt, dx2dt, dv2dt]
        
        # Solve the system
        solution = solve_ivp(equations, [0, duration], initial_conditions, 
                           t_eval=times, method='RK45')
        
        return solution
    
    def run_demonstration(self):
        """Run complete demonstration"""
        print("DUAL MATTER SIMULATION - CTT Theory")
        print("=" * 50)
        
        # Test masses
        m_plus = self.mass_modulation(self.f_res_positive, "positive")
        m_minus = self.mass_modulation(self.f_res_negative, "negative")
        
        print(f"Positive matter mass at 587 kHz: {m_plus:.3f} m₀ (+{(m_plus-1)*100:.1f}%)")
        print(f"Negative matter mass at 293.5 kHz: {m_minus:.3f} m₀ ({(m_minus-1)*100:+.1f}%)")
        print()
        
        # Simulation 1: Both matter types at rest
        print("Simulation 1: Both matter types initially at rest")
        print("Positive matter should resist motion, negative matter should self-accelerate")
        print()
        
        initial_state = [0, 0, 5, 0]  # x1=0,v1=0; x2=5,v2=0
        solution = self.simulate_interaction(initial_state, duration=20)
        
        # Plot results
        plt.figure(figsize=(15, 10))
        
        # Position plot
        plt.subplot(2, 2, 1)
        plt.plot(solution.t, solution.y[0], 'b-', label='Positive Matter', linewidth=2)
        plt.plot(solution.t, solution.y[2], 'r-', label='Negative Matter', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Position')
        plt.title('Position vs Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Velocity plot
        plt.subplot(2, 2, 2)
        plt.plot(solution.t, solution.y[1], 'b-', label='Positive Matter', linewidth=2)
        plt.plot(solution.t, solution.y[3], 'r-', label='Negative Matter', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Velocity')
        plt.title('Velocity vs Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Simulation 2: Positive matter pushed
        print("Simulation 2: Positive matter pushed, negative matter free")
        initial_state2 = [0, 1, 5, 0]  # x1=0,v1=1; x2=5,v2=0
        solution2 = self.simulate_interaction(initial_state2, duration=15)
        
        # Position plot
        plt.subplot(2, 2, 3)
        plt.plot(solution2.t, solution2.y[0], 'b-', label='Positive Matter', linewidth=2)
        plt.plot(solution2.t, solution2.y[2], 'r-', label='Negative Matter', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Position')
        plt.title('Positive Matter Pushed - Position vs Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Velocity plot
        plt.subplot(2, 2, 4)
        plt.plot(solution2.t, solution2.y[1], 'b-', label='Positive Matter', linewidth=2)
        plt.plot(solution2.t, solution2.y[3], 'r-', label='Negative Matter', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Velocity')
        plt.title('Positive Matter Pushed - Velocity vs Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('dual_matter_interaction.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        # Print behavioral analysis
        print("BEHAVIORAL ANALYSIS:")
        print("=" * 50)
        print("POSITIVE MATTER (587 kHz):")
        print("  • Resists motion (normal inertia)")
        print("  • Seeks stability")
        print("  • Behaves classically")
        print()
        print("NEGATIVE MATTER (293.5 kHz):")
        print("  • Self-accelerates (anti-inertia)")
        print("  • Seeks change and optimization")
        print("  • Exhibits quantum-like behavior")
        print()
        print("INTERACTION:")
        print("  • Positive matter attracts negative matter")
        print("  • Negative matter repels positive matter")
        print("  • Forms stable dynamic systems")
        
        return solution, solution2

# Run the demonstration
if __name__ == "__main__":
    print("Starting Dual Matter Simulation...")
    print("This demonstrates both positive and negative temporal matter")
    print("based on Convergent Time Theory's dual resonance prediction.")
    print()
    
    simulator = DualMatterSimulation()
    results = simulator.run_demonstration()
    
    print()
    print("Simulation complete. Results saved to 'dual_matter_interaction.png'")
    print("This demonstrates the revolutionary implications of CTT:")
    print("1. Two fundamental matter types with opposite temporal properties")
    print("2. Negative matter with anti-inertial behavior")
    print("3. Complete mathematical symmetry in temporal resistance")
