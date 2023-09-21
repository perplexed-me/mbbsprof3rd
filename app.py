from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('record_search_updated.html')

@app.route('/search', methods=['GET'])
def search_record():
    criteria = request.args.get('criteria')
    value = request.args.get('value')
    
    conn = sqlite3.connect('prof3data.db')
    cursor = conn.cursor()

    # Using string formatting for the column name, but parameterized query for the value to avoid SQL injection
    cursor.execute(f"SELECT * FROM records WHERE {criteria} LIKE ?", ('%' + value + '%',))
    
    records = cursor.fetchall()
    conn.close()
   
    if records:
        # College Name,Student's Name,Registration,Session,Program,Exam Roll,Class Roll,Exam Year,Status

        keys = ['College','Name','Registration','Session','Program','Roll', 'ClassRoll','ExamYear','Status']
        records_list = [dict(zip(keys, record)) for record in records]
        return jsonify(records_list)
    else:
        return jsonify({"message": "No records found"}), 404

if __name__ == '__main__':
    app.run(debug=False, port=3000)
