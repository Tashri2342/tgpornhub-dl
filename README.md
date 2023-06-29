### Environment

In order to deploy your own bot, please fill-up the provided vars correctly in pornhub/config.py.

### Deploy on Heroku (PAID)

1. Fork this repo
2. Visit heroku.com
3. Create new App -> Enter the App Name -> Choose App Country
4. Click on Deploy Tab
5. Click on GitHub Tab -> Connect the App to Your GitHub account
6. Enter the Repo name You've forked before -> Tap Connect
7. Click on Deploy Branch button
8. After build done -> Click on Resources Tab -> Switch Toggle On

### Deploy on VPS

```console
root@ubuntu~ $ git clone https://github.com/Tashri2342/tgpornhub-dl
root@ubuntu~ $ cd tgpornhub-dl
root@ubuntu~ $ pip3 install -Ur requirements.txt
root@ubuntu~ $ python3 -m pornhub
```

### Others

This repo has made with an function that let you generate statistic (the generated stats is counted from the local database, remember every time the server restart, all data generated in database will reset to zero!), broadcasting message, search video with inline mode and force user to join into your channel. So make sure that you've set an group for receive the log report given by your bot also the channel of the force-subscribe feature.

### Credit

This repo is distributed under the MIT License 2022 By [@Tashri2342](https://github.com/Tashri2342)
