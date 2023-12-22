#!/usr/bin/env python3

import json
import locale
import sys
import emails
import reports

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
  max_sales = {"sales":0}
  max_year = {}
  for item in data:
    # Calculate the revenue gienerated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    if item["total_sales"] > max_sales["sales"]:
        item["sales"] = item["total_sales"]
        max_sales = item

    # TODO: also handle most popular car_year
    if item["car"]["car_year"] in max_year:
        max_year[item["car"]["car_year"]] += item["total_sales"]
    else:
        max_year[item["car"]["car_year"]] = item["total_sales"]

  for k, v in max_year.items():
      if v == max(max_year.values()):
          max_target_yr = k
          max_target_sales = v

  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {} had the most sales: {}".format(
      format_car(max_sales["car"]), max_sales["sales"]),
    "The most popular year was {} with {} sales.".format(
      max_target_yr, max_target_sales)
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
  dict_table = cars_dict_to_table(data)
  reports.generate("/tmp/cars.pdf", "Sales Summmay for last month<br/>",
          "\n".join(summary), dict_table)
  # TODO: send the PDF report as an email attachment
  msg = emails.generate("automation@example.com", "student-03-748ac797144d@example.com",
          "Sales summary for last month", "The same summary from the PDF, but using \n between the lines",
          "/tmp/cars.pdf")
  emails.send(msg)

if __name__ == "__main__":
  main(sys.argv)
