"""
EcoCampus AI - Energy Analysis Engine

Converts classroom occupancy and appliance operating assumptions
into estimated energy consumption, cost, and carbon emissions.

Note:
Energy values are estimates based on configurable appliance
power ratings. They are not direct smart-meter measurements.

Appliance states are prototype/configured inputs and are NOT
directly detected by YOLO.
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

    # ---------------------------------------------------------
    # Recommended energy-use factors based on occupancy
    # ---------------------------------------------------------

    # Empty classroom:
    # All configured appliances can potentially be switched off.
    empty_usage_factor: float = 0.00

    # Very low occupancy (<25%):
    # Reduced lighting/fan/AC operation is recommended.
    low_usage_factor: float = 0.50

    # Moderate occupancy (25–50%):
    # Some optimization is possible.
    moderate_usage_factor: float = 0.80

    # High occupancy (>=50%):
    # Current configured operation is treated as appropriate.
    high_usage_factor: float = 1.00


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
    Estimate classroom energy consumption and potential savings.

    Parameters
    ----------
    people_detected : int
        Number of people detected by YOLO.

    duration_hours : float
        Duration represented by the analysis.

    lights_on, fans_on, ac_on, projector_on : bool
        Configured/prototype operating states of appliances.

    config : EnergyConfig
        Classroom energy configuration.

    Returns
    -------
    dict
        Energy consumption, estimated cost, potential savings,
        CO2 reduction, occupancy and priority.
    """

    if config is None:
        config = EnergyConfig()

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    people_detected = max(0, int(people_detected))
    duration_hours = max(0.0, float(duration_hours))

    # Prevent occupancy from exceeding classroom capacity.
    people_for_calculation = min(
        people_detected,
        config.classroom_capacity
    )

    # ---------------------------------------------------------
    # OCCUPANCY
    # ---------------------------------------------------------

    occupancy_percentage = (
        people_for_calculation
        / config.classroom_capacity
    ) * 100

    # ---------------------------------------------------------
    # CURRENT APPLIANCE POWER
    # ---------------------------------------------------------

    appliance_power = {
        "Lighting": (
            config.lighting_kw
            if lights_on
            else 0.0
        ),

        "Fans": (
            config.fans_kw
            if fans_on
            else 0.0
        ),

        "Air Conditioning": (
            config.ac_kw
            if ac_on
            else 0.0
        ),

        "Projector": (
            config.projector_kw
            if projector_on
            else 0.0
        ),
    }

    total_power_kw = sum(
        appliance_power.values()
    )

    # ---------------------------------------------------------
    # CURRENT ENERGY
    # ---------------------------------------------------------

    energy_kwh = (
        total_power_kw
        * duration_hours
    )

    estimated_cost = (
        energy_kwh
        * config.electricity_rate
    )

    estimated_co2 = (
        energy_kwh
        * config.emission_factor
    )

    # ---------------------------------------------------------
    # OCCUPANCY-BASED RECOMMENDED USAGE
    # ---------------------------------------------------------

    if people_for_calculation == 0:

        occupancy_status = "EMPTY"

        recommended_usage_factor = (
            config.empty_usage_factor
        )

        priority = "CRITICAL"

    elif occupancy_percentage < 25:

        occupancy_status = "LOW"

        recommended_usage_factor = (
            config.low_usage_factor
        )

        priority = "HIGH"

    elif occupancy_percentage < 50:

        occupancy_status = "MODERATE"

        recommended_usage_factor = (
            config.moderate_usage_factor
        )

        priority = "MEDIUM"

    else:

        occupancy_status = "NORMAL"

        recommended_usage_factor = (
            config.high_usage_factor
        )

        priority = "LOW"

    # ---------------------------------------------------------
    # RECOMMENDED ENERGY
    # ---------------------------------------------------------

    recommended_power_kw = (
        total_power_kw
        * recommended_usage_factor
    )

    recommended_energy_kwh = (
        recommended_power_kw
        * duration_hours
    )

    # ---------------------------------------------------------
    # POTENTIAL WASTE / SAVING
    # ---------------------------------------------------------

    potentially_wasted_energy = max(
        0.0,
        energy_kwh - recommended_energy_kwh
    )

    potential_saving_cost = (
        potentially_wasted_energy
        * config.electricity_rate
    )

    potential_co2_reduction = (
        potentially_wasted_energy
        * config.emission_factor
    )

    # ---------------------------------------------------------
    # RECOMMENDED APPLIANCE POWER
    # ---------------------------------------------------------

    recommended_appliance_power = {
        appliance: round(
            power * recommended_usage_factor,
            2
        )
        for appliance, power
        in appliance_power.items()
    }

    # ---------------------------------------------------------
    # RETURN RESULTS
    # ---------------------------------------------------------

    return {

        # Occupancy
        "people_detected": people_detected,

        "classroom_capacity": (
            config.classroom_capacity
        ),

        "occupancy_percentage": round(
            occupancy_percentage,
            2
        ),

        "occupancy_level": occupancy_status,

        # Duration
        "duration_hours": round(
            duration_hours,
            2
        ),

        # Current appliance configuration
        "appliance_power_kw": {
            appliance: round(power, 2)
            for appliance, power
            in appliance_power.items()
        },

        # Current energy
        "total_power_kw": round(
            total_power_kw,
            2
        ),

        "energy_kwh": round(
            energy_kwh,
            2
        ),

        "estimated_cost_inr": round(
            estimated_cost,
            2
        ),

        "estimated_co2_kg": round(
            estimated_co2,
            2
        ),

        # Recommended operation
        "recommended_usage_factor": round(
            recommended_usage_factor,
            2
        ),

        "recommended_power_kw": round(
            recommended_power_kw,
            2
        ),

        "recommended_energy_kwh": round(
            recommended_energy_kwh,
            2
        ),

        "recommended_appliance_power_kw":
            recommended_appliance_power,

        # Potential savings
        "potentially_wasted_energy_kwh": round(
            potentially_wasted_energy,
            2
        ),

        "potential_saving_inr": round(
            potential_saving_cost,
            2
        ),

        "potential_co2_reduction_kg": round(
            potential_co2_reduction,
            2
        ),

        # Priority
        "priority": priority,
    }


