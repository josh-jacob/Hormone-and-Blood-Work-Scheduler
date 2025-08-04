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
        # Set default cycle length for "Irregular"
        if cycle_length == 'irregular':
            cycle_length = 28  # Default cycle length if irregular
        else:
            cycle_length = int(cycle_length)
        
        today = datetime.today()
        
        # Calculate hormone phases for 3 cycles
        # Current cycle (cycle 1)
        current_estrogen_start_date = last_period_date
        
        # Next cycle (cycle 2)
        estrogen_start_date = last_period_date + timedelta(days=cycle_length)
        
        # Third cycle (cycle 3)
        third_estrogen_start_date = last_period_date + timedelta(days=cycle_length + cycle_length)
        
        # Calculate hormone end dates and progesterone dates for each cycle
        if cycle_length == 30:
            # Current cycle - corrected timing
            current_prog_start_date = current_estrogen_start_date + timedelta(days=17-1)  # Day 17
            current_estrogen_end_date = current_estrogen_start_date + timedelta(days=25-1)  # Day 25
            current_prog_end_date = current_prog_start_date + timedelta(days=13)
            
            # Second cycle
            prog_start_date = estrogen_start_date + timedelta(days=17-1)  # Day 17
            estrogen_end_date = estrogen_start_date + timedelta(days=25-1)  # Day 25
            prog_end_date = prog_start_date + timedelta(days=13)
            
            # Third cycle
            third_prog_start_date = third_estrogen_start_date + timedelta(days=17-1)  # Day 17
            third_estrogen_end_date = third_estrogen_start_date + timedelta(days=25-1)  # Day 25
            third_prog_end_date = third_prog_start_date + timedelta(days=13)
        else:
            # Current cycle - corrected timing
            current_prog_start_date = current_estrogen_start_date + timedelta(days=15-1)  # Day 15
            current_estrogen_end_date = current_estrogen_start_date + timedelta(days=21-1)  # Day 21
            current_prog_end_date = current_prog_start_date + timedelta(days=13)
            
            # Second cycle
            prog_start_date = estrogen_start_date + timedelta(days=15-1)  # Day 15
            estrogen_end_date = estrogen_start_date + timedelta(days=21-1)  # Day 21
            prog_end_date = prog_start_date + timedelta(days=13)
            
            # Third cycle
            third_prog_start_date = third_estrogen_start_date + timedelta(days=15-1)  # Day 15
            third_estrogen_end_date = third_estrogen_start_date + timedelta(days=21-1)  # Day 21
            third_prog_end_date = third_prog_start_date + timedelta(days=13)
        
        # Blood work dates for 3 cycles - corrected calculation
        day_dif = cycle_length - 28
        
        # First cycle blood work
        blood_work_date = last_period_date + timedelta(days=19-1 + day_dif)  # Day 19 + adjustment
        blood_work_end_date = blood_work_date + timedelta(days=3-1)  # 3-day window
        
        # Second cycle blood work
        blood_work_date_2 = estrogen_start_date + timedelta(days=19-1 + day_dif)
        blood_work_end_date_2 = blood_work_date_2 + timedelta(days=3-1)
        
        # Third cycle blood work
        blood_work_date_3 = third_estrogen_start_date + timedelta(days=19-1 + day_dif)
        blood_work_end_date_3 = blood_work_date_3 + timedelta(days=3-1)
        
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
            # Example: First blood work window
            'gcal_blood_work_1': generate_gcal_url(
                "First Blood Work Window",
                blood_work_date,
                blood_work_end_date
            ),
            
            'gcal_blood_work_2': generate_gcal_url(
                "Second Blood Work Window",
                blood_work_date_2,
                blood_work_end_date_2
            ),
            
            'gcal_blood_work_3': generate_gcal_url(
                "Third Blood Work Window",
                blood_work_date_3,
                blood_work_end_date_3
            ),

        })
    except ValueError:
        return jsonify({'error': 'Invalid input values. Please enter valid numbers.'}), 400



if __name__ == '__main__':
    app.run(debug=True)
