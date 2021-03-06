from threading import Thread
import pandas
import matplotlib.pyplot as plt
import shutil
import os
import subprocess
import time
from django.template import loader
import signal
from django.http import HttpResponse
from django.shortcuts import render, redirect


import re
threads=[]
stop=False
proc1 = None
live_flag=0
live_n=None
live_p=None
live_number_of_lines=None
live_pattern=None
req = None
n_global=None
p_global=None
running_status=0
def IndexView(request):
    global stop
    global threads
    global live_flag
    global live_n
    global live_p
    global live_number_of_lines
    global live_pattern
    global req
    global n_global
    global proc1
    global p_global
    global running_status
    variable=0
    variable2=0
    data=""

    live_flag=0
    if live_flag ==1:

        if ("Live_Stop" in request.POST):
            live_flag = 0
            template = loader.get_template('index.html')
            context = {'variable': variable, 'data': data, 'variable2': variable2,
                       }
            return HttpResponse(template.render(context, request))

        data2=[]
        list=[]
        time.sleep(1)
        live(live_n, live_p, live_number_of_lines, "a")
        print("Harsh Hi")
        variable = 0
        variable2 = 1
        for i in range(live_n):
            f = open("/anode%d" % (i + 1), "r")
            list.append(i)
            data = f.read()
            data2.append((data, i))
        print(data2)
        print(len(data2))

        template = loader.get_template('index.html')
        context = {'variable': variable, 'data': data, 'data2': data2, 'variable2': variable2, 'list': list,
                   }
        return HttpResponse(template.render(context, request))
    else:
        if request.method == "POST":
            print(request)
            if request.POST["value_n"] :
                value_n = request.POST["value_n"]
                if value_n != "":
                    value_n = int(value_n)
                    n_global=value_n
                print(value_n)
            if request.POST["value_p"]:
                value_p = request.POST["value_p"]
                if value_p != "":
                    value_p = int(value_p)
                    p_global=value_p
                print(value_p)

            if ("Start" in request.POST) :
                process = Thread(target=run_script, args=[value_n, value_p])
                process.start()
                threads.append(process)
                print(threads)
                running_status=1

            if ("Stop" in request.POST) and (live_flag != 1):
                while(os.path.isdir('log_simulator')):
                    os.system('rm -rf log_simulator')

                print("####################STOPPED#######################")
                stop = False
                for process in threads:
                    process.join()
                running_status=0

            if ("Print" in request.POST):
                n_val = int(request.POST["n"])
                p_val = int(request.POST["p"])
                pattern = request.POST["pattern"]
                number_lines = int(request.POST["number_of_lines"])
                headTen(n_val, p_val, number_lines, pattern, "/home/harsh/PycharmProjects/CloudInit/log.txt")
                f = open("log.txt", "r")
                data = f.read()
                variable = 1

            data2 = []
            list = []


            template = loader.get_template('index.html')
            context = {'variable': variable, 'data': data, 'data2': data2, 'variable2': variable2, 'list': list, 'running_status':running_status,
                       }
            return HttpResponse(template.render(context, request))

        else:

            template = loader.get_template('index.html')
            context = {'variable': variable, 'data': data, 'variable2': variable2, 'running_status':running_status,
                          }
            return HttpResponse(template.render(context, request))



