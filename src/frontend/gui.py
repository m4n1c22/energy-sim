from flask import Flask, Response, render_template, redirect
import csv

app = Flask(__name__)

energy_usage_per_hr = {
	"ref": 167,
	"tv": 50,
	"micro":1000,
	"wm":850,
	"dish":1800,
	"comp": 200
}

savings = 0.0

def calculate_energy_usage(ref, tv, micro, wm, dish, comp):
	usage = 0
	if ref=="true":
		usage += energy_usage_per_hr["ref"]
	if tv=="true":
		usage += energy_usage_per_hr["tv"]
	if micro=="true":
		usage += energy_usage_per_hr["micro"]
	if wm=="true":
		usage += energy_usage_per_hr["wm"]
	if dish=="true":
		usage += energy_usage_per_hr["dish"]
	if comp=="true":
		usage += energy_usage_per_hr["comp"]
	if usage == 0:
		usage = 8
	return usage


@app.route('/')
def index():
	return redirect("/plan/1")



@app.route('/plan/<schedulenum>')
def plan(schedulenum):
	schedule_num = int(schedulenum)
	global savings
	scheduled_usage = 0
	unscheduled_usage = 0
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
				unscheduled_usage = calculate_energy_usage(ref, tv, micro, wm, dish, comp)
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
				scheduled_usage = calculate_energy_usage(iref, itv, imicro, iwm, idish, icomp)
				break
			linecount += 1

	int_savings = (unscheduled_usage - scheduled_usage)*100/unscheduled_usage 

	savings += int_savings


	return render_template("plan.html", ref= ref, tv= tv, micro=micro, wm=wm, dish=dish, comp=comp, iref=iref, itv=itv, imicro=imicro, iwm=iwm, idish=idish, icomp=icomp, schedulenum=schedule_num+1, int_savings = str(round(int_savings, 5)),savings=str(round(savings, 5)))
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, threaded=True)