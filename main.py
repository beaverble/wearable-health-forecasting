import schedule
import time
import predict_health

def main_predict():
   predict_health.main()

schedule.every().hour.at(":00").do(main_predict)
main_predict()

while True:
   try:
      schedule.run_pending()
   except:
      print(time.strftime('%Y.%m.%d - %H:%M:%S') + "   error")
      time.sleep(60)
      print(time.strftime('%Y.%m.%d - %H:%M:%S') + "   restart")
      schedule.every().hour.at(":00").do(main_predict)
      schedule.run_pending()
