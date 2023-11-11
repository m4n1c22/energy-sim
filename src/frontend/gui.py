from flask import Flask, Response, render_template, redirect
import csv

app = Flask(__name__)


@app.route('/')
def index():
	return redirect("/plan/1")



@app.route('/plan/<schedulenum>')
def plan(schedulenum):
	schedule_num = int(schedulenum)
	ref, tv, micro, wm, dish, comp, iref, itv, imicro, iwm, idish, icomp = None, None, None, None, None, None, None, None, None, None, None, None
	with open('data/unscheduled.csv', newline='') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		linecount = 0
		for row in csv_reader:
			if linecount==schedule_num:				
				ref 	= "true" if row[2] == "1" else "false"
				tv 		= "true" if row[3] == "1" else "false"
				micro 	= "true" if row[4] == "1" else "false"
				wm 		= "true" if row[5] == "1" else "false"
				dish 	= "true" if row[6] == "1" else "false"
				comp 	= "true" if row[7] == "1" else "false"
				break
			linecount += 1

	with open('data/scheduled.csv', newline='') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		linecount = 0
		for row in csv_reader:
			if linecount==schedule_num:
				iref 	= "true" if row[2] == "1" else "false"
				itv 	= "true" if row[3] == "1" else "false"
				imicro 	= "true" if row[4] == "1" else "false"
				iwm 	= "true" if row[5] == "1" else "false"
				idish 	= "true" if row[6] == "1" else "false"
				icomp 	= "true" if row[7] == "1" else "false"
				break
			linecount += 1


	return render_template("plan.html", ref= ref, tv= tv, micro=micro, wm=wm, dish=dish, comp=comp, iref=iref, itv=itv, imicro=imicro, iwm=iwm, idish=idish, icomp=icomp, schedulenum=schedule_num+1)
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, threaded=True)