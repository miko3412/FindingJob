# FindingJob
Project which helps you find jobs on some sides like "https://pracuj.pl/", "https://nofluffjobs.com/".

App is very simple. You mast have both scripts (gui.py + scrap.py) un the same folder. Scripts are using selenium and BeautifulSoup, which you must download by pip.

You can see how to install them on:
https://pypi.org/project/beautifulsoup4/ ,
https://pypi.org/project/selenium/


App is easy to use, because you give in gui.py necessary data you want to have in your job offer and then it searches for results (currently only from "https://pracuj.pl/").
When it ends searching, you see a list of job offers. Choose one and it gives you link to this offer for more information and apply.
