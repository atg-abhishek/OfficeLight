import os
from flask import Flask, request, send_from_directory, url_for, redirect


app = Flask(__name__, static_url_path='')

@app.route('/version')
def Welcome():
	return 'OFFICELIGHT VERSION 0'

# @app.route('/css/<path:path>')
# def send_js(path):
# 	return redirect(url_for('static/css', filename=path))


port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	# app.run(host='0.0.0.0', port=int(port))
	app.run(debug=True)