def LiveView(request):
    global live_flag
    global live_n
    global live_p
    global live_number_of_lines
    global live_pattern
    global n_global
    variable2=0
    if live_flag ==1:
        if ("Live_Stop" in request.POST):
            live_flag = 0
            template = loader.get_template('live.html')
            context = {'variable2': variable2,
                       }
            return HttpResponse(template.render(context, request))

        data2=[]
        list=[]
        time.sleep(1)
        live(live_n, live_p, live_number_of_lines, "a")
        variable2 = 1
        for i in range(live_n):
            df = pandas.read_csv("anode%d.csv"%(i+1), sep=',')
            data = df.to_html()
            list.append(i)
            data2.append((data, i))

        template = loader.get_template('live.html')
        context = {'data2': data2, 'variable2': variable2, 'list': list,
                   }
        return HttpResponse(template.render(context, request))
    else:
        if request.method == "POST":

            data2 = []
            list = []

            if ("Print_live" in request.POST):
                live_n = n_global
                live_p = int(request.POST["p_live"])
                live_number_of_lines = int(request.POST["live_number_of_lines"])
                live_flag = 1
                if live_flag == 1:
                    time.sleep(1)
                    live(live_n, live_p, live_number_of_lines,  "a")
                    variable = 0
                    variable2 = 1
                    for i in range(live_n):
                        df = pandas.read_csv("anode%d.csv" % (i + 1), sep=',')
                        data = df.to_html()
                        list.append(i)
                        data2.append((data, i))


                    template = loader.get_template('live.html')
                    context = { 'data2': data2, 'variable2': variable2, 'list': list,
                        }
                    return HttpResponse(template.render(context, request))
            template = loader.get_template('live.html')
            context = { 'data2': data2, 'variable2': variable2, 'list': list,
                       }
            return HttpResponse(template.render(context, request))

        else:
            template = loader.get_template('live.html')
            context = {'variable2': variable2,
                          }
            return HttpResponse(template.render(context, request))

def TimeView(request):
    variable3 = 0
    data_time = ""
    global n_global
    print(request.POST)
    if (request.method == "POST"):
        n_time = int(request.POST['n_time'])
        p_time = int(request.POST['p_time'])
        start = request.POST['date_start']
        end = request.POST['date_end']
        live(n_global,p_time,1000,"a")
        TimeData(n_time, p_time, start, end)
        df = pandas.read_csv("time.csv", sep=',')
        data_time = df.to_html()
        variable3 = 1

        template = loader.get_template('time.html')
        context = {'variable3': variable3, 'data_time': data_time,
                   }
        return HttpResponse(template.render(context, request))

    else:
        template = loader.get_template('time.html')
        context = {'variable3': variable3, 'data_time': data_time,
                   }
        return HttpResponse(template.render(context, request))

def TimelineView(request):
    global n_global
    global p_global
    variable=0
    data_timeline =[]

    if(request.method == 'POST'):
        number_of_lines = int(request.POST['number_of_lines'])
        timeline(n_global,p_global,number_of_lines)
        df = pandas.read_csv("timeline.csv", sep=',')
        data_timeline = df.to_html()
        variable=1
        print(data_timeline)

        template = loader.get_template('timeline.html')
        context = {'variable':variable, 'data_timeline':data_timeline}
        return HttpResponse(template.render(context,request))



    else:
        variable=0
        data_timeline=[]
        template = loader.get_template('timeline.html')
        context = {'variable':variable, 'data_timeline':data_timeline}
        return HttpResponse(template.render(context,request))

def GraphView(request):
    variable=0
    global n_global
    if (request.method == "POST"):
        variable=1
        n_graph = n_global
        p_graph = int(request.POST['p_graph'])
        num_graph = int(request.POST['num_graph'])
        search = request.POST['search']
        process_counts(n_graph, p_graph, num_graph, search)
        list=[]
        data=[]
        for i in range(n_graph):
            list.append((i,i+1))
            data.append(("plotNode_%d.png"%(i+1),"plotNode_pie_%d.png"%(i+1),i))

        print(data)
        print(list)
        template = loader.get_template('graph.html')
        context = {'variable': variable,
        'list':list,
        'data':data
                   }
        return HttpResponse(template.render(context, request))

    else:
        template = loader.get_template('graph.html')
        context = {'variable': variable,
                   }
        return HttpResponse(template.render(context, request))


def timeline(n,p,num):
    file_path2="log_simulator/"
    i=1
    while i<=n:
        j=1
        while j<=p:
            filename=file_path2+'HackNode'+str(i)+"/Process"+str(j)+".log"
            lines="".join(tail(filename,num)).split('\n')
            FR=open("timeline.csv","w")
            FR.write("Date,Time,Node,Process,Tag,File,Exception"+"\n")
            FR.close()
            FR=open("timeline.csv","a+")
            for line in lines :
                l=line.split()
                # if line.find(keyword):
                #     print(line)
                if (re.match("^\d",line)!=None):
                    #   print(l)
                    FR.write(l[0] + " , "+str(l[1])+ " , " + str(i)+ " , " +str(j) + " , "+l[2]+" , "+l[3]+" , "+" ".join(l[4:])+"\n")
                    print(str(l[0]) + "|  "+str(l[1])+ "| NODE :" + str(i)+ "| PROCESS :" +str(j) + "| MATCH LINE:"+str(" ".join(l[2:]))+"\n")
            j+=1
            FR.close()
        i+=1






