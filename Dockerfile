FROM selenium/standalone-chrome:4.7.2-20221219

RUN sudo apt-get update && sudo apt-get install -y python3-pip

RUN pip3 install selenium discord_webhook

COPY . /whatsbot

RUN sudo chown -R 1200:1201 /whatsbot

RUN sudo mv /whatsbot/whatsbot.conf /etc/supervisor/conf.d/whatsbot.conf

RUN sudo chown root:root /etc/supervisor/conf.d/whatsbot.conf
