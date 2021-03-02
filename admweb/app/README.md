# sshログイン
ssh -i itonaga_pem.pem ec2-user@ec2-3-17-39-227.us-east-2.compute.amazonaws.com

# mysql ログイン
mysql -h simpway.ck7mjckhgvuz.us-east-2.rds.amazonaws.com -P 3306 -u admin -p

# pass
simpway1

# database周り
FLASK_APP=run.py flask shell

from application.database import db
db.create_all()

# 実行まわり
nohup python run.py &
https://qiita.com/alancodvo/items/15dc36d243e842448d33

https://qiita.com/hitochan777/items/941d4422c53978b275f8

sudo nohup python run.py > ~/output_log/out.log &

# migration
## migrateできないとき
https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date

https://qiita.com/kitarikes/items/9c5d6cbc557ed62bb512

FLASK_APP=run.py flask db migrate

FLASK_APP=run.py flask db upgrade

# ec2系
https://qiita.com/2355/items/7b4074afa5e0f16656f1