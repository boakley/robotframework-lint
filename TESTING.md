## How to run smoke tests:

From the root of the repository, issue the following command:

    python -m robot.run -A tests/conf/smoke.args tests
    
## How to run the full suite:

    python -m robot.run -A tests/conf/default.args tests

## Test results

The above will put the results in tests/results (eg: tests/results/log.html, etc.)


