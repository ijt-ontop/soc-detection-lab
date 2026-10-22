import csv
import random
import subprocess
import time
from datetime import datetime
from pathlib import Path

# PROJECT 2 — DAY 4 SOC SIMULATION

import os

HOST = os.environ.get("SOC_LAB_HOST", "labuser@WINDOWS_ENDPOINT_IP")
KEY = Path(
    os.environ.get(
        "SOC_LAB_SSH_KEY",
        str(Path.home() / ".ssh" / "soc_lab_key")
    )
)
BASE = Path.home() / "soc-lab" / "day4"
DURATION = 3600

rng = random.SystemRandom()

# normal background activity, including authorised commands
# that can trigger custom detection rules

BENIGN = [
    ("Hostname check", "cmd /c hostname", ""),
    ("Process listing", "cmd /c tasklist", ""),
    ("System information", "cmd /c systeminfo", ""),
    (
        "Service check",
        'powershell -NoProfile -Command "Get-Service | Select-Object -First 8"',
        "",
    ),
    (
        "Date check",
        'powershell -NoProfile -Command "Get-Date"',
        "",
    ),
    ("Authorised identity check", "cmd /c whoami.exe", "100200"),
    ("Authorised network check", "cmd /c ipconfig.exe", "100201"),
]

# three controlled adversarial scenarios
# these simulate suspicious behaviour without malware or exploitation

CASES = [
    (
        "CASE-01",
        [
            ("Identity discovery", "cmd /c whoami.exe", "100200"),
            ("Account enumeration", "cmd /c net user", ""),
            (
                "Administrator enumeration",
                "cmd /c net localgroup administrators",
                "",
            ),
            ("Network discovery", "cmd /c ipconfig.exe", "100201"),
        ],
    ),
    (
        "CASE-02",
        [
            (
                "Encoded PowerShell",
                "powershell -NoProfile -EncodedCommand RwBlAHQALQBEAGEAdABlAA==",
                "",
            ),
            (
                "Process discovery",
                'powershell -NoProfile -Command "Get-Process | Select-Object -First 8"',
                "",
            ),
            (
                "Outbound HTTPS",
                'powershell -NoProfile -Command '
                '"Invoke-WebRequest https://www.wikipedia.org '
                '-UseBasicParsing -TimeoutSec 15 | Out-Null"',
                "100203",
            ),
        ],
    ),
    (
        "CASE-03",
        [
            (
                "Stage benign executable",
                "cmd /c copy /Y C:\\Windows\\System32\\whoami.exe "
                "%USERPROFILE%\\Downloads\\lab-test.exe",
                "",
            ),
            (
                "Execute staged binary",
                'cmd /c "%USERPROFILE%\\Downloads\\lab-test.exe"',
                "100204",
            ),
            (
                "Privilege discovery",
                "cmd /c whoami /priv",
                "",
            ),
            (
                "Connection discovery",
                "cmd /c netstat -ano",
                "",
            ),
        ],
    ),
]


def timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def execute(command):
    try:
        result = subprocess.run(
            [
                "ssh",
                "-i", str(KEY),
                "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=8",
                "-o", "StrictHostKeyChecking=yes",
                HOST,
                command,
            ],
            capture_output=True,
            text=True,
            timeout=50,
        )
        return result.returncode, result.stderr.strip()[-240:]

    except subprocess.TimeoutExpired:
        return -1, "SSH command timed out"


def build_schedule():
    # three incident windows, randomly assigned to the cases
    windows = [
        (6 * 60, 15 * 60),
        (23 * 60, 33 * 60),
        (41 * 60, 51 * 60),
    ]

    rng.shuffle(windows)
    events = []

    for (case_id, actions), (earliest, latest) in zip(CASES, windows):
        start = rng.uniform(earliest, latest - 90)
        offset = 0

        for label, command, rule in actions:
            events.append((
                start + offset,
                case_id,
                label,
                command,
                rule,
            ))

            # short delays within related sequences
            offset += rng.randint(12, 28)

    # 23 ordinary background activities across the hour
    for _ in range(23):
        label, command, rule = rng.choice(BENIGN)

        events.append((
            rng.uniform(20, DURATION - 90),
            "BACKGROUND",
            label,
            command,
            rule,
        ))

    return sorted(events, key=lambda event: event[0])


def main():
    BASE.mkdir(parents=True, exist_ok=True)

    log_path = BASE / "ground_truth.csv"

    if log_path.exists():
        print("Ground truth already exists. Refusing to overwrite.")
        return

    if not KEY.is_file():
        print("SSH key missing.")
        return

    schedule = build_schedule()

    print("=" * 50)
    print("PROJECT 2 — DAY 4 SOC SIMULATION")
    print("=" * 50)
    print(f"Scheduled activities: {len(schedule)}")
    print("Duration: approximately 60 minutes")
    print("Target: SOC-ENDPOINT-01")
    print("Ground truth: separate CSV")
    print()

    # check connectivity before starting
    code, error = execute("cmd /c hostname")

    if code != 0:
        print("SSH connectivity check failed:", error)
        return

    start = time.monotonic()

    with log_path.open("x", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "start_time",
            "end_time",
            "case_id",
            "activity",
            "command",
            "intended_rule",
            "exit_code",
            "execution_result",
            "error",
        ])

        for number, event in enumerate(schedule, 1):
            offset, case_id, label, command, rule = event

            wait = start + offset - time.monotonic()

            if wait > 0:
                time.sleep(wait)

            began = timestamp()
            code, error = execute(command)
            ended = timestamp()

            status = "SUCCESS" if code == 0 else "FAILED"

            writer.writerow([
                began,
                ended,
                case_id,
                label,
                command,
                rule,
                code,
                status,
                error,
            ])

            file.flush()

            print(
                f"[{number:02d}/{len(schedule)}] "
                f"Activity executed: {status}",
                flush=True,
            )

        remaining = start + DURATION - time.monotonic()

        if remaining > 0:
            time.sleep(remaining)

    print()
    print("Simulation complete.")
    print("Preserve ground_truth.csv until Day 6.")


if __name__ == "__main__":
    main()
