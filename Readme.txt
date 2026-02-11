readme.txt
.

The task is to implement the API scheduler using multithreading.
API scheduler will hit the URL(ifconfig.co) at the given timestamps and save the results in a notebook called log where it will show if the API hit was successful or unsuccessful.
The code is written in a modular structure with separate configuration and logic files.
Unit and integration tests are included to verify functionality.

To carry out the task, we need to:
1.Group all the timestamps by seconds for simultaneous(concurrent) execution.
2.Validate and Parse timestamps.
3.Respond politely to network problems.
4.Include 6 passing Unit tests.
5.Clean CLI input.
6.Log actual execution timestamps in the exact format "2025-12-03 18:32:31: Successfully called API at ifconfig.co".

Logs are stored automatically after execution.

This project demonstrates multithreading, logging, API handling, and clean code practices.
