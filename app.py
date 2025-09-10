from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def generate_gcal_url(title, start_date, end_date):
    return (
        "https://www.google.com/calendar/render"
        "?action=TEMPLATE"
        f"&text={title}"
        f"&dates={start_date.strftime('%Y%m%d')}/{(end_date + timedelta(days=1)).strftime('%Y%m%d')}"
        "&details=Hormone or Blood Work Schedule"
        "&sf=true&output=xml"
    )


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        last_period = request.form['last_period']
        cycle_length = request.form['cycle_length']

        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')
        # Default cycle length if irregular
        if cycle_length == 'irregular':
            cycle_length = 28
        else:
            cycle_length = int(cycle_length)

        today = datetime.today()

        cycles_passed = max(0, (today - last_period_date).days // cycle_length)
        current_cycle_start = last_period_date + timedelta(days=cycles_passed * cycle_length)

        # Define 3 cycles: current, next, third
        current_estrogen_start_date = current_cycle_start
        estrogen_start_date = current_cycle_start + timedelta(days=cycle_length)
        third_estrogen_start_date = current_cycle_start + timedelta(days=2 * cycle_length)

        # Calculate hormone phases depending on cycle length
        if cycle_length == 30:
            # Current cycle
            current_prog_start_date = current_estrogen_start_date + timedelta(days=16)  # Day 17
            current_estrogen_end_date = current_estrogen_start_date + timedelta(days=24)  # Day 25
            current_prog_end_date = current_prog_start_date + timedelta(days=13)

            # Second cycle
            prog_start_date = estrogen_start_date + timedelta(days=16)
            estrogen_end_date = estrogen_start_date + timedelta(days=24)
            prog_end_date = prog_start_date + timedelta(days=13)

            # Third cycle
            third_prog_start_date = third_estrogen_start_date + timedelta(days=16)
            third_estrogen_end_date = third_estrogen_start_date + timedelta(days=24)
            third_prog_end_date = third_prog_start_date + timedelta(days=13)
        else:
            # Current cycle
            current_prog_start_date = current_estrogen_start_date + timedelta(days=14)  # Day 15
            current_estrogen_end_date = current_estrogen_start_date + timedelta(days=20)  # Day 21
            current_prog_end_date = current_prog_start_date + timedelta(days=13)

            # Second cycle
            prog_start_date = estrogen_start_date + timedelta(days=14)
            estrogen_end_date = estrogen_start_date + timedelta(days=20)
            prog_end_date = prog_start_date + timedelta(days=13)

            # Third cycle
            third_prog_start_date = third_estrogen_start_date + timedelta(days=14)
            third_estrogen_end_date = third_estrogen_start_date + timedelta(days=20)
            third_prog_end_date = third_prog_start_date + timedelta(days=13)

        # Blood work adjustment for cycle length
        day_dif = cycle_length - 28

        # Current cycle blood work
        blood_work_date = current_estrogen_start_date + timedelta(days=18 + day_dif)  # Day 19 + adjustment
        blood_work_end_date = blood_work_date + timedelta(days=2)

        # Second cycle blood work
        blood_work_date_2 = estrogen_start_date + timedelta(days=18 + day_dif)
        blood_work_end_date_2 = blood_work_date_2 + timedelta(days=2)

        # Third cycle blood work
        blood_work_date_3 = third_estrogen_start_date + timedelta(days=18 + day_dif)
        blood_work_end_date_3 = blood_work_date_3 + timedelta(days=2)

        date_format = "%B %d, %Y"

        return jsonify({
            # Current cycle
            'current_estrogen_start_date': current_estrogen_start_date.strftime(date_format),
            'current_estrogen_end_date': current_estrogen_end_date.strftime(date_format),
            'current_prog_start_date': current_prog_start_date.strftime(date_format),
            'current_prog_end_date': current_prog_end_date.strftime(date_format),

            # Second cycle
            'estrogen_start_date': estrogen_start_date.strftime(date_format),
            'estrogen_end_date': estrogen_end_date.strftime(date_format),
            'prog_start_date': prog_start_date.strftime(date_format),
            'prog_end_date': prog_end_date.strftime(date_format),

            # Third cycle
            'third_estrogen_start_date': third_estrogen_start_date.strftime(date_format),
            'third_estrogen_end_date': third_estrogen_end_date.strftime(date_format),
            'third_prog_start_date': third_prog_start_date.strftime(date_format),
            'third_prog_end_date': third_prog_end_date.strftime(date_format),

            # Blood work dates
            'blood_work_date': blood_work_date.strftime(date_format),
            'blood_work_end_date': blood_work_end_date.strftime(date_format),
            'blood_work_date_2': blood_work_date_2.strftime(date_format),
            'blood_work_end_date_2': blood_work_end_date_2.strftime(date_format),
            'blood_work_date_3': blood_work_date_3.strftime(date_format),
            'blood_work_end_date_3': blood_work_end_date_3.strftime(date_format),

            # Google Calendar links
            'gcal_blood_work_1': generate_gcal_url("First Blood Work Window", blood_work_date, blood_work_end_date),
            'gcal_blood_work_2': generate_gcal_url("Second Blood Work Window", blood_work_date_2, blood_work_end_date_2),
            'gcal_blood_work_3': generate_gcal_url("Third Blood Work Window", blood_work_date_3, blood_work_end_date_3),

            'gcal_current_estrogen': generate_gcal_url("Current Cycle - Estrogen Phase", current_estrogen_start_date, current_estrogen_end_date),
            'gcal_current_progesterone': generate_gcal_url("Current Cycle - Progesterone Phase", current_prog_start_date, current_prog_end_date),

            'gcal_next_estrogen': generate_gcal_url("Next Cycle - Estrogen Phase", estrogen_start_date, estrogen_end_date),
            'gcal_next_progesterone': generate_gcal_url("Next Cycle - Progesterone Phase", prog_start_date, prog_end_date),

            'gcal_third_estrogen': generate_gcal_url("Third Cycle - Estrogen Phase", third_estrogen_start_date, third_estrogen_end_date),
            'gcal_third_progesterone': generate_gcal_url("Third Cycle - Progesterone Phase", third_prog_start_date, third_prog_end_date),
        })
    except ValueError:
        return jsonify({'error': 'Invalid input values. Please enter valid numbers.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
