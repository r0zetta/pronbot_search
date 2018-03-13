import pygal
import os

def dump_bar_chart(dirname, filename, title, x_labels, chart_data):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    filepath = os.path.join(dirname, filename)
    label_count = len(x_labels)
    if label_count > 10:
        label_count = 10
    chart = pygal.Bar(show_y_guides=True, x_labels_major_count=label_count, show_minor_x_labels=False, show_minor_y_labels=True, x_label_rotation=20)
    chart.title = title
    chart.x_labels = x_labels
    for name, stuff in chart_data.iteritems():
        chart.add(name, stuff)
    chart.render_to_file(filepath)

def dump_line_chart(dirname, filename, title, x_labels, chart_data):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    filepath = os.path.join(dirname, filename)
    label_count = len(x_labels)
    if label_count > 10:
        label_count = 10
    chart = pygal.Line(show_y_guides=True, show_dots=False, x_labels_major_count=5, show_minor_x_labels=False, show_minor_y_labels=True, x_label_rotation=20)
    chart.title = title
    chart.x_labels = x_labels
    for name, stuff in chart_data.iteritems():
        chart.add(name, stuff)
    chart.render_to_file(filepath)

def dump_pie_chart(dirname, filename, title, chart_data):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    filepath = os.path.join(dirname, filename)
    total = 0
    for n, c in chart_data.iteritems():
        total += c
    pie_chart = pygal.Pie(truncate_legend=-1)
    pie_chart.title = title
    output_count = 0
    for n, c in sorted(chart_data.iteritems(), key=lambda x:x[1], reverse = True):
        percent = float(float(c)/float(total))*100.00
        label = n + " (" + "%.2f" % percent + "%)"
        pie_chart.add(label, c)
        output_count += 1
        if output_count > 15:
            break
    pie_chart.render_to_file(filepath)

