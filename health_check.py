#! /urs/bin/env python3

import shutil
import psutil
import socket
import report_email

cpu_usage_rate = psutil.cpu_percent()
available_memory = psutil.virtual_memory()
memory_avail_mb = round(available_memory.available/1024**2,0)

disk_free = shutil.disk_usage("/")
disk_free_rate = round(disk_free.free / disk_free.total, 2)

catch_alert = "clean"

if cpu_usage_rate > 80:
    catch_alert = "CPU_ALERT"
elif memory_avail_mb < 500:
    catch_alert = "MEMORY_ALERT"
elif disk_free_rate < 0.2:
    catch_alert = "DISK_ALERT"
elif socket.gethostbyname("localhost") != "127.0.0.1":
    catch_alert = "RESOLVE_ALERT"

if catch_alert == "clean":
    pass
elif catch_alert in ("CPU_ALERT", "MEMORY_ALERT", "DISK_ALERT", "RESOLVE_ALERT"):
    alert_situation = {"CPU_ALERT": "Error - CPU usage is over 80%",
                    "DISK_ALERT": "Error - Available disk space is less than 20%",
                    "MEMORY_ALERT": "Error - Available memory is less than 500MB",
                    "RESOLVE_ALERT": "Error - localhost cannot be resolved to 127.0.0.1"}

    subject_paragraph = alert_situation[catch_alert]

    msg = report_email.gmail_generate(sender="automation@example.com", 
                        recipient="study_hard@example.com",
                        subject=subject_paragraph,
                        body="Please check your system and resolve the issue as soon as possible", 
                        attachment_path=None)

    report_email.send_gmail(msg)