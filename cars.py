# 이메일 환경설정 및 테스트 이메일 송부

import smtplib
import email.message
import mimetypes
import os.path

import reportlab

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import pandas as pd
import json
import re

with open("./data/used_car_sales.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    data_list = []
    for num in range(len(lines)): #len(lines)
        if num == 0:
            dum_line=lines[num].split(",")
            print(dum_line)
        else:
            data_dict = {}
            car_dict = {}
            dum_line=lines[num].split(",")
            # print(dum_line)
            car_dict["car_make"] = re.sub('"',"",dum_line[5])
            car_dict["car_model"] = re.sub('"',"",dum_line[6])
            car_dict["car_year"] = re.sub('"',"",dum_line[7])
            data_dict["id"] = num #re.sub('"',"",dum_line[0])
            data_dict["car"] = car_dict
            data_dict["price"] = int(re.sub('"',"",dum_line[1]))
            data_dict["sold_year"] = re.sub('"',"",dum_line[2])
            data_dict["sales"] = 1
            data_dict["value_key"] = "_".join(list(car_dict.values())[0:2])
            data_list.append(data_dict)
print(len(data_list)) #122144대
print(data_list[0])

# json.dumps() 함수는 딕셔너리를 문자열로 바꾸는 점에 주의할 것.

cnt_dict = {}
for num in range(len(data_list)):
    # print(num)
    data = data_list[num]
    # print(data["car"])
    for k, v in data.items():
        if k == "value_key":
            if v in cnt_dict:
                cnt_dict[v] += 1
            else:
                cnt_dict[v] = 1

print(len(cnt_dict))

# reports.py
#!/usr/bin/env python3

import reportlab

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate(filename, title, additional_info, table_data):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h1"])
  report_info = Paragraph(additional_info, styles["BodyText"])
  table_style = [('GRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')]
  report_table = Table(data=table_data, style=table_style, hAlign="LEFT")
  empty_line = Spacer(1,20)
  report.build([report_title, empty_line, report_info, empty_line, report_table])

# emails.py
import email.message
import mimetypes
import os.path
import smtplib

def generate(sender, recipient, subject, body, attachment_path):
  """Creates an email with an attachement."""
  # Basic Email formatting
  message = email.message.EmailMessage()
  message["From"] = sender
  message["To"] = recipient
  message["Subject"] = subject
  message.set_content(body)

  # Process the attachment and add it to the email
  attachment_filename = os.path.basename(attachment_path)
  mime_type, _ = mimetypes.guess_type(attachment_path)
  mime_type, mime_subtype = mime_type.split('/', 1)

  with open(attachment_path, 'rb') as ap:
    message.add_attachment(ap.read(),
                          maintype=mime_type,
                          subtype=mime_subtype,
                          filename=attachment_filename)

  return message

def send(message):
  """Sends the message to the configured SMTP server."""
  mail_server = smtplib.SMTP('localhost')
  mail_server.send_message(message)
  mail_server.quit()

#!/usr/bin/env python3

# example.py
import emails_old
import os
import reports_old
import requests
table_data=[
  ['Name', 'Amount', 'Value'],
  ['elderberries', 10, 0.45],
  ['figs', 5, 3],
  ['apples', 4, 2.75],
  ['durians', 1, 25],
  ['bananas', 5, 1.99],
  ['cherries', 23, 5.80],
  ['grapes', 13, 2.48]]
reports_old.generate("/tmp/report.pdf", "A Complete Inventory of My Fruit", "This is all my fruit.", table_data)

sender = "sender@example.com"
receiver = "{}@example.com".format(os.environ.get('USER'))
subject = "List of Fruits"
body = "Hi\n\nI'm sending an attachment with all my fruit."

message = emails_old.generate(sender, receiver, subject, body, "/tmp/report.pdf")
emails_old.send(message)


# cars.py main
# student-03-748ac797144d
#!/usr/bin/env python3

import json
import locale
import sys


def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    # TODO: also handle most popular car_year

  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
  ]

  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  print(summary)
  # TODO: turn this into a PDF report

  # TODO: send the PDF report as an email attachment


if __name__ == "__main__":
  main(sys.argv)

