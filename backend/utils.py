#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 17:04:56 2026

@author: nivetha
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv
from datetime import datetime

LOG_DIR = "/app/logs"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "agent_logs.csv")


def save_log(email, order_id, decision, reason):

    print("saving the log files")
    print("FINAL LOG FILE PATH:", LOG_FILE)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "email",
                "order_id",
                "decision",
                "reason"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            email,
            order_id,
            decision,
            reason
        ])

    print("log written successfully:", LOG_FILE)
