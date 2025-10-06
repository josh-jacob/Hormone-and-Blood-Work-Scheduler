from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        last_period = request.form['last_period']
        cycle_length = request.form['cycle_length']

        # Handle irregular
        if cycle_length == 'irregular':
            cycle_length = 28
        else:
            try:
                cycle_length = int(cycle_length)
            except ValueError:
                return jsonify({'error': 'Cycle length must be a number.'}), 400

            if cycle_length > 50:
                return jsonify({'error': 'Cycle length out of range.'}), 400

        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')
        today = datetime.today()

        # How many cycles have elapsed since last period
        elapsed_cycles = (today - last_period_date).days // cycle_length

        # Anchor the "current" cycle to where we are now
        current_cycle_start = last_period_date + timedelta(days=elapsed_cycles * cycle_length)
        next_cycle_start = current_cycle_start + timedelta(days=cycle_length)
        third_cycle_start = current_cycle_start + timedelta(days=2 * cycle_length)

        # === Hormone phases ===
        # Estrogen: Day 1–25
        # Progesterone: Day 15–29 (15 days total)

        # Current cycle
        current_estrogen_start = current_cycle_start
        current_estrogen_end   = current_cycle_start + timedelta(days=24)
        current_prog_start     = current_cycle_start + timedelta(days=14)
        current_prog_end       = current_cycle_start + timedelta(days=28)

        # Next cycle
        estrogen_start = next_cycle_start
        estrogen_end   = next_cycle_start + timedelta(days=24)
        prog_start     = next_cycle_start + timedelta(days=14)
        prog_end       = next_cycle_start + timedelta(days=28)

        # Third cycle
        third_estrogen_start = third_cycle_start
        third_estrogen_end   = third_cycle_start + timedelta(days=24)
        third_prog_start     = third_cycle_start + timedelta(days=14)
        third_prog_end       = third_cycle_start + timedelta(days=28)

        # === Blood work dates ===
        day_dif = cycle_length - 28

        blood_work_date    = current_cycle_start + timedelta(days=18 + day_dif)
        blood_work_end     = blood_work_date + timedelta(days=2)

        blood_work_date_2  = next_cycle_start + timedelta(days=18 + day_dif)
        blood_work_end_2   = blood_work_date_2 + timedelta(days=2)

        blood_work_date_3  = third_cycle_start + timedelta(days=18 + day_dif)
        blood_work_end_3   = blood_work_date_3 + timedelta(days=2)

        # Format output
        fmt = "%B %d, %Y"

        return jsonify({
            # Current cycle
            'current_estrogen_start_date': current_estrogen_start.strftime(fmt),
            'current_estrogen_end_date': current_estrogen_end.strftime(fmt),
            'current_prog_start_date': current_prog_start.strftime(fmt),
            'current_prog_end_date': current_prog_end.strftime(fmt),

            # Next cycle
            'estrogen_start_date': estrogen_start.strftime(fmt),
            'estrogen_end_date': estrogen_end.strftime(fmt),
            'prog_start_date': prog_start.strftime(fmt),
            'prog_end_date': prog_end.strftime(fmt),

            # Third cycle
            'third_estrogen_start_date': third_estrogen_start.strftime(fmt),
            'third_estrogen_end_date': third_estrogen_end.strftime(fmt),
            'third_prog_start_date': third_prog_start.strftime(fmt),
            'third_prog_end_date': third_prog_end.strftime(fmt),

            # Blood work
            'blood_work_date': blood_work_date.strftime(fmt),
            'blood_work_end_date': blood_work_end.strftime(fmt),
            'blood_work_date_2': blood_work_date_2.strftime(fmt),
            'blood_work_end_date_2': blood_work_end_2.strftime(fmt),
            'blood_work_date_3': blood_work_date_3.strftime(fmt),
            'blood_work_end_date_3': blood_work_end_3.strftime(fmt),

            # Extra: where are we now
            'day_in_cycle': (today - current_cycle_start).days + 1
        })

    except Exception as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400


if __name__ == '__main__':
    app.run(debug=True)
