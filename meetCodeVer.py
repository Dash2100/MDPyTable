from bs4 import BeautifulSoup
import requests
import json

def meet(code):
    if code == "":
        return {"meetURL":"","Classroom":""}
    global sPeriodsem
    sUrl = f"http://s2.mingdao.edu.tw/AACourses/Web/qVT.php?F_sPeriodsem={sPeriodsem}&eID={code}"
    while True:
        try:
            print("trying " + str(code))
            meetHtml = requests.get(sUrl)
            break
        except:
            print("failed, retrying. code: " + str(code))
            continue
    meetPage = BeautifulSoup(meetHtml.text, 'html.parser')
    try:
        meetURL = meetPage.find('a').string.replace(" ","")
        classroom = meetPage.find('div', style="font-size:20px;").string.replace(" ","")
    except:
        return {"meetURL":"","Classroom":""}
    onlineCode = {"meetURL":meetURL,"Classroom":classroom}
    print(onlineCode)
    return onlineCode

def gettable(account,password):
    global sPeriodsem
    session_requests = requests.session()
    data = {'sureReg':'YES',
            'accessWay':'ACCOUNT',
            'wRole':'STD',
            'stdID':account,
            'stdPWD':password,
            'uRFID':'',
            'Submit':'%BDT%A9w%B5n%A4J'
            }
    url = 'http://s2.mingdao.edu.tw/AACourses/Web/wLogin.php'
    result = session_requests.post(url, data=data)

    html = BeautifulSoup(result.text, 'html.parser')

    all_sub,all_tea,all_room,all_code = list(),list(),list(),list()

    option = html.find('option', {'selected': True})
    sPeriodsem = option['value']
    subj = html.find_all("span" ,style="word-break:break-all;")
    for t in subj:
        sub = t.find("div", class_="subj")
        if sub != None:
            sub = sub.string.replace(" ","").replace("\n","")
            all_sub.append(sub)
        else:
            all_sub.append("")
        tea = t.find("div", class_="tea")
        if tea != None:
            tea = tea.string.replace(" ","").replace("\n","")
            all_tea.append(tea)
        else:
            all_tea.append("")
        room = t.find("div", class_="room")
        if room != None:
            room = room.string.replace(" ","").replace("\n","")
            all_room.append(room)
        else:
            all_room.append("")
        code = t.find("div",class_="tea")
        if code != None:
            str_start = str(code).find("view_Week_Sec('")+15
            code = str(code)[str_start:str_start+7]
            all_code.append(code)
        else:
            all_code.append("")

    table = {"day1":"","day2":"","day3":"","day4":"","day5":"","day6":""}
    day,index = 0,0

    for day in range(6):
        subjDict = dict()
        index = day
        for subNum in range(8):
            dataDict = {"subj":"","tea":"","room":"","online":""}
            dataDict["subj"] = all_sub[index]
            dataDict["tea"] = all_tea[index]
            dataDict["room"] = all_room[index]
            dataDict["online"] = meet(all_code[index])
            subjDict[subNum+1] = dataDict
            index += 6
        dayName = "day" + str(day+1)
        table[dayName] = subjDict
    print(table)
    with open('data.json', 'w', encoding="utf8") as f:
        json.dump(table, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # #?????????????????????????????????????????????
    account = ""
    password = ""
    gettable(account,password)