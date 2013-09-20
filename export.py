#coding=utf-8
import base
import logger
import math

def output_html():
    """ Export to HTML and making graphs (lib morris.js) """
    with open(u"export/output.html", u"w") as htmlfile:
        htmlfile.writelines(u"<!doctype html>\n" + \
                            u"<html dir=\"ltr\" xmlns=\"http://www.w3.org/1999/xhtml\">\n" + \
                            u"<head>\n" + \
                            u"<script src=\"lib/jquery.min.js\"></script>\n" + \
                            u"<script src=\"lib/raphael-min.js\"></script>\n" + \
                            u"<script src=\"lib/morris.js\"></script>\n" + \
                            u"<script src=\"lib/prettify.js\"></script>\n" + \
                            u"<link rel=\"stylesheet\" href=\"lib/example.css\">\n" + \
                            u"<link rel=\"stylesheet\" href=\"lib/prettify.css\">\n" + \
                            u"<link rel=\"stylesheet\" href=\"lib/morris.css\">\n" + \
                            u"</head>\n" + \
                            u"<body>\n" + \
                            u"<table \" id=\"table-info\">\n" + \
                            u"<tr><td>Name of coefficient</td><td>Value</td></tr>\n" + \
                            u"<tr><td> Efficiency of the system <strong>r</strong> </td><td> " + str(base.r) + u"</td></tr>\n" + \
                            u"<tr><td> The average wait time of the request in the queue <strong>qT</strong> </td><td> " + str(base.qT) + u"</td></tr>\n" + \
                            u"<tr><td> The average residence time of the request in the system <strong>sT</strong>  </td><td> " + str(base.sT) + u"</td></tr>\n" + \
                            u"<tr><td> The average number of claims in the queue at the time <strong>qN</strong>  </td><td> " + str(base.qN) + u"</td></tr>\n" + \
                            u"<tr><td> The average number of claims in the system at the time <strong>sN</strong>  </td><td> " + str(base.sN) + u"</td></tr>\n" + \
                            u"<tr><td> Absolute bandwidth <strong>aC</strong>  </td><td> " + str(base.aC) + u"</td></tr>\n" + \
                            u"<tr><td> Relative bandwidth <strong>rC</strong> </td><td> " + str(base.rC) + u"</td></tr>\n" + \
                            u"<tr><td> The number of established requirements <strong>ad_counter</strong></td><td> " + str(base.ad_counter) + u"</td></tr>\n" + \
                            u"<tr><td> End time </td><td> " + str(base.end_time) + u"</td></tr>\n" + \
                            u"</table>\n" + \
                            u"<h1> Graphs of distributions of random variables (delivery requirements) </h1>\n" + \
                            u"<div id=\"graph11\"></div>\n" + \
                            u"<h1> Graph of distributions of random variables (processing requirements) </h1>\n" + \
                            u"<div id=\"graph12\"></div>\n" + \
                            u"<h1> Graph of density distribution of random variables (delivery requirements) </h1>\n" + \
                            u"<div id=\"graph21\"></div>\n" + \
                            u"<h1> Graph of density distribution of random variables (processing requirements) </h1>\n" + \
                            u"<div id=\"graph22\"></div>\n" + \
                            u"<h1> Graph of the number of claims in the queue at the time </h1>\n" + \
                            u"<div id=\"graph3\"></div>\n" + \
                            u"<h1> Graph of the number of claims in the system at the time </h1>\n" + \
                            u"<div id=\"graph4\"></div>\n" + \
                            u"<h1> Graph of the average number of claims in the queue at the time </h1>\n" + \
                            u"<div id=\"graph5\"></div>\n" + \
                            u"<h1> Graph of the average number of claims in the system at the time </h1>\n" + \
                            u"<div id=\"graph6\"></div>\n" + \
                            u"<h1> Graph of the coefficient value at the time </h1>\n" + \
                            u"<div id=\"graph7\"></div>\n" + \
                            u"<div id=\"graph8\"></div>\n" + \
                            u"<div id=\"graph9\"></div>\n" + \
                            u"<div id=\"graphHist1\"></div>\n" + \
                            u"<div id=\"graphHist2\"></div>\n")
        htmlfile.write(u"<script>\n")

        base.prc_time_list = sorted(base.prc_time_list)
        base.adm_time_list = sorted(base.adm_time_list)
        # 1.1 - graph 11
        htmlfile.write(u"Morris.Line({\n")
        htmlfile.write(u"element: 'graph11',\n")
        htmlfile.write(u"data: [\n")
        # 1-exp(-x(i)/m)
        i = 0
        while i < len(base.adm_time_list):
            htmlfile.write(u"  {x: " + str(base.adm_time_list[i]) + \
                           u", y: " + str(1 - math.exp(-1 * base.adm_time_list[i])) + u"},\n")
            i += 1
        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['WaitTime', ' '],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        # 1.2 - graph 12
        htmlfile.write(u"Morris.Line({\n")
        htmlfile.write(u"element: 'graph12',\n")
        htmlfile.write(u"data: [\n")
        # 1-exp(-x(i)/m)
        i = 0
        while i < len(base.prc_time_list):
            htmlfile.write(u"  {x: " + str(base.prc_time_list[i]) + \
                           u", y: " + str(1 - math.exp(-1 * base.prc_time_list[i])) + u"},\n")
            i += 1
        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['ExecTime', ' '],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")


        #2.1 - graph 21
        htmlfile.write(u"Morris.Line({\n")
        htmlfile.write(u"element: 'graph21',\n")
        htmlfile.write(u"data: [\n")

        i = 0
        while i < len(base.adm_time_list):
            htmlfile.write(u"  {x: " + str(base.adm_time_list[i]) + \
                           u", y: " + str(math.exp(-1 * base.adm_time_list[i]) / base.avg_admission_time) + u"},\n")
            i += 1
        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['WaitTime', 'Exp'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #2.2 - graph 22
        htmlfile.write(u"Morris.Line({\n")
        htmlfile.write(u"element: 'graph22',\n")
        htmlfile.write(u"data: [\n")

        i = 0
        while i < len(base.prc_time_list):
            htmlfile.write(u"  {x: " + str(base.prc_time_list[i]) + \
                           u", y: " + str(math.exp(-1 * base.prc_time_list[i]) / base.avg_processing_time) + u"},\n")
            i += 1
        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['ExecTime', 'Exp'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #3 - graph3
        htmlfile.write(u"Morris.Area({\n")
        htmlfile.write(u"element: 'graph3',\n")
        htmlfile.write(u"data: [\n")

        logger.sorted_items_in_stack = logger.sorted_dict_keys(logger.items_in_stack)

        for item in logger.sorted_items_in_stack:
            htmlfile.write(u"  {x: " + str(item[0]) +  \
                           u", y: " + str(item[1]) + u"},\n")

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['Count', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #4 - graph4
        htmlfile.write(u"Morris.Area({\n")
        htmlfile.write(u"element: 'graph4',\n")
        htmlfile.write(u"data: [\n")

        logger.sorted_items_in_work = logger.sorted_dict_keys(logger.items_in_work)

        for item in logger.sorted_items_in_work:
            htmlfile.write(u"  {x: " + str(item[0]) +  \
                           u", y: " + str(item[1]) + u"},\n")

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['Count', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #5 - graph5
        htmlfile.write(u"Morris.Area({\n")
        htmlfile.write(u"element: 'graph5',\n")
        htmlfile.write(u"data: [\n")

        cur_count = 0
        for item in logger.sorted_items_in_stack:
            cur_count += 1
            htmlfile.write(u"  {x: " + str(item[0]) +  \
                           u", y: " + str(float(logger.get_count_sum_stack(item[0]) / cur_count)) + u"},\n")

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['Avg.Count', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #6 - graph6
        htmlfile.write(u"Morris.Area({\n")
        htmlfile.write(u"element: 'graph6',\n")
        htmlfile.write(u"data: [\n")

        cur_count = 0
        for item in logger.sorted_items_in_work:
            cur_count += 1
            htmlfile.write(u"  {x: " + str(item[0]) +  \
                           u", y: " + str(float(logger.get_count_sum_work(item[0]) / cur_count)) + u"},\n")

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['Avg.Count', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #7 - graph7
        htmlfile.write(u"Morris.Area({\n")
        htmlfile.write(u"element: 'graph7',\n")
        htmlfile.write(u"data: [\n")

        logger.sorted_coefs_per_time = logger.sorted_dict_keys(logger.coefs_per_time)

        for item in logger.sorted_coefs_per_time:
            htmlfile.write(u"  {x: " + str(item[0]) + \
                           u", y: " + str(item[1]) + u"},\n")

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['coeff', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #8 - graph8
        htmlfile.write(u"Morris.Line({\n")
        htmlfile.write(u"element: 'graph8',\n")
        htmlfile.write(u"data: [\n")

        i = 1
        while i < 20:
            htmlfile.write(u"  {x: " + str(i) + \
                           u", y: " + str(logger.get_correlation_adm(base.array_adm, i))+ u"},\n")
            i += 1

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['coeff', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #9 - graph9
        htmlfile.write(u"Morris.Line({\n")
        htmlfile.write(u"element: 'graph9',\n")
        htmlfile.write(u"data: [\n")

        i = 1
        while i < 20:
            htmlfile.write(u"  {x: " + str(i) + \
                           u", y: " + str(logger.get_correlation_proc(base.array_proc, i))+ u"},\n")
            i += 1

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['coeff', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")

        #10 - graph10
        htmlfile.write(u"Morris.Bar({\n")
        htmlfile.write(u"element: 'graphHist1',\n")
        htmlfile.write(u"data: [\n")

        i = 0
        while i < len(base.hist_adm_x):
            htmlfile.write(u"  {x: " + str(base.hist_adm_x[i]) + \
                           u", y: " + str(base.hist_adm_y[i]) + u"},\n")
            i += 1

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['coeff', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")


        #11 - graph11
        htmlfile.write(u"Morris.Bar({\n")
        htmlfile.write(u"element: 'graphHist2',\n")
        htmlfile.write(u"data: [\n")

        i = 0
        while i < len(base.hist_proc_x):
            htmlfile.write(u"  {x: " + str(base.hist_proc_x[i]) + \
                           u", y: " + str(base.hist_proc_y[i]) + u"},\n")
            i += 1

        htmlfile.write(u"],\n" + \
                        u"xkey: 'x',\n" + \
                        u"ykeys: 'y',\n" + \
                        u"labels: ['coeff', 'Count'],\n" + \
                        u"parseTime: false,\n" + \
                        u"pointSize: 0,\n" + \
                        u"integerYLabels: true\n" + \
                        u"});\n")


        #==========================
        htmlfile.write(u"</script>\n" + \
                        u"</body>")

        with open("export/fact_out.html", "a") as txtfile:
            txtfile.writelines( #"<table border=1>\n" +
                                #"<tr><td> N </td><td> rand A </td><td> rand B </td><td> r </td><td> Ts </td><td> Tq </td><td> Ns </td><td> Nq </td><td> Ca </td><td> Cr </td></tr>\n" +
                                "<tr><td> 2 </td><td>"+str(base.admission_init_value)+"</td><td>"+str(base.processing_init_value)+"</td><td>"+str(base.r)+"</td>\n" +
                                    "<td>"+str(base.sT)+"</td><td>"+str(base.qT)+"</td><td>"+str(base.sN)+"</td><td>"+str(base.qN)+"</td><td>"+str(base.rC)+"</td><td>"+str(base.aC)+"</td></tr>\n"
                                #"</table>"
                                )

