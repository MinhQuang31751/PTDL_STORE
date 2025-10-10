import pandas as pd
df = pd.read_csv('/content/convenience_store.csv')


import matplotlib.pyplot as plt
import pandas as pd

# Tính tổng số giao dịch
total_transactions = len(df)

# Đếm số lượng giao dịch của hội viên và không phải hội viên
member_counts = df['Member'].value_counts()

# Tính tỷ lệ phần trăm
member_percentage = (member_counts['Yes'] / total_transactions) * 100
non_member_percentage = (member_counts['No'] / total_transactions) * 100

# In ra số lượng và tỷ lệ phần trăm
print(f"Tổng số giao dịch: {total_transactions}")
print(f"Số lượng giao dịch của hội viên: {member_counts['Yes']} ({member_percentage:.2f}%)")
print(f"Số lượng giao dịch của không phải hội viên: {non_member_percentage:.2f}%)")

# Tạo dữ liệu cho biểu đồ tròn
labels = ['Hội viên', 'Không hội viên'] 
sizes = [member_percentage, non_member_percentage]
colors = ['#ff9999','#66b3ff'] # Màu sắc cho các phần
explode = (0.1, 0)  #

# Vẽ biểu đồ tròn
plt.figure(figsize=(8, 8))

plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', shadow=True, startangle=90)
plt.axis('equal')  
plt.title('Tỷ lệ giao dịch giữa hội viên và không phải hội viên') 
plt.show()





# Hội viên chi tiêu trung bình cao hơn bao nhiêu % so với khách thường
import matplotlib.pyplot as plt
import pandas as pd

# Tính tổng chi tiêu trung bình cho hội viên và không phải hội viên
average_spending = df.groupby('Member')['Total_Cost'].mean()

# Lấy giá trị chi tiêu trung bình
average_spending_member = average_spending['Yes']
average_spending_non_member = average_spending['No']

# Tính phần trăm chi tiêu trung bình cao hơn của hội viên so với không phải hội viên
percentage_higher = ((average_spending_member - average_spending_non_member) / average_spending_non_member) * 100

# In kết quả
print(f"Chi tiêu trung bình của hội viên: {average_spending_member:.2f}") # In với 2 chữ số thập phân
print(f"Chi tiêu trung bình của không phải hội viên: {average_spending_non_member:.2f}") # In với 2 chữ số thập phân
print(f"Hội viên chi tiêu trung bình cao hơn không hội viên: {percentage_higher:.2f}%") # In với 2 chữ số thập phân

# Tạo dữ liệu cho biểu đồ so sánh
labels = ['Không hội viên', 'Hội viên'] 
values = [average_spending_non_member, average_spending_member]

# Vẽ biểu đồ cột so sánh chi tiêu trung bình
plt.figure(figsize=(8, 6))
bars = plt.bar(labels, values, color=['#66b3ff', '#ff9999']) # Sử dụng màu khác nhau cho mỗi cột

# Thêm chú thích giá trị trung bình lên trên mỗi cột
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', va='bottom', ha='center') 

plt.title('So sánh chi tiêu trung bình giữa hội viên và không phải hội viên') 
plt.xlabel('Trạng thái thành viên') 
plt.ylabel('Chi tiêu trung bình') 
plt.show()







# Hội viên có xu hướng mua theo mùa / khung giờ nào nhiều nhất
import matplotlib.pyplot as plt
import pandas as pd

# Lọc dữ liệu chỉ cho hội viên
df_members = df[df['Member'] == 'Yes'].copy()

# Phân tích xu hướng theo mùa cho hội viên (theo 4 mùa)
df_members['Date'] = pd.to_datetime(df_members['Date'])
df_members['Month'] = df_members['Date'].dt.month

# Hàm phân loại tháng vào các mùa 
def categorize_season(month):
    if month in [3, 4, 5]:
        return 'Xuân'
    elif month in [6, 7, 8]:
        return 'Hạ'
    elif month in [9, 10, 11]:
        return 'Thu'
    else:
        return 'Đông'

df_members['Season'] = df_members['Month'].apply(categorize_season)

member_transactions_by_season = df_members['Season'].value_counts()

# Sắp xếp các mùa theo thứ tự để vẽ biểu đồ
season_order = ['Xuân', 'Hạ', 'Thu', 'Đông']
member_transactions_by_season = member_transactions_by_season.reindex(season_order)


# Vẽ biểu đồ xu hướng giao dịch theo mùa cho hội viên
plt.figure(figsize=(8, 6))
member_transactions_by_season.plot(kind='bar')
plt.title('Phân phối giao dịch theo mùa của hội viên') 
plt.xlabel('Mùa')
plt.ylabel('Số lượng giao dịch')
plt.xticks(rotation=0) 
plt.grid(axis='y') 
plt.show()

# Phân tích xu hướng theo giờ cho hội viên (Giữ phân tích theo giờ như cũ vì cũng được yêu cầu)
df_members['Hour'] = pd.to_datetime(df_members['TimeOfDay']).dt.hour
hourly_member_transactions = df_members['Hour'].value_counts().sort_index()

# Vẽ biểu đồ xu hướng giao dịch theo giờ cho hội viên
plt.figure(figsize=(12, 6))
plt.plot(hourly_member_transactions.index, hourly_member_transactions.values)
plt.title('Phân phối giao dịch theo giờ trong ngày của hội viên') 
plt.xlabel('Giờ trong ngày') 
plt.ylabel('Số lượng giao dịch') 
plt.xticks(range(24))
plt.grid(True)
plt.show()