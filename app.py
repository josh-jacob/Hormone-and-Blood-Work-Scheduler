from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/calculate_hormones', methods=['POST'])
def calculate_hormones():
    try:
        last_period = request.form['last_period']
        cycle_length = request.form['cycle_length']
    
        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')

        # Set default cycle length for "Irregular"
        if cycle_length == 'irregular':
            cycle_length = 28  # Default cycle length if irregular
        else:
            cycle_length = int(cycle_length)
        
        today = datetime.today()

        # Calculate hormone phases
        estrogen_start_date = last_period_date + timedelta(days=cycle_length)
        current_estrogen_start_date = last_period_date
        
        if cycle_length == 30:
            prog_start_date = estrogen_start_date + timedelta(days=17-1)  # Progesterone start on day 17
            estrogen_end_date = estrogen_start_date + timedelta(days=25-1)  # Estrogen end on day 25
            current_prog_start_date = current_estrogen_start_date + timedelta(days=16)
            current_estrogen_end_date = current_estrogen_start_date + timedelta(days=24)
        else:
            prog_start_date = estrogen_start_date + timedelta(days=15-1)  # Progesterone start on day 15
            estrogen_end_date = estrogen_start_date + timedelta(days=21-1)  # Estrogen end on day 21
            current_prog_start_date = current_estrogen_start_date + timedelta(days=14)
            current_estrogen_end_date = current_estrogen_start_date + timedelta(days=20)
        
        prog_end_date = prog_start_date + timedelta(days=13)  # Progesterone end 13 days after start
        current_prog_end_date = current_prog_start_date + timedelta(days=13)


        return jsonify({
            'current_estrogen_start_date': last_period_date.strftime('%B %d, %Y'),
            'current_estrogen_end_date': (last_period_date + timedelta(days=20)).strftime('%B %d, %Y'),
            'estrogen_start_date': estrogen_start_date.strftime('%B %d, %Y'),
            'estrogen_end_date': estrogen_end_date.strftime('%B %d, %Y'),
            'current_prog_start_date': last_period_date.strftime('%B %d, %Y'),
            'current_prog_end_date': (last_period_date + timedelta(days=27)).strftime('%B %d, %Y'),
            'prog_start_date': prog_start_date.strftime('%B %d, %Y'),
            'prog_end_date': prog_end_date.strftime('%B %d, %Y')
        })
    except ValueError:
        return jsonify({'error': 'Invalid input values. Please enter valid numbers.'}), 400

@app.route('/calculate_blood_work', methods=['POST'])
def calculate_blood_work():
    try:
        last_period = request.form['last_period']
        cycle_length = request.form['cycle_length']

        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')
        if cycle_length == 'irregular':
            cycle_length = 28
        else:
            cycle_length = int(cycle_length)

        # Blood work dates
        day_dif = cycle_length - 28
        blood_work_date = last_period_date + timedelta(days=19-1 + day_dif)
        blood_work_end_date = blood_work_date + timedelta(days=3-1)
        
        blood_work_date_2 = estrogen_start_date + timedelta(days=19-1 + day_dif)
        blood_work_end_date_2 = blood_work_date_2 + timedelta(days=2)
        third_estrogen_start_date = current_estrogen_start_date + timedelta(days=20)
        date_format = "%B %d, %Y"

        return jsonify({
            'blood_work_date': blood_work_date.strftime('%B %d, %Y'),
            'blood_work_end_date': blood_work_end_date.strftime('%B %d, %Y'),
            'blood_work_date_2': blood_work_date_2.strftime('%B %d, %Y'),
            'blood_work_end_date_2': blood_work_end_date_2.strftime('%B %d, %Y')
        })
    except ValueError:
        return jsonify({'error': 'Invalid input values. Please enter valid numbers.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
