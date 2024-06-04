import time
import csv
import api_parsing as api
import find_all_members as find


with open("GroupsOK.csv", newline='', encoding='utf-8') as Groups:
   reader = csv.reader(Groups, delimiter=';')
   community_ids = []
   for row in reader:
      community_ids.append(row[0])
   print("Получили данные о всех группах, приступаю к поиску")


users_file = 'Users1.csv'


with open(users_file, mode='a', newline='', encoding='utf-8') as Users:
   writer_Users = csv.writer(Users)
   writer_Users.writerow(['community_id', 'API user id', 'Age', 'Gender', 'City', 'Country', 'Last online'])
   count = len(community_ids)
   for i in range(0, 10):
      group_id = community_ids[i]
      href = "https://ok.ru/group/" + community_ids[i]
      users = find.get_members(group_id)
      count_users = 0
      if users != 0:
         for user in users:
            member = api.members_facts(user['userId'])
            try:
               age = member[0]['age']
            except:
               age = None
            try:
               gender = member[0]['gender']
            except:
               gender = None
            try:
               city = member[0]['location']['city']
            except:
               city = None
            try:
               country = member[0]['location']['country']
            except:
               country = None
            try:
               last_online = member[0]['last_online']
            except:
               last_online = None
            writer_Users.writerow([community_ids[i], user['userId'], age, gender, city, country, last_online])
            if (count_users * 10) % api.count_members(str(community_ids[i])) == 0:
               print(f"Обработано {(api.count_members(str(community_ids[i])) * 10) % api.count_members(str(community_ids[i]))}"
                     f"% юзеров")
            count_users += 1
            print(count_users)
      count += 1
      print(f'Добавлено в таблицу {count} групп.')
   print(f"Завершено успешно, таблица groups была создана. Обработано {count} групп.")

time.sleep(2)
