from flask import Flask, render_template, json, url_for
from datetime import datetime, timedelta, date, time

app = Flask(__name__)
istTimeDelta = timedelta(hours = 5,minutes = 30)


with open('./static/sample_json_1.json') as json_data:
    data1 = json.load(json_data)
with open('./static/sample_json_2.json') as json_data:
    data2 = json.load(json_data)
with open('./static/sample_json_3.json') as json_data:
    data3 = json.load(json_data)

#default route to give out instructions
@app.route('/')
def giveInstructions():
    details = "For Question 1 :<br>GET <a>https://backendinterntask.herokuapp.com/Q1/2021-01-28T12:00:00Z/2021-01-28T19:00:00Z</a><br><br>For Question 2 :<br>GET <a>https://backendinterntask.herokuapp.com/Q2/2021-01-28T12:00:00Z/2021-01-28T19:00:00Z</a><br><br>For Question 3 :<br>GET <a>https://backendinterntask.herokuapp.com/Q3/2021-01-28T12:00:00Z/2021-01-28T19:00:00Z</a><br><br>For custom endpoints replace dates in the URLs<br><br>Format for startTime and endTime:<br><br>%Y-%m-%dT%H:%M:%SZ<br>ex : 2021-01-28T12:00:00Z"
    return details

#Question 1
@app.route('/Q1/<string:startTime>/<string:endTime>')
def Q1(startTime,endTime):
    Astart = time(6,0)
    Aend = time(14,0)
    Bstart = time(14,0)
    Bend = time(20,0)
    Cstart = time(20,0)
    Cend = time(14,0)
    
    result = {
        "shiftA":{ "production_A_count" :0, "production_B_count" :0},
        "shiftB":{ "production_A_count" :0, "production_B_count" :0},
        "shiftC":{ "production_A_count" :0, "production_B_count" :0}
    }
    try:
        startTime = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%SZ') + istTimeDelta
        endTime = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%SZ') + istTimeDelta
    except:
        return "Invalid Date format"
    
    for i in data1:
        currTime = datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S') + istTimeDelta
        if (startTime.date() == date(2021,1,28) or startTime.date() == date(2021,1,29)) and (endTime.date() == date(2021,1,28) or endTime.date() == date(2021,1,29)):
            if Astart <= currTime.time() <= Aend and startTime<=currTime<=endTime:
                result['shiftA']['production_A_count'] += i['production_A']
                result['shiftA']['production_B_count'] += i['production_B']

            elif Bstart <= currTime.time() <= Bend and startTime<=currTime<=endTime:
                result['shiftB']['production_A_count'] += i['production_A']
                result['shiftB']['production_B_count'] += i['production_B']
            elif startTime<=currTime<=endTime:
                result['shiftC']['production_A_count'] += i['production_A']
                result['shiftC']['production_B_count'] += i['production_B'] 
        else:
            return "No Data Available for given date."

    return json.dumps(result,indent=4,sort_keys=False)

#Question 2
@app.route('/Q2/<string:startTime>/<string:endTime>')
def Q2(startTime,endTime):

    result = {
        "runtime" : "",
	    "downtime": "",
	    "utilisation": 0

    }
    try:
        startTime = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%SZ') + istTimeDelta
        endTime = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%SZ') + istTimeDelta
    except:
        return "Invalid Date format"
    runTime = 0
    downTime = 0
    for i in data2:
        currTime = datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S') + istTimeDelta
        if (startTime.date() == date(2021,1,28) or startTime.date() == date(2021,1,29)) and (endTime.date() == date(2021,1,28) or endTime.date() == date(2021,1,29)):
            if startTime <= currTime <= endTime:
                if i['runtime'] > 1021:
                    runTime += 1021
                    downTime += i['runtime'] - 1021 + i['downtime']
                else:
                    runTime += i['runtime']
                    downTime += i['downtime']
        else:
            return "No Data Available for given date."

    utilisation = runTime*100/(runTime+downTime)
    result['utilisation'] = round(utilisation,2)

    runtimeHours = runTime // 3600
    runTime %= 3600
    runtimeMins = runTime // 60
    if len(str(runtimeMins)) == 1:
        runtimeMins = '0' + str(runtimeMins)
    runtimeSeconds = runTime % 60
    if len(str(runtimeSeconds)) == 1:
        runtimeSeconds = '0' + str(runtimeSeconds)
    
    downtimeHours = downTime // 3600
    downTime %= 3600
    downtimeMins = downTime // 60
    if len(str(downtimeMins)) == 1:
        downtimeMins = '0' + str(downtimeMins)
    downtimeSeconds = downTime % 60
    if len(str(downtimeSeconds)) == 1:
        downtimeSeconds = '0' + str(downtimeSeconds)
    
    result['runtime'] = f'{runtimeHours}h:{runtimeMins}m:{runtimeSeconds}s'
    result['downtime'] = f'{downtimeHours}h:{downtimeMins}m:{downtimeSeconds}s'

    return json.dumps(result,indent=4,sort_keys=False)

#Question 3
@app.route('/Q3/<string:startTime>/<string:endTime>')
def Q3(startTime,endTime):

    result = []
    try:
        startTime = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%SZ') + istTimeDelta
        endTime = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%SZ') + istTimeDelta
    except:
        return "Invalid Date format"
    uniqueIds = []
    dataForGivenTime = []
    for i in data3:
        currTime = datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S') + istTimeDelta
        if (startTime.date() == date(2021,1,28) or startTime.date() == date(2021,1,29)) and (endTime.date() == date(2021,1,28) or endTime.date() == date(2021,1,29)):
            if startTime <= currTime <= endTime:
                uniqueIds.append(i['id'])
                dataForGivenTime.append(i)    
        else:
            return "No Data Available for given date."
    
    uniqueIds = list(set(uniqueIds))
    uniqueIds.sort()
    print(uniqueIds)

    for i in uniqueIds:
        avg_belt1 = 0
        avg_belt2 = 0
        ct = 0
        id = i
        id = int(id.replace('ch',''))
        for j in dataForGivenTime:
            if j['id'] == i:
                ct+=1
                if j['state'] == True:
                    avg_belt2 = ((avg_belt2 * (ct-1)) + j['belt2'])//ct
                else:
                    avg_belt1 = ((avg_belt1 * (ct-1)) + j['belt1'])//ct
        result.append({"id":id,"avg_belt1":avg_belt1,"avg_belt2":avg_belt2})

    return json.dumps(result,indent=4,sort_keys=False)

if __name__ == "__main__":
    app.run(debug=True)