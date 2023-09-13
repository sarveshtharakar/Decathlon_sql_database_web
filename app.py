from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

#for connecting data base 
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sarvesh98#',
    'database': 'decathlon'
}   

#this def function is use give the column name for the table which we are gong to retrivr from the database 
def fetch_column_names(cursor):
    """Fetch and return column names from the cursor."""
    column_names = [column[0] for column in cursor.description]
    return column_names

#this @app route is used to open the html file which we want to open here we have opened an index page which consisting
#of and text area where we enter our sql queries 
@app.route('/')
def index():
    return render_template('index.html')

#this @app.route is used execute the query which we have entered in html it will take that query to the sql and execute 
@app.route('/execute_query', methods=['POST'])
def execute_query():
    try:
        query = request.form['query']

        conn = mysql.connector.connect(**db_config)#we have built the connection and login to sql server from here
        cursor = conn.cursor()

        cursor.execute(query)

 
        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):#this if statement is used to inserting the values in table 
            conn.commit()  
            return "Query executed successfully!"  
        else: #this else statement is used to retrive the data from the table 
            result = cursor.fetchall()
            column_names = fetch_column_names(cursor) 

            cursor.close()
            conn.close()

            return render_template('result.html', result=result, column_names=column_names)#that retrived data will show in the next html page called result 

    except Exception as e:
        return render_template('index.html', error=str(e))#if any error occurs it will take that error and present it in index page only 

if __name__ == '__main__':
    app.run(debug=True)
