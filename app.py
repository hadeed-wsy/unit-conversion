from flask import Flask, render_template, request

app = Flask(__name__)

# conversion bases
length = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.34
}

weight = {
    "mg": 0.000001,
    "g": 0.001,
    "kg": 1,
    "oz": 0.0283495,
    "lb": 0.453592
}

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        try:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]

            # LENGTH
            if from_unit in length and to_unit in length:
                result_value = value * length[from_unit] / length[to_unit]

            # WEIGHT
            elif from_unit in weight and to_unit in weight:
                result_value = value * weight[from_unit] / weight[to_unit]

            # TEMPERATURE (special case)
            elif from_unit in ["C", "F", "K"] and to_unit in ["C", "F", "K"]:
                result_value = convert_temperature(value, from_unit, to_unit)

            else:
                return render_template("index.html", result="Conversion not supported")

            result = f"{value} {from_unit} = {round(result_value, 2)} {to_unit}"

        except:
            result = "Invalid input"

    return render_template("index.html", result=result)


# temperature conversion logic
def convert_temperature(value, from_u, to_u):
    # convert to Celsius first
    if from_u == "F":
        value = (value - 32) * 5/9
    elif from_u == "K":
        value = value - 273.15

    # convert from Celsius to target
    if to_u == "F":
        return value * 9/5 + 32
    elif to_u == "K":
        return value + 273.15

    return value  # already Celsius


if __name__ == "__main__":
    app.run(debug=True)