import telebot
from bs4 import BeautifulSoup
import requests
from flask import Flask, request
import os



TOKEN =  "{your chat bot api token from botfather}"
ktu_link = "https://www.ktu.edu.in/"
welcome_msg  = "Hai ,I am here to get you the latest announcements by KTU. \nAll the information I pass to you is from the offical KTU website\n{}\n click /news to get the current news in KTU website. You can also type in 'news' or '/news' to get the News at any time\nOr  click /help\n If you want to contact my owner @mydevs or click /master".format(ktu_link)
help_msg = "Just send me a '/news' command to get the latest announcements published on the KTU website.\nIf you want to contact my master click /master.\nNOTE: since I fetch information from the website it takes a few moments.Kindly wait and don't reply until I serve ypu with answer of your last command thank you.\n /news"
contact_msg = "Hai, to contact my master \n\nAt Instagram https://instagram.com/yadhuphilip \n\nAt GitHub https://github.com/yadhuphilip \n\nAt telegram  t.me/mydevs \n \n/news"


bot = telebot.TeleBot(token = TOKEN)
server = Flask(__name__)
@bot.message_handler(commands=['/start','start','Start','START','START'])
def greetings(message):
    cli = message.chat.id
    bot.send_message(cli,welcome_msg)

@bot.message_handler(commands=['/help','HELP','/HELP','/Help','help','Help'])
def helpmsg(message):
     cli = message.chat.id
     bot.send_message(cli,help_msg)


@bot.message_handler(commands=['/master','master','Master','MASTER'])
def ma_details(message):
    cli = message.chat.id
    bot.send_message(cli,contact_msg)


@bot.message_handler(commands=['NEWS','news','News','/NEWS','/news','/News'])
def news(message):
    cli = message.chat.id

    ktu_web_req = requests.get(ktu_link)
    news_ret=""
    a=0
    if ktu_web_req:
        ktu_script = BeautifulSoup(ktu_web_req.content,'html.parser')
        ls = ktu_script.find_all(class_='annuncement')
        news_board = ls[0]
        news = news_board.find_all('li')
        for each_news in news:
            a=a+1
            each_date_wrapped = each_news.find('label')
            main_content_wrapped = each_news.find('a')
            main_content = main_content_wrapped.get_text()
            each_date = each_date_wrapped.get_text()
            main_content_link = ktu_link+main_content_wrapped.get('href')
            if "00:00:00 IST" in each_date:
                each_date = each_date.replace("00:00:00 IST","")
                each_date = each_date[4:]
            news_ret = news_ret + "{}. {}  issued on- {}  {}\n\n".format(a,main_content,each_date,main_content_link)
    else:
        news_ret = "Sorry, I can,t connect to {}  try again after some time.\nNOTE: since I fetch information from the website it takes a few moments.Kindly wait and don't reply until I serve ypu with answer of your last command thank you\n /news".format(ktu_link)
    
    news_message = news_ret
    bot.send_message(cli,news_message)




@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url={hosted url[heroku]} + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', {port number})))