def process_counts(n, process, num, extra):
    i = 1
    extra = extra.split(',')
    file_path1='log_simulator/'
    while i <= n:
        filename = file_path1 + 'HackNode' + str(i) + "/Process" + str(process) + ".log"
        count_info = 0
        count_dbg = 0
        count_error = 0
        string = "".join(tail(filename, num))
        extra_y = [0] * len(extra)
        for line in string.split('\n'):
            print(line)
            if line.find('DBG') >= 0:
                count_dbg += 1
            elif line.find('ERROR') >= 0:
                count_error += 1
            elif line.find('INFO') >= 0:
                count_info += 1
            for j in range(0, len(extra)):
                if re.search(extra[j], line, re.I):
                    extra_y[j] += 1

        x = ["INFO", "DBG", "ERROR"] + extra
        y = [count_info, count_dbg, count_error] + extra_y
        barplot(x, y, i, num)
        i += 1


def barplot(x, y, i, num):
    # my_color=tuple([round(i/(len(x)+1),1) for i in range(1,len(x)+1)])
    # print(my_color)
    plt.bar(x, y)
    plt.xlabel('Category')
    plt.ylabel('Number of occurrence in last ' + str(num) + ' logs in node ' + str(i))
    plt.savefig('media/plotNode_' + str(i))
    plt.close()

    plt.pie(y, labels=x)
    plt.savefig('media/plotNode_pie_' + str(i))
    plt.close()








def run_script(n,p):
    global proc1
    proc1 = subprocess.Popen("python2 log_simulator.zip -n %d -p %d" %(n,p), shell=True)

def headTen(node, process, num, pattern, outputfilename):
    filename = 'log_simulator/HackNode' + str(node) + "/Process" + str(process) + ".log"
    FO = open(filename, 'r')
    FR = open(outputfilename, 'w')
    count = 0
    while True and count < num:
        loglines = FO.readline()
        if loglines.find(pattern) >= 0:
            # print(loglines)
            # loglines = loglines +"<br>"
            FR.write(loglines)
            count += 1

# def live(n,process,num,pattern,outputfilename):
#     file_path1 = '/home/harsh/PycharmProjects/CloudInit/log_simulator/'
#     delay=0
#     time.sleep(delay)
#     i=1
#     while i <= n:
#         filename=file_path1+'HackNode'+str(i)+"/Process"+str(process)+".log"
#         FR=open(outputfilename+"node"+str(i),'w')
#         to_print = "".join(tail(filename,num))
#         if re.search(pattern, to_print, re.I):
#             FR.write(to_print)
#             print(to_print)
#         FR.close()
#         i+=1

# def live(n, process, num, outputfilename):
#     file_path1 = '/home/harsh/PycharmProjects/CloudInit/log_simulator/'
#     delay = 0.1
#     time.sleep(delay)
#     i = 1
#     while i <= n:
#         filename = file_path1 + 'HackNode' + str(i) + "/Process" + str(process) + ".log"
#         FR = open(outputfilename + "node" + str(i)+".csv", 'w')
#         FR.write("Date,Timestamp,Tags,File,Exception" + "\n")
#         FR.close()
#         FR = open(outputfilename + "node" + str(i)+".csv", 'a+')
#         to_print = "".join(tail(filename, num))
#         to_print = to_print.split("\n")
#         count = 0
#         flag = 0
#         for x in to_print:
#             count += 1
#             if ((re.match("^\d", x) == None)):
#                 if (x.split(" ")[0] == "Traceback"):
#                     flag = 4
#
#                 print(x)
#                 flag -= 1
#             else:
#                 if (count > num):
#                     continue
#                 t = x.split(" ")
#                 a = " ".join(t[4:])
#                 b = ",".join(t[0:4])
#                 toprint = b + "," + a
#                 if (count != num):
#                     FR.write(toprint + "\n")
#                     # print(toprint)
#                 else:
#                     FR.write(toprint)
#                     # print(toprint)
#
#         # to_print[5]= " ".join(to_print[5:])
#         # to_print = ",".join(to_print[0:5])
#         # print(to_print)
#         print("\n")
#         # if re.search(pattern, to_print, re.I):
#         #     FR.write(to_print)
#         #     print(to_print)
#         FR.close()
#         # with open(outputfilename+"node"+str(i),'r') as infile, open(outputfilename+"node_"+str(i), 'a+') as outfile:
#         #     for line in infile:
#         #         outfile.write(" ".join(line.split()).replace(' ', ','))
#         #         outfile.write(",")
#         i += 1


