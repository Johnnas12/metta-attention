from hyperon import MeTTa
import matplotlib.pyplot as plt
import numpy as np

# Initialize MeTTa instance
metta = MeTTa()

# Define the base code for concepts and initial attention levels
metta.run('''
    (Concept "Dog")
    (Concept "Cat")
    (Concept "Fish")
    (Attention (Concept "Dog") 0.7)
    (Attention (Concept "Cat") 0.5)
    (Attention (Concept "Fish") 0.2)
''')

# Function to get attention value for a concept
def get_attention(concept_name):
    result = metta.run(f'!(match &self (Attention (Concept "{concept_name}") $x) $x)')
    return result[0] if result else None

# Function to shift attention (set a new value)
def shift_attention(concept_name, new_value):
    # First, remove the existing attention value for the concept by clearing the old attention atom
    metta.run(f'!(remove-atom &self (Attention (Concept "{concept_name}") $x))')
    # Then, add the new attention value
    metta.run(f'(Attention (Concept "{concept_name}") {new_value})')

# Function to drift attention (increment or decrement by a certain amount)
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

# Lists to store attention values over time
time_steps = []
dog_values = []
cat_values = []
fish_values = []

# Function to record values
def record_values(t):
    time_steps.append(t)
    dog_values.append(float(str(get_attention('Dog')[0])) if get_attention('Dog') else 0.0)
    cat_values.append(float(str(get_attention('Cat')[0])) if get_attention('Cat') else 0.0)
    fish_values.append(float(str(get_attention('Fish')[0])) if get_attention('Fish') else 0.0)

# Continuous drifting simulation
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

# Example: Test shifting and drifting
print("Initial Attention Values:")
print(f"Dog: {get_attention('Dog')}")
print(f"Cat: {get_attention('Cat')}")
print(f"Fish: {get_attention('Fish')}")
record_values(0)

# Shifting the attention of "Dog" to 1.0
shift_attention("Dog", 1.0)
print("\nAfter Shifting 'Dog' Attention to 1.0:")
print(f"Dog: {get_attention('Dog')}")
record_values(1)

# Drifting the attention of "Cat" by -0.1
shift_attention("Cat", 0.4)
print("\nAfter Drifting 'Cat' Attention by 0.4:")
print(f"Cat: {get_attention('Cat')}")
record_values(2)

#######################################
shift_attention("Fish", 0.6)
print("\nAfter Shifting 'Dog' Attention to 0.6:")
print(f"Dog: {get_attention('Dog')}")
record_values(3)

# Start continuous drifting simulation
print("\nStarting Continuous Drifting Simulation (0 to 45 seconds)...")
shift_attention("Dog", 0.85)
record_values(0)
continuous_drift(0, 15, 0.1)
shift_attention("Cat", 0.85)



print("\nFinal Attention Values:")
print(f"Dog: {get_attention('Dog')}")
print(f"Cat: {get_attention('Cat')}")
print(f"Fish: {get_attention('Fish')}")

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(time_steps, dog_values, label="Dog", color="blue", linewidth=2)
plt.plot(time_steps, cat_values, label="Cat", color="green", linewidth=2)
plt.plot(time_steps, fish_values, label="Fish", color="red", linewidth=2)
plt.xlabel("Time (seconds)")
plt.ylabel("Attention Level")
plt.title("Shifting and Drifting Attention Dynamics")
plt.legend(loc="upper right")
plt.grid(True)
plt.ylim(0, 1)  # Set y-axis limit to 0-1 for attention levels

# Display the plot in a closable window
plt.show(block=True)

# Fallback: Save plot if interactive display fails
try:
    plt.savefig("attention_plot.png")
    print("Plot saved as 'attention_plot.png' if window display failed.")
except Exception as e:
    print(f"Could not save plot: {e}")

print("Plot window closed. Script completed.")