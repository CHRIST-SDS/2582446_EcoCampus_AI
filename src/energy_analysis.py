"""
EcoCampus AI - Energy Analysis Engine

Converts classroom occupancy and appliance operating assumptions
into estimated energy consumption, cost, and carbon emissions.

Note:
Energy values are estimates based on configurable appliance
power ratings. They are not direct smart-meter measurements.
"""

from dataclasses import dataclass


@dataclass
class EnergyConfig:
    """Configuration for classroom energy estimation."""

    classroom_capacity: int = 60

    # Estimated appliance power ratings in kW
    lighting_kw: float = 0.80
    fans_kw: float = 0.30
    ac_kw: float = 2.50
    projector_kw: float = 0.30

    # Electricity tariff (₹/kWh)
    electricity_rate: float = 8.0

    # Estimated grid emission factor (kg CO2/kWh)
    emission_factor: float = 0.70


def calculate_energy(
    people_detected: int,
    duration_hours: float = 1.0,
    lights_on: bool = True,
    fans_on: bool = True,
    ac_on: bool = True,
    projector_on: bool = False,
    config: EnergyConfig | None = None,
):
    """
    Estimate classroom energy consumption.

    Parameters
    ----------
    people_detected : int
        Number of people detected by the computer-vision model.

    duration_hours : float
        Duration represented by the analysis.

    lights_on, fans_on, ac_on, projector_on : bool
        Assumed/configured operating states of classroom appliances.

    config : EnergyConfig
        Classroom energy configuration.
    """

    if config is None:
        config = EnergyConfig()

    occupancy_percentage = (
        people_detected / config.classroom_capacity
    ) * 100

    appliance_power = {
        "Lighting": config.lighting_kw if lights_on else 0,
        "Fans": config.fans_kw if fans_on else 0,
        "Air Conditioning": config.ac_kw if ac_on else 0,
        "Projector": config.projector_kw if projector_on else 0,
    }

    total_power_kw = sum(appliance_power.values())

    energy_kwh = total_power_kw * duration_hours

    estimated_cost = energy_kwh * config.electricity_rate

    estimated_co2 = energy_kwh * config.emission_factor

    # Prototype assumption:
    # when the room is empty, active appliances represent
    # potentially unnecessary energy use.
    if people_detected == 0:
        potentially_wasted_energy = energy_kwh
    else:
        potentially_wasted_energy = 0

    potential_saving_cost = (
        potentially_wasted_energy * config.electricity_rate
    )

    potential_co2_reduction = (
        potentially_wasted_energy * config.emission_factor
    )

    # Priority based on occupancy.
    if people_detected == 0:
        priority = "CRITICAL"
    elif occupancy_percentage < 25:
        priority = "HIGH"
    elif occupancy_percentage < 50:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "people_detected": people_detected,
        "classroom_capacity": config.classroom_capacity,
        "occupancy_percentage": round(occupancy_percentage, 2),
        "duration_hours": duration_hours,
        "appliance_power_kw": appliance_power,
        "total_power_kw": round(total_power_kw, 2),
        "energy_kwh": round(energy_kwh, 2),
        "estimated_cost_inr": round(estimated_cost, 2),
        "estimated_co2_kg": round(estimated_co2, 2),
        "potentially_wasted_energy_kwh": round(
            potentially_wasted_energy, 2
        ),
        "potential_saving_inr": round(
            potential_saving_cost, 2
        ),
        "potential_co2_reduction_kg": round(
            potential_co2_reduction, 2
        ),
        "priority": priority,
    }


def print_report(result):
    """Display the energy analysis in a readable format."""

    print("\n===== EcoCampus AI — Energy Analysis =====")

    print(f"People detected       : {result['people_detected']}")
    print(f"Classroom capacity    : {result['classroom_capacity']}")
    print(f"Occupancy             : {result['occupancy_percentage']}%")

    print("\nAppliance Power:")

    for appliance, power in result["appliance_power_kw"].items():
        print(f"  {appliance:<20}: {power:.2f} kW")

    print("\nEnergy Estimate:")

    print(f"Total power           : {result['total_power_kw']:.2f} kW")
    print(f"Energy consumption    : {result['energy_kwh']:.2f} kWh")
    print(f"Estimated cost        : ₹{result['estimated_cost_inr']:.2f}")
    print(f"Estimated CO₂         : {result['estimated_co2_kg']:.2f} kg")

    print("\nPotential Waste:")

    print(
        f"Potential wasted energy : "
        f"{result['potentially_wasted_energy_kwh']:.2f} kWh"
    )

    print(
        f"Potential cost saving   : "
        f"₹{result['potential_saving_inr']:.2f}"
    )

    print(
        f"Potential CO₂ reduction : "
        f"{result['potential_co2_reduction_kg']:.2f} kg"
    )

    print(f"\nPriority              : {result['priority']}")


if __name__ == "__main__":

    # Standalone test scenario.
    # In the final integrated pipeline, this value
    # will come directly from YOLO detection.
    result = calculate_energy(
        people_detected=0,
        duration_hours=1,
        lights_on=True,
        fans_on=True,
        ac_on=True,
        projector_on=False,
    )

    print_report(result)
