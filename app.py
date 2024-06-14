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
    
        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')

        if cycle_length == 'irregular':
            today = datetime.today()
            next_period_date = last_period_date

            while next_period_date <= today:
                next_period_date += timedelta(days=28)
            
                
            estrogen_end_date = next_period_date + timedelta(days=21)
            prog_start_date = next_period_date + timedelta(days=15)
            prog_end_date = prog_start_date + timedelta(days=13)
            blood_work_date = next_period_date + timedelta(days=19)
            blood_work_end_date = blood_work_date + timedelta(days=3)

            date_format = "%B %d, %Y"
        
        else:
            cycle_length = int(cycle_length)
            next_period_date = last_period_date + timedelta(days=cycle_length)

       
            if cycle_length == 28:
                prog_start_date = next_period_date + timedelta(days=15)
                estrogen_end_date = next_period_date + timedelta(days=21)
                
            else:
                prog_start_date = next_period_date + timedelta(days=17)
                estrogen_end_date = next_period_date + timedelta(days=21)
            
            prog_end_date = prog_start_date + timedelta(days=13)
            blood_work_date = next_period_date + timedelta(days=19)
            blood_work_end_date = blood_work_date + timedelta(days=3)
            
            date_format = "%B %d, %Y"
            
        return jsonify({
            'next_period': next_period_date.strftime(date_format),
            'estrogen_end_date': estrogen_end_date.strftime(date_format),
            'prog_start_date': prog_start_date.strftime(date_format),
            'prog_end_date': prog_end_date.strftime(date_format),
            'blood_work_date': blood_work_date.strftime(date_format),
            'blood_work_end_date': blood_work_end_date.strftime(date_format),
        })
    except ValueError:
        return jsonify({'error': 'Invalid input values. Please enter valid numbers.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
