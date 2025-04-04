import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chlorine_calculator():
    if request.method == "POST":
        solution_tank_volume = float(request.form["solution_tank_volume"])
        water_flow_rate = float(request.form["water_flow_rate"])
        required_chlorine_demand = float(request.form["required_chlorine_demand"])
        chlorine_concentration = float(request.form["chlorine_concentration"]) / 100  # Convert % to decimal
        doser_pump_flow_rate_100 = float(request.form["doser_pump_flow_rate_100"])
        set_point = float(request.form["set_point"])
        chlorine_last_duration = float(request.form["chlorine_last_duration"])

        # Step 1: Calculate chlorine required per hour (g/hr)
        mass_chlorine_per_hour = (required_chlorine_demand * water_flow_rate) / 1000  # Convert mg to g

        # Step 2: Calculate total chlorine needed
        total_chlorine_needed = mass_chlorine_per_hour * chlorine_last_duration  # g

        # Step 3: Adjust for chlorine concentration
        chlorine_required = total_chlorine_needed / chlorine_concentration  

        # Step 4: Round to 2 decimal places
        chlorine_required = round(chlorine_required, 2)

        # Pass the result to the template
        return render_template("index.html", result=chlorine_required)

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