def print_report(result):
    """Display the energy analysis in a readable format."""

    print(
        "\n===== EcoCampus AI — Energy Analysis ====="
    )

    print(
        f"People detected       : "
        f"{result['people_detected']}"
    )

    print(
        f"Classroom capacity    : "
        f"{result['classroom_capacity']}"
    )

    print(
        f"Occupancy             : "
        f"{result['occupancy_percentage']:.1f}%"
    )

    print(
        f"Occupancy level       : "
        f"{result['occupancy_level']}"
    )

    print("\nCurrent Appliance Power:")

    for appliance, power in (
        result["appliance_power_kw"].items()
    ):

        print(
            f"  {appliance:<20}: "
            f"{power:.2f} kW"
        )

    print("\nCurrent Energy Estimate:")

    print(
        f"Total power           : "
        f"{result['total_power_kw']:.2f} kW"
    )

    print(
        f"Energy consumption    : "
        f"{result['energy_kwh']:.2f} kWh"
    )

    print(
        f"Estimated cost        : "
        f"₹{result['estimated_cost_inr']:.2f}"
    )

    print(
        f"Estimated CO₂         : "
        f"{result['estimated_co2_kg']:.2f} kg"
    )

    print("\nRecommended Operation:")

    print(
        f"Usage factor          : "
        f"{result['recommended_usage_factor'] * 100:.0f}%"
    )

    print(
        f"Recommended power     : "
        f"{result['recommended_power_kw']:.2f} kW"
    )

    print(
        f"Recommended energy    : "
        f"{result['recommended_energy_kwh']:.2f} kWh"
    )

    print("\nPotential Savings:")

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

    print(
        f"\nPriority              : "
        f"{result['priority']}"
    )


# ---------------------------------------------------------
# STANDALONE TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\nTesting EMPTY classroom...")
    
    result = calculate_energy(
        people_detected=0,
        duration_hours=1,
        lights_on=True,
        fans_on=True,
        ac_on=True,
        projector_on=False,
    )

    print_report(result)

    print("\n\nTesting LOW occupancy classroom...")

    result = calculate_energy(
        people_detected=1,
        duration_hours=1,
        lights_on=True,
        fans_on=True,
        ac_on=True,
        projector_on=False,
    )

    print_report(result)