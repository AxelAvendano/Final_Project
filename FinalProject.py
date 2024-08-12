#Axel Avendano 
# PSID 2023639


#The following code imports necessary modules
from datetime import datetime
import csv

import csv
import datetime


#The following variables are initialized
sorted_items = []
price_item = []
price_id = {}
date_item_list = []
date_id = {}
all_items = []


#takes file names from the user and reads the files 
#also stores each file's data in separate lists
for i in range(3):
    csv_file = input("Enter the file name: ")

    with open(csv_file, 'r') as readable_csv_file:
        readable_csv_file = csv.reader(readable_csv_file, delimiter=',')
        if i == 0:
            for line in readable_csv_file:
                all_items.append(line)

        elif i == 1:
            for line in readable_csv_file:
                price_item.append(line)

        elif i == 2:
            for line in readable_csv_file:
                date_item_list.append(line)


#sorts the list of items by manufacturer name and returns the sorted list
def sorting():
    manu_list = []
    for manu_item in range(len(all_items)):
        manu_list.append(all_items[manu_item][1])
        manu_list = list(set(manu_list))

    for manu in range(len(manu_list)):
        for first_item in range(len(all_items)):
            if all_items[first_item][1] == manu_list[manu]:
                sorted_items.append(all_items[first_item])
    return sorted_items

'''The sorting function is used to sort the 
items in the inventory by manufacturer.'''


#creates a dictionary of prices with the item ID as the key and price as the value
def creating_PriceDirectory():
    for item in range(len(price_item)):
        first = price_item[item][0]
        second = price_item[item][1]
        price_id[first] = second
    return price_id




#The following function creates a dictionary of service dates with the item ID as the key and date as the value
def creating_ListOfServiceDates():
    for date_item in range(len(date_item_list)):
        item_id = date_item_list[date_item][0]
        date = date_item_list[date_item][1]
        date_id[item_id] = date
    return date_id




#creates a CSV file named FullInventory and writes the entire inventory to it
def creating_FullInventory():
    f = open("FullInventory.csv", "w")
    fullinventory = csv.writer(f)
    for line_item in sorted_items:
        id = line_item[0]
        new_list = line_item[0], line_item[1], line_item[2], price_id[id], date_id[id], line_item[3]
        fullinventory.writerow(new_list)




#creates separate CSV files for each item type and writes the corresponding items to them
def creating_DifferentList():
    list_of_item_types = list(set(item[2] for item in sorted_items))
    item_lists = []
    for item_type in list_of_item_types:
        items_of_type = [(item[0], item[1], price_id[item[0]], date_id[item[0]], item[3])
                         for item in sorted_items if item[2] == item_type]
        items_of_type.sort()
        item_lists.append(items_of_type)


    for item_type, items_of_type in zip(list_of_item_types, item_lists):
        with open(f"{item_type}.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(items_of_type)



# creates a CSV file named PastServiceDateInventory and writes items whose service date has expired to it
def creating_ExpiredInventory():
    expired_items = []
    with open('PastServiceDateInventory.csv', 'w', newline='') as n:
        writer = csv.writer(n)
        writer.writerow(['Item ID', 'Manufacturer Name', 'Item Type', 'Item Price', 'Date Time', 'Item Damage'])
        for item in sorted_items:
            item_id, manufacturer_name, item_type, item_damage = item[0], item[1], item[2], item[3]
            item_price = price_id[item_id]
            date_time = date_id[item_id]
            expiration_date = datetime.datetime.strptime(date_time, "%m/%d/%Y").date()
            today = datetime.datetime.now().date()
            if expiration_date < today:
                expired_items.append((item_id, manufacturer_name, item_type, item_price, date_time, item_damage))
                writer.writerow((item_id, manufacturer_name, item_type, item_price, date_time, item_damage))
    return [item[4] for item in expired_items]


new_list_of_dates = []
list_of_dates = creating_ExpiredInventory()
datetime_dates = [datetime.strptime(date, "%m/%d/%Y") for date in list_of_dates]
datetime_dates.sort()
sorted_dates = [datetime.strftime(sorted_date, "%m/%d/%Y") for sorted_date in datetime_dates]



def ItemDamage():
    damaged_items = [item for item in sorted_items if item[3] == "damaged"]
    prices = sorted([int(price_id[item[0]]) for item in damaged_items])

    with open("DamagedInventory.csv", "w") as f:
        writer = csv.writer(f)
        for price in prices:
            for item in sorted_items:
                if item[0] in price_id and int(price_id[item[0]]) == price:
                    add_line = item[0], item[1], item[2], price_id[item[0]], date_id[item[0]], item[3]
                    writer.writerow(add_line)

priceDictionary = creating_PriceDirectory()
serviceDictionary = creating_ListOfServiceDates()



sorting()
creating_PriceDirectory()
creating_ListOfServiceDates()
creating_FullInventory()
creating_DifferentList()
creating_ExpiredInventory()
ItemDamage()