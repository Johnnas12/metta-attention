# MeTTa Attention Shifting and Drifting Simulation

This repository contains a Python-based simulation that integrates MeTTa (a logic-based language) with Matplotlib to model and visualize the dynamics of attention shifting and drifting, inspired by the paper *"Shifting and Drifting Attention While Reading"* by Goertzel et al. (2018). The project tracks the attention levels of three concepts ("Dog," "Cat," "Fish") through discrete shifts and continuous drifting over time, plotting the results in an interactive graph.

## Overview

The simulation initializes attention levels for "Dog," "Cat," and "Fish" in a MeTTa atomspace, allows for manual shifts (e.g., setting a new attention value) and drifts (incremental changes), and includes a continuous time-based drifting simulation. The attention dynamics are visualized using Matplotlib, showing both discrete jumps (shifts) and smooth transitions (drifting) over a 45-second period.

## Features

- **MeTTa Integration**: Uses the `hyperon` library to manage concepts and attention levels in a logic-based atomspace.
- **Discrete Shifts**: Allows setting specific attention values (e.g., "Dog" to 1.0, "Cat" to 0.85) at defined time steps.
- **Discrete Drifts**: Implements incremental changes to attention levels (e.g., "Cat" by -0.1).
- **Continuous Drifting Simulation**: Models attention drifting over time using a differential equation (\( \frac{dA}{dt} = S - D \cdot A \)) with configurable stimulus (\( S \)) and decay (\( D \)) rates, converging to steady states (e.g., 0.5 for "Dog," 0.15 for "Cat," 0.3 for "Fish").
- **Visualization**: Plots attention levels over time using Matplotlib, with discrete shifts as jumps and continuous drifts as smooth curves, displayed in a closable interactive window.
- **Debugging**: Includes print statements to monitor MeTTa atomspace states and verify operations.

### Impelementation Details
- **Shifting**: The process of instantly changing an attention level to a specific value (e.g., setting "Dog" to 0.85), represented as discrete jumps in the graph. consider it as sudden jump from one attention Level to another
- **Drifting**: The gradual adjustment of attention levels over time based on stimulus and decay dynamics (e.g., converging to 0.5 for "Dog"), shown as smooth curves.

1. shifting Implementation                                                                                                           
  ```
  def shift_attention(concept_name, new_value):
    # First, remove the existing attention value for the concept by clearing the old attention atom
    metta.run(f'!(remove-atom &self (Attention (Concept "{concept_name}") $x))')
    # Then, add the new attention value
    metta.run(f'(Attention (Concept "{concept_name}") {new_value})')
  ```
2. Discerete Drifts
    ```
      def drift_attention(concept_name, drift_amount):
          current_value = get_attention(concept_name)
          if current_value is not None and len(current_value) > 0:
              # Extract and convert the value to float
              try:
                  current_numeric = float(str(current_value[0]))  # Convert list item to float
                  new_value = max(0.0, min(1.0, current_numeric + drift_amount))  # Constrain to [0, 1]
                  shift_attention(concept_name, new_value)
                  print(f"Drifted {concept_name} from {current_numeric} to {new_value}")
              except (ValueError, TypeError) as e:
                  print(f"Error converting value for {concept_name}: {e}, using fallback")
                  return
          else:
              print(f"Invalid attention value for {concept_name}, skipping drift")
    ```  
3. continious Drifting
       ```
        def continuous_drift(t_start, t_end, dt):
            t = t_start
            while t <= t_end:
                for concept in ["Dog", "Cat", "Fish"]:
                    current_value = float(str(get_attention(concept)[0])) if get_attention(concept) else 0.0
                    if t > 5:  # Start drifting after 5 seconds
                        if concept == "Dog":
                            stimulus = 0.07  # Steady state = 0.5 (0.1 / 0.2)
                            decay = 0.2
                            new_value = current_value + dt * (stimulus - decay * current_value)
                        elif concept == "Cat":
                            stimulus = 0.03  # Steady state = 0.15 (0.03 / 0.2)
                            decay = 0.2
                            new_value = current_value + dt * (stimulus - decay * current_value)
                        elif concept == "Fish":
                            if 5 < t <= 25:
                                stimulus = 0.06  # Steady state = 0.3 (0.06 / 0.2)
                                decay = 0.2
                                new_value = current_value + dt * (stimulus - decay * current_value)
                            elif 25 < t <= 30:
                                stimulus = 0.08  # Temporary spike
                                decay = 0.2
                                new_value = current_value + dt * (stimulus - decay * current_value)
                            else:
                                stimulus = 0.06  # Back to 0.3
                                decay = 0.2
                                new_value = current_value + dt * (stimulus - decay * current_value)
                        new_value = max(0.0, min(1.0, new_value))  # Constrain to [0, 1]
                        shift_attention(concept, new_value)
                record_values(t)
                t += dt                                                                                                   
       ```                                                                                                    
                                                                                                                                                                                                                                           

## Setup

### Prerequisites
- Python 3.7 or higher
- Required libraries:
  - `hyperon` (for MeTTa integration)
  - `matplotlib` (for plotting)
  - `numpy` (for numerical operations)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/iCog-Labs-Dev/metta-attention.git
   cd metta-attention
  ```
### Install Dependencies 
  ```
    pip install hyperon matplotlib numpy
  ```
  2. Running the code
    ```
      python attention-bank/shifting-and-drifting/shifting-drifting.py
    ```
