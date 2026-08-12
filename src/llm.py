import ollama


def generate_energy_report(
    persons_detected,
    classroom_capacity,
    occupancy_percentage,
    occupancy_level,
    energy_kwh,
    estimated_cost,
    estimated_co2,
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

Analyze the following classroom observation and estimated energy scenario.

CLASSROOM OBSERVATION
Detected people: {persons_detected}
Classroom capacity: {classroom_capacity}
Occupancy percentage: {occupancy_percentage:.1f}%
Occupancy level: {occupancy_level}

CONFIGURED APPLIANCE SCENARIO

Lights: {"ON" if lights_on else "OFF"}
Fans: {"ON" if fans_on else "OFF"}
Air Conditioning: {"ON" if ac_on else "OFF"}
Projector: {"ON" if projector_on else "OFF"}

These are configured prototype inputs.
They are NOT detected by YOLO.

STRICT FACTS:

- Lights are {"ON" if lights_on else "OFF"}.
- Fans are {"ON" if fans_on else "OFF"}.
- Air Conditioning is {"ON" if ac_on else "OFF"}.
- Projector is {"ON" if projector_on else "OFF"}.

Never change these states.
Never infer a different appliance state.

If an appliance is OFF, do not describe it as operating,
active, running, consuming electricity, or requiring investigation.

IMPORTANT:
The appliance states are prototype/configured inputs.
They were NOT detected from the classroom image.

ENERGY ESTIMATES

Estimated energy consumption: {energy_kwh:.2f} kWh
Estimated electricity cost: ₹{estimated_cost:.2f}
Estimated CO2 emissions: {estimated_co2:.2f} kg
Potential cost saving: ₹{potential_saving:.2f}
Potential CO2 reduction: {potential_co2_reduction:.2f} kg

Priority level: {priority}

Generate a concise professional university energy audit containing:

1. Occupancy assessment
2. Energy-waste observation
3. Estimated energy and cost impact
4. Recommended actions
5. Priority level

IMPORTANT REPORTING RULES:

- Do NOT include a date.
- Do NOT include a classroom ID.
- Do NOT use placeholders.
- Do NOT claim appliances were detected by computer vision.
- Clearly distinguish computer-vision observations from configured appliance inputs.
- Do NOT claim electricity consumption was directly measured.
- Clearly describe energy, cost and CO2 values as estimates.
- Do NOT invent smart-meter readings.
- Never change the supplied appliance states.
- Do not discuss the projector if it is OFF.
- Base recommendations only on the supplied information.
- Keep the report professional and suitable for a university facility manager.
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


if __name__ == "__main__":

    report = generate_energy_report(
        persons_detected=0,
        classroom_capacity=60,
        occupancy_percentage=0.0,
        occupancy_level="EMPTY",
        energy_kwh=3.60,
        estimated_cost=28.80,
        estimated_co2=2.52,
        potential_saving=28.80,
        potential_co2_reduction=2.52,
        priority="CRITICAL",
        lights_on=True,
        fans_on=True,
        ac_on=True,
        projector_on=False,
    )

    print("\n===== EcoCampus AI — Local Gemma Energy Report =====\n")
    print(report)

    output_file = "outputs/energy_report.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nReport saved to: {output_file}")
