# -*- encoding: utf-8 -*-
import csv
import winline

def get_current_stat(month):
    try:
        f=open(month+'/total.stat')
        arr = [line.strip() for line in f]
        f.close()
        return arr
    except:
        return []
    
def save_bets(page,month,day):
    records = winline.get_records(page)
    flag=0;
    with open(month+'/'+day+"_"+month+"_results.csv", 'w',newline='') as csvfile:
        fieldnames = ['event_id', 'team_host','team_away','league',
                      'bet_type','expected_result','coefficient',
                      'actual_result','win_status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter =";")
        writer.writeheader()
        for record in records:
            writer.writerow(record)
            if record['win_status']=='undefined':
                flag = 1
    if flag:
        print(month,"_",day,": has undefined result")
    else:
        f=open(month+'/total.stat','a')
        f.write(day+'\n')
        f.close()
        