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

        if cycle_length == 'irregular': # cycle length is irregular
            today = datetime.today()
            estrogen_start_date = last_period_date
            current_estrogen_start_date = last_period_date
            
            
            while estrogen_start_date <= today: # default to 28 days and calculate about when cycle should start
                estrogen_start_date += timedelta(days=28)

            date_format = "%B %d, %Y"
        
        else:
            cycle_length = int(cycle_length)
            estrogen_start_date = last_period_date + timedelta(days=cycle_length)
        
        current_estrogen_start_date = last_period_date
        if cycle_length == 30:
            prog_start_date = estrogen_start_date + timedelta(days=17-1) # progesterone start on day 17
            estrogen_end_date = estrogen_start_date + timedelta(days=25-1) # estrogen end on day 25
            current_prog_start_date = current_estrogen_start_date+timedelta(days=16)
            current_estrogen_end_date = current_estrogen_start_date+timedelta(days=24)
         
        else:
            prog_start_date = estrogen_start_date + timedelta(days=15-1) # progestrone start on day 15
            estrogen_end_date = estrogen_start_date + timedelta(days=21-1) # estrogen end on day 21
            current_prog_start_date = current_estrogen_start_date+timedelta(days=14)
            current_estrogen_end_date = current_estrogen_start_date+timedelta(days=20)
        
 

        prog_end_date = prog_start_date + timedelta(days=13) # progesterone end 13 days after start
        current_prog_end_date = current_prog_start_date+timedelta(days=13)
        
        blood_work_date = last_period_date + timedelta(days=19-1)
        blood_work_end_date = blood_work_date + timedelta(days=3-1)
        
        blood_work_date_2 = estrogen_start_date + timedelta(days=19-1)
        blood_work_end_date_2 = blood_work_date_2 + timedelta(days=2)
            
        date_format = "%B %d, %Y"
        
        print(current_estrogen_start_date)
        print(current_estrogen_end_date)
        
        print(current_prog_start_date)
        return jsonify({
            'estrogen_start_date': estrogen_start_date.strftime(date_format),
            'estrogen_end_date': estrogen_end_date.strftime(date_format),
            'current_estrogen_start_date': current_estrogen_start_date.strftime(date_format),
            'current_estrogen_end_date': current_estrogen_end_date.strftime(date_format),
            'prog_start_date': prog_start_date.strftime(date_format),
            'prog_end_date': prog_end_date.strftime(date_format),
            'current_prog_start_date': current_prog_start_date.strftime(date_format),
            'current_prog_end_date': current_prog_end_date.strftime(date_format),
            'blood_work_date': blood_work_date.strftime(date_format),
            'blood_work_end_date': blood_work_end_date.strftime(date_format),
            'blood_work_date_2': blood_work_date_2.strftime(date_format),
            'blood_work_end_date_2': blood_work_end_date_2.strftime(date_format)
        })
    except ValueError:
        return jsonify({'error': 'Invalid input values. Please enter valid numbers.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
