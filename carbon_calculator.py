# backend/carbon_calculator.py

def calculate_co2(cpu_usage, ram_usage, network_sent, network_recv, session_duration_min):
    """
    Calculate CO2 emission in grams based on device usage
    
    Formula:
    - CPU Energy = (CPU_Watts × Time) / 1000
    - RAM Energy = (RAM_Watts × Time) / 1000  
    - Network Energy = Data_MB × 0.0001 kWh
    - CO2 = Total_Energy × 450 gCO2/kWh (carbon intensity)
    """
    
    # Convert bytes to MB
    total_data_mb = (network_sent + network_recv) / (1024 * 1024)
    
    # CPU Energy Calculation (kWh)
    # Average laptop CPU uses 5-40W depending on load
    cpu_power_watts = (cpu_usage / 100) * 30 + 5  # Base 5W + CPU load
    cpu_energy_kwh = (cpu_power_watts * session_duration_min) / 60 / 1000
    
    # RAM Energy Calculation (kWh)
    # RAM uses about 2W for 8GB
    ram_power_watts = (ram_usage / 100) * 2
    ram_energy_kwh = (ram_power_watts * session_duration_min) / 60 / 1000
    
    # Network Energy Calculation (kWh)
    # Approx 0.0001 kWh per MB of data transfer
    network_energy_kwh = total_data_mb * 0.0001
    
    # Total Energy (kWh)
    total_energy_kwh = cpu_energy_kwh + ram_energy_kwh + network_energy_kwh
    
    # CO2 Emission (grams)
    # Average carbon intensity: 450 gCO2/kWh (global average)
    carbon_intensity = 450
    co2_grams = total_energy_kwh * carbon_intensity
    
    return round(co2_grams, 2)


def calculate_hourly_emission(cpu_usage, ram_usage, network_sent, network_recv):
    """
    Calculate emission for exactly 1 hour (used for prediction)
    """
    return calculate_co2(cpu_usage, ram_usage, network_sent, network_recv, 60)


def get_network_intensity(network_type):
    """
    Get carbon intensity based on network type
    Different networks have different energy efficiencies
    """
    intensity_map = {
        'WiFi': 250,      # Cleaner - usually on固定 power
        'Ethernet': 200,  # Most efficient
        '4G': 450,        # Average mobile network
        '5G': 400,        # Better than 4G
        '3G': 500,        # Less efficient
        'Mobile Data': 450
    }
    return intensity_map.get(network_type, 350)