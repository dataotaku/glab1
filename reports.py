#!/usr/bin/env python3

import os
import reportlab

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import datetime

filename = "procesed.pdf"
title = "Processed Update on " + datetime.datetime.now().strftime("%Y/%m/%d")
print(title)

dir_nm = "./supplier-data/descriptions/"
flist = os.listdir(dir_nm)

info_list = []
for idx in range(len(flist)):
    with open(dir_nm + flist[idx], 'r') as fp:
        lines = fp.readlines()
        if len(lines) < 3:
            pass
        else:
            for num in range(len(lines)):
                if num == 0:
                    info_list.append(lines[num].strip())
                elif num == 1:
                    info_list.append(lines[num].strip())
    info_list.append(" ")

additional_info = "<br/>".join(info_list)

filename = "./supplier-data/processed.pdf"

def generate(filename, title, additional_info):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h1"])
  report_info = Paragraph(additional_info, styles["BodyText"])
  empty_line = Spacer(1,20)
  report.build([report_title, empty_line, report_info])

generate(filename=filename, title=title, additional_info=additional_info)