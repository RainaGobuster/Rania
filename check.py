from datetime import datetime
import time,os,requests

reference_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
token=""
# Function to check if a given date string is after or before the reference date
def check_date(input_date_str):
    # Convert the input date string to a datetime object
    try:
        input_date = datetime.strptime(input_date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."
    
    # Compare the input date with the reference date
    if input_date > reference_date:
        return False
    if input_date < reference_date:
        return True
    return False



while True:
 x=open("list_date.txt","r").read().split("\n")
 for a in x:
  if a=="":
     pass
  else:
   b=a.split(":::")
   if check_date(b[3]):
      os.system(f"screen -X -S {b[0]} quit")
      os.system(f"rm -rf {b[0]}")
      os.system(f'sudo su - postgres -c "dropdb {b[0]}"')
      text=open("list_date.txt","r").read().replace(f"{a}\n","")
      
      open("list_date.txt","w").write(text)
      url = f'https://api.telegram.org/bot{token}/sendMessage'
      payload = {
      'chat_id': 1938276557,
      'text': f'''المستخدم:-{b[0]}
تاريخ بدء الاشتراك:-{b[2]}
تاريخ الانتهاء:-{b[3]}
نوع الاشتراك:-{b[1]}
انتهى الاشتراك لديه❌'''
      }
      requests.post(url, data=payload)
 time.sleep(3600)