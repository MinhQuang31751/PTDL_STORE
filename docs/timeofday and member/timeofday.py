import pandas as pd
df = pd.read_csv('/content/convenience_store.csv')


import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd


df['TimeOfDay'] = pd.to_datetime(df['TimeOfDay'])
df['Hour'] = df['TimeOfDay'].dt.hour
hourly_transactions = df['Hour'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
plt.plot(hourly_transactions.index, hourly_transactions.values)
plt.title('Phân phối giao dịch theo giờ trong ngày') 
plt.xlabel('Giờ trong ngày') 
plt.ylabel('Số lượng giao dịch') 
plt.xticks(hourly_transactions.index)
plt.grid(True)
plt.show()






#Khung giờ vàng 
import matplotlib.pyplot as plt
import pandas as pd


timeofday_category_counts = df['TimeOfDay_Category'].value_counts()
golden_hour_category = timeofday_category_counts.idxmax()


plt.figure(figsize=(10, 6))
bars = plt.bar(timeofday_category_counts.index, timeofday_category_counts.values)

for bar in bars:
    if bar.get_height() == timeofday_category_counts.max():
        bar.set_color('orange')
   
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center') 


plt.title('Phân phối giao dịch theo khoảng thời gian trong ngày') 
plt.xlabel('Khoảng thời gian trong ngày') 
plt.ylabel('Số lượng giao dịch') 
plt.show()




#Phân phối giao dịch theo giờ trong ngày theo nhóm tuổi
import matplotlib.pyplot as plt
import pandas as pd


def categorize_age_group(category):
   
    if category in ['Teenager (13-19)', 'Young Adult (20-29)']:
        return 'Người trẻ'
    else:
        return 'Người già'

df['Age_Group'] = df['Customer_Category'].apply(categorize_age_group)


df['Hour'] = pd.to_datetime(df['TimeOfDay']).dt.hour


hourly_transactions_young = df[df['Age_Group'] == 'Người trẻ']['Hour'].value_counts().sort_index()
hourly_transactions_old = df[df['Age_Group'] == 'Người già']['Hour'].value_counts().sort_index()


plt.figure(figsize=(12, 6))
plt.plot(hourly_transactions_young.index, hourly_transactions_young.values, label='Người trẻ') 
plt.plot(hourly_transactions_old.index, hourly_transactions_old.values, label='Người già') 

plt.title('Phân phối giao dịch theo giờ trong ngày theo nhóm tuổi') 
plt.xlabel('Giờ trong ngày') 
plt.ylabel('Số lượng giao dịch') 
plt.xticks(range(24))
plt.grid(True)
plt.legend() 
plt.show()