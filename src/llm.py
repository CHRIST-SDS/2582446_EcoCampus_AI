import ollama


def generate_energy_report(
    persons_detected,
    classroom_capacity,
    lights_on,
    fans_on,
    ac_on,
    projector_on
):
    occupancy_percentage = (
        persons_detected / classroom_capacity
    ) * 100

    prompt = f"""
You are EcoCampus AI, a university energy management assistant.

Analyze the following classroom information:

Detected people: {persons_detected}
Classroom capacity: {classroom_capacity}
Occupancy percentage: {occupancy_percentage:.1f}%

Lights ON: {lights_on}
Fans ON: {fans_on}
AC ON: {ac_on}
Projector ON: {projector_on}

Generate a concise energy audit containing:
1. Occupancy assessment
2. Potential energy-waste condition
3. Recommended actions
4. Priority level

Do not claim that actual electricity consumption was measured.
Clearly describe values as estimates or observations.
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
        persons_detected=7,
        classroom_capacity=60,
        lights_on=True,
        fans_on=True,
        ac_on=True,
        projector_on=True
    )

    print("\n===== EcoCampus AI — Local LLM Energy Report =====\n")
    print(report)