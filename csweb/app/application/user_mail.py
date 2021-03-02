import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import datetime

def send_reserved(
  user_name,
  user_mail,
  user_take_date,
  user_return_date,
  start_spot,
  goal_spot,
  ):
  user_return_date = "{0:%Y年%m月%d日%H時%M分}".format(user_return_date)
  user_take_date = "{0:%Y年%m月%d日%H時%M分}".format(user_take_date)
  mail_text = \
    user_name + '様\n'\
    + 'この度はSimpwayをご利用頂き誠にありがとうございます。\n以下の通り予約が完了致しましたのでご確認ください。\n\n'\
    + '■予約内容\n'\
    + '受け取り日時：' + user_take_date + '\n'\
    + '返却日時：' + user_return_date + '\n'\
    + '出発店舗：' + start_spot + '\n'\
    + '到着店舗：' + goal_spot + '\n'\
    + '■注意事項\n'\
    + '・出発店舗と到着店舗は変更ができません\n'\
    + '・出発予定時間、到着予定時間の遅れがございましたらそれぞれの店舗へご連絡お願い致します。\n\n'\
    + '■キャンセルポリシー\n'\
    + 'なにか追記する'
  message = Mail(
        from_email='noreply@simpway.to',
        to_emails=user_mail,
        subject='Simpway予約確認メール（' + user_return_date + '予約分）',
        plain_text_content=mail_text
        )
        
  sg = SendGridAPIClient('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')
  response = sg.send(message)

def test():
  config = Dotenv('../sendgrid.env')
  apikey = config['SENDGRID_API_KEY']
  print(apikey)
  print('ここだよおおおおおおおおおおおお')