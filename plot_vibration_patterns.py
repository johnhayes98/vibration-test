import matplotlib.pyplot as plt
import vibration_patterns
import inspect

# Function to generate time series data
def generate_time_series(data: dict):
    time_series_dict = {}
    for key, values in data.items():
        time_series = []
        for duration, value in values:
            if duration > 0:  # Skip if duration is 0
                time_series.extend([value] * duration)
        time_series_dict[key] = time_series
    return time_series_dict


def plot_vibration_pattern(vibration_dict_name):
    # Generate time series data for each entry
    time_series_data = generate_time_series(getattr(vibration_patterns, vibration_dict_name, None))

    # Create a vertical plot with subplots
    fig, axes = plt.subplots(len(time_series_data), 1, figsize=(4, 4), sharex=True)

    # Plot each time series in its own subplot
    for i, (key, series) in enumerate(time_series_data.items()):
        axes[i].plot(series, color="black", linewidth=1)
        # axes[i].set_title(key)
        axes[i].set_ylabel(key)
        # axes[i].grid(True, linestyle="--", alpha=0.5)
        # axes[i].legend(loc="upper right")
        axes[i].set_ylim(0, 300)  # Set y-axis limit for all subplots

    # Add a global figure title
    fig.suptitle(vibration_dict_name + " Vibration Patterns", fontsize=12)

    # Add shared x-axis label
    plt.xlabel("Time (ms)")
    plt.tight_layout()  # Adjust layout to avoid overlap



if __name__ == "__main__":
    for vibration_group in [name for name, obj in inspect.getmembers(vibration_patterns) if isinstance(obj, dict) and not name.startswith('__')]:
        plot_vibration_pattern(vibration_group)
    plt.show()