def live(n, process, num, outputfilename):
    file_path1 = 'log_simulator/'
    delay = 0.01
    time.sleep(delay)
    i = 1
    while i <= n:
        filename = file_path1 + 'HackNode' + str(i) + "/Process" + str(process) + ".log"
        FR = open(outputfilename + "node" + str(i) + '.csv', 'w')
        FR.write("Date,Timestamp,Tags,File,Exception" + "\n")
        FR.close()
        FR = open(outputfilename + "node" + str(i) + '.csv', 'a+')
        to_print = "".join(tail(filename, num))
        to_print = to_print.split("\n")
        count = 0
        for x in to_print:
            count += 1
            if ((re.match("^\d", x) == None)):
                if (re.match("^\s", x) != None):
                    y = x.split(",")
                    print(" - , - ," + y[0] + "," + y[1] + ", Traceback" + y[2])
                    FR.write(" - , - ," + y[0] + "," + y[1] + ", Traceback" + y[2] +"\n")
                #  print("-,-,"+x)
                elif (x.split(" ")[0] == "Traceback"):
                    continue
                else:
                    y = x.split(":")
                    if (len(y) > 1):
                        FR.write(" - , - , " + y[0] + " , - ," + y[1] + "\n")
                        print(" - , - , " + y[0] + " , - ," + y[1])
            else:
                if (count > num):
                    continue
                t = x.split(" ")
                a = " ".join(t[4:])
                b = ",".join(t[0:4])
                toprint = b + "," + a
                if (count != num):
                    FR.write(toprint + "\n")
                    print(toprint)
                else:
                    FR.write(toprint)
                    print(toprint)

        # to_print[5]= " ".join(to_print[5:])
        # to_print = ",".join(to_print[0:5])
        # print(to_print)
        print("\n")
        # if re.search(pattern, to_print, re.I):
        #     FR.write(to_print)
        #     print(to_print)
        FR.close()
        # with open(outputfilename+"node"+str(i),'r') as infile, open(outputfilename+"node_"+str(i), 'a+') as outfile:
        #     for line in infile:
        #         outfile.write(" ".join(line.split()).replace(' ', ','))
        #         outfile.write(",")
        i += 1

def tail(fi, n):
    f = open(fi, 'r')
    assert n >= 0
    pos, lines = n + 1, []
    while len(lines) <= n:
        try:
            f.seek(-pos, 2)
        except IOError:
            f.seek(0)
            break
        finally:
            lines = list(f)
        pos *= 2
    return lines[-n:]




def TimeData(n,p,start,end):
    startDate=start
    endDate=end
    print(startDate)
    print(endDate)


    date_re = re.compile(r'(\d+-\d+-\d+\,\d+:\d+:\d+)')
    with open("anode%d.csv"%(n), "r") as fh:
        FR = open("time.csv", "w")
        FR.write("Date,Timestamp,Tag,File,Exception" + "\n")
        FR.close()
        for line in fh.readlines():
            match = date_re.search(line)
            if match is not None:
                matchDate = match.group(1)
                if matchDate >= startDate and matchDate <= endDate:
                    FR = open("time.csv", 'a+')
                    t = line.split(",")

                    FR.write(line)
