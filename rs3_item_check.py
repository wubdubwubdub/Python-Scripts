import requests
import json
import matplotlib.pyplot as plt

#define API call-------------------------------------------

#input collection and modification
item = input('Type in item to look up. Capitalize the first letter: ')
print('Compiling data for',item)
item_selection = item.replace(" ", "%20")
#-----------------------------------------------------------------------

def graph_data(item_selection):
    #defining where to send request
    url = 'https://api.weirdgloop.org/exchange/history/rs/last90d?name=' + item_selection

    #sends get request and stores returned data in response
    res = requests.get(url)
    #Lets us know if the call was successful or not
    if res.status_code == 200:
        print('Success!')
    else:
        print('Failed to retrieve data: ', res.status_code)

    #transform list into json
    data = json.loads(res.text)

    #data structure
    #{'id': '556','price': 27,'volume': 1111111,'timestamp': 1452525252525},

    #if length of object is needed
    #data_length = len(data['item'])

    price = []
    volume = []
    timestamp = []
    i = 0
    max_price = 0
    min_price = data[item][0].get('price')


    #loop to populate price and timestamp
    while i < 14:
        price.append(data[item][i].get('price'))
        if max_price < data[item][i].get('price'):
            max_price = data[item][i].get('price')
        if min_price > data[item][i].get('price'):
            min_price = data[item][i].get('price')
        timestamp.append(i+1)
        i += 1

    #print out of useful data----------------------------------------
    #min man
    print('Bi-weekly min = ' + str(min_price) + ' max = ' + str(max_price))
    #total profit after tax
    profit = (max_price - min_price)*.98
    print('Total profit per unit = ' + str(profit) + 'gp')
    #-----------------------------------------------------------------

    #form plot
    plt.plot(timestamp,price)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()


graph_data(item_selection)
