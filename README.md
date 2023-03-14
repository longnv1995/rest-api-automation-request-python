# rest-api-automation-request-python
Rest API automation using pytest library in python

Following this guide to run rest api automation project

Pre-con:
1. Install Ghost api locally by following this guide: https://ghost.org/docs/
install/local/ (For docs: https://ghost.org/docs/)
2. Install python, I'm using python 3.10.5
3. Install packages to run automation script
Open powershell or any cli tool in your root project. 
Run 'python -m venv venv' to create venv (virtual environment) that no depends or affects by others env. Then, activate the env by running this cmd: .\venv\Scripts\activate
Finally, run this cmd: pip install -r requirements.txt --use-pep517

That's all for installation!

Now, move on to the setup & configuration session
Setup & Configuration:
1. After installation, start a ghost by running cmd: ghost start. 
To stop, run: ghost stop
2. Open admin dashboard at: http://localhost:2368/ghost/admin, sign up for new account, then login with that account
3. Go to: http://localhost:2368/ghost/#/settings/integrations
to create new custom integration. After create new one successfully, you will get Content API key, Admin API key, API URL. These values will be used to config before running automation script
4. Change ".env.example" file name to ".env", then copy those values from step #4 to corresspoding key:value pair in .env file

How to run tests
Go to root project
* To run all tests: pytest tests -v -s --alluredir=test_reports
* To run specific test suites, ex: pytest tests\admin\post -v -s --alluredir=test_reports

If you want to open allure reports, you need to install Java (at link: https://www.java.com/en/download/)

Open allure reports, run: allure serve test_reports, it will open a default browser automatically

BIG NOTE: There is one issue is that, if you run all testsuites at once, you will get 401 unauthorized due to expired token. Currently, expire token time is max 5 minutes. I can think of a few solutions to overcome 'expired time' but not good enough, I will resolve this issue soon.

Sources & References:
1. https://python.org/
2. https://docs.pytest.org/
3. https://www.linkedin.com/learning (python course on linkedin)
2. https://medium.com/
3. https://stackoverflow.com/
4. https://realpython.com/
5. https://testdriven.io
6. https://www.youtube.com/@coreyms
7. https://www.freecodecamp.org/
8. https://json-schema.org/
9. https://github.com/assertpy/assertpy
10. https://docs.qameta.io/allure-report/