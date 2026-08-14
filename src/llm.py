import ollama


def generate_energy_report(
    persons_detected,
    classroom_capacity,
    occupancy_percentage,
    occupancy_level,
    energy_kwh,
    estimated_cost,
    estimated_co2,
    recommended_power_kw,
    recommended_energy_kwh,
    potential_saving,
    potential_co2_reduction,
    priority,
    lights_on,
    fans_on,
    ac_on,
    projector_on
):
    """
    Generate a natural-language energy audit using local Gemma.
    """

    prompt = f"""
You are EcoCampus AI, a university energy management assistant.

Analyze the following classroom observation and estimated
energy scenario.

CLASSROOM OBSERVATION

Detected people: {persons_detected}
Classroom capacity: {classroom_capacity}
Occupancy percentage: {occupancy_percentage:.1f}%
Occupancy level: {occupancy_level}

IMPORTANT:
The number of people was obtained from YOLO computer vision.
Appliance states were NOT detected by YOLO.

CONFIGURED APPLIANCE SCENARIO

Lights: {"ON" if lights_on else "OFF"}
Fans: {"ON" if fans_on else "OFF"}
Air Conditioning: {"ON" if ac_on else "OFF"}
Projector: {"ON" if projector_on else "OFF"}

These appliance states are configured prototype inputs.

STRICT APPLIANCE FACTS

- Lights are {"ON" if lights_on else "OFF"}.
- Fans are {"ON" if fans_on else "OFF"}.
- Air Conditioning is {"ON" if ac_on else "OFF"}.
- Projector is {"ON" if projector_on else "OFF"}.

These are the supplied CURRENT appliance states.

Do not change or reinterpret these states when describing
the CURRENT situation.

However, recommendations MAY propose changing appliance
operation when the occupancy level and recommended energy
values indicate that a reduction is appropriate.

If the classroom is EMPTY and configured appliances are ON,
recommend switching off those unnecessary appliances.

If occupancy is LOW, recommend reducing unnecessary
appliance operation where appropriate.

If an appliance is OFF:

- Do not describe it as operating.
- Do not describe it as active or running.
- Do not say it is consuming electricity.
- Do not recommend investigating that appliance.
- Do not mention it in the report.

ENERGY ESTIMATES

Current estimated power:
{energy_kwh / 1.0:.2f} kW

Current estimated energy consumption:
{energy_kwh:.2f} kWh

Current estimated electricity cost:
₹{estimated_cost:.2f}

Current estimated CO2 emissions:
{estimated_co2:.2f} kg

Recommended operating power:
{recommended_power_kw:.2f} kW

Recommended energy consumption:
{recommended_energy_kwh:.2f} kWh

Potential electricity cost saving:
₹{potential_saving:.2f}

Potential CO2 reduction:
{potential_co2_reduction:.2f} kg

Priority level:
{priority}

ENERGY INTERPRETATION

The current energy consumption represents the configured
appliance scenario for the analysis duration.

The recommended energy consumption represents the estimated
energy use after applying the occupancy-based recommended
operating level.

Potential savings represent the difference between the current
estimated consumption and recommended estimated consumption.

DECISION RULES

Follow these rules exactly:

1. If occupancy level is EMPTY:
   - Recommended operating power should be 0 kW.
   - Recommend switching OFF the configured appliances that
     are currently ON.
   - Report the calculated potential cost saving and CO2
     reduction when they are greater than zero.
   - Do NOT say that no changes are recommended.

2. If occupancy level is LOW:
   - Do NOT recommend switching OFF all appliances if the
     recommended operating power is greater than 0 kW.
   - Recommend reducing or optimizing appliance operation
     toward the calculated recommended operating level.
   - Report the calculated potential saving values.

3. If occupancy level is MEDIUM or HIGH:
   - Do not recommend unnecessary shutdowns.
   - Base recommendations on the supplied recommended
     operating level and calculated values.

4. Never contradict the numerical energy analysis.

The numerical values supplied by the energy engine are the
authoritative values for this report.

REPORTING RULES

- Do NOT include a date.
- Do NOT include a classroom ID.
- Do NOT use placeholders.
- Do NOT claim appliances were detected by computer vision.
- Clearly distinguish YOLO occupancy detection from configured
  appliance inputs.
- Do NOT claim electricity consumption was directly measured.
- Clearly describe energy, cost, and CO2 values as estimates.
- Do NOT invent smart-meter readings.
- Do not change the supplied appliance states when describing
  the CURRENT situation.
- Recommendations may propose changing appliance operation
  according to the decision rules above.
- Do not discuss the projector if it is OFF.
- Base recommendations only on the supplied information.
- Keep the report professional and suitable for a university
  facility manager.
- Do not invent additional appliances or energy measurements.

REPORT FORMAT

Generate a concise professional university energy audit with
exactly these five sections:

1. Occupancy Assessment
2. Energy-Waste Observation
3. Estimated Energy and Cost Impact
4. Recommended Actions
5. Priority Level

SAVINGS REPORTING

If potential savings are greater than zero, clearly report:

- Current estimated energy consumption
- Recommended estimated energy consumption
- Potential electricity cost saving
- Potential CO2 reduction

If potential savings are zero, do not invent savings.

Make the report factual, concise, and consistent with the
supplied numerical values.

"""

    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# ---------------------------------------------------------
# STANDALONE TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    report = generate_energy_report(
        persons_detected=1,
        classroom_capacity=60,
        occupancy_percentage=1.7,
        occupancy_level="LOW",

        energy_kwh=3.60,
        estimated_cost=28.80,
        estimated_co2=2.52,

        recommended_power_kw=1.80,
        recommended_energy_kwh=1.80,

        potential_saving=14.40,
        potential_co2_reduction=1.26,

        priority="HIGH",

        lights_on=True,
        fans_on=True,
        ac_on=True,
        projector_on=False,
    )

    print(
        "\n===== EcoCampus AI — Local Gemma Energy Report =====\n"
    )

    print(report)