IEWT(Interactive Embedded Web Terminal)
------------------------------------------

This release has minor bug fixes.

Installation:
----------------

- Python 3.8+
- Run ``pip install iewt`` to install iewt package. IEWT requires file creation permissions, hence run in a location with sufficient permissions.
- To run the application you need to have

  1. A remote machine with a Unix(Linux, MacOS etc.) OS.
  2. Tmux installed on the computer/VM.(Optional)
  3. SSH server running on the computer/VM.
  4. Network access to the SSH server.

- Once all the above steps are performed, run the command ``iewt``. Open a browser and goto     `localhost:8888/iewt <http://localhost:8888/iewt>`_
- Enter the SSH credentials in the form at the bottom of the screen. The terminal will appear soon after. To automatically execute commands, type the commands in the input field and click on the **send command** button. The command is executed in the terminal and after its completion its time will appear in the readonly input field below the command status button. The command status turns green on success and red on failure.

Integration Tests and Load Test:
-----------------------------------------

- pip install -r requirements.txt
- run each test individually.
- change remote server credentials as per your requirements.
- provide correct input paths where required.

Unit Tests:
-------------------

- pip install flake8 mock
- python -m unittest discover tests

Code Coverage:
-------------------

- coverage run -m unittest discover tests
- coverage report -m > coverage_report.txt

Docker Image:
------------------

- docker compose up

Legacy files:
---------------------

- dbservice-skeleton.py: part of release 1.2.0
- setup.sql: part of releases 1.0.0 and 1.1.0
