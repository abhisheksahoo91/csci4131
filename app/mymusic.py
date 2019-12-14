import requests
from app import logging
from app.dbclass import Genre

class MyMusic:
    # URL
    BASE_URL = 'http://api.deezer.com/'

    # This section implements search functionalities
    def search_entity(self, name, value):
        QUERY_URL = 'search/{}?q={}'.format(name, value)
        url = self.BASE_URL + QUERY_URL
        resp = requests.get(url)
        json = resp.json()
        data = json.get('data')
        '''
        data = []
        if name == 'album':
            for i_data in json_data:
                info = {
                    "id": i_data.get('id'),
                    "name": i_data.get('title'),
                    "image": i_data.get('cover_big'),
                }
                data.append(info)
        elif name == 'artist':
            for i_data in json_data:
                info = {
                    "id": i_data.get('id'),
                    "name": i_data.get('name'),
                    "image": i_data.get('picture_big')
                }
                data.append(info)
        elif name == 'playlist':
            for i_data in json_data:
                info = {
                    "id": i_data.get('id'),
                    "name": i_data.get('title'),
                    "image": i_data.get('picture_big')
                }
                data.append(info)
        elif name == 'track':
            for i_data in json_data:
                info = {
                    "id": i_data.get('id'),
                    "name": i_data.get('title'),
                    "image": i_data.get('album').get('cover_big'),
                }
                data.append(info)
        data = {
            "name": name, "data": data
        }
        
        # Format the data first
        if json_data != None or json_data!= '':
            data = {
                "type": name,
                "data": json_data
            }
        '''
        #print(data)
        return data
        
    def group_album_by_genre(self, data):
        data = sorted(data, key=lambda i: i['genre_id'])
        data_list = []
        data_sub_list = []
        for (i,d) in enumerate(data):
            if i != 0:
                if d.get('genre_id') != data[i-1].get('genre_id'):
                    cur_genre = Genre.query.get(data[i-1].get('genre_id'))
                    if cur_genre == None:
                        genre_name = 'Others'
                    else:
                        genre_name = cur_genre.name
                    instance = {
                        "genre": genre_name,
                        "data": data_sub_list,
                        "list_length": len(data_sub_list)
                    }
                    data_list.append(instance)
                    data_sub_list = []
                    data_sub_list.append(d)
                else:
                    data_sub_list.append(d)
            else:
                data_sub_list.append(d)
            if i == len(data)-1:
                cur_genre = Genre.query.get(d.get('genre_id'))
                if cur_genre == None:
                    genre_name = 'Others'
                else:
                    genre_name = cur_genre.name
                instance = {
                    "genre": genre_name,
                    "data": data_sub_list,
                    "list_length": len(data_sub_list)
                }
                data_list.append(instance)
        data_list = sorted(data_list, key=lambda i: i['list_length'])
        data_list = data_list[::-1]
        [data.pop('list_length', None) for data in data_list]
        '''
        for d in data_list:
            print(d.get('genre'))
            for di in d.get('data'):
                print (di.get('genre_id'))
            print('End')
        '''
        return data_list

    def get_entity_byId(self, search_type, id):
        print(search_type)
        QUERY_URL = '{}/{}'.format(search_type, id)
        url = self.BASE_URL + QUERY_URL
        resp = requests.get(url)
        data = resp.json()
        if search_type != 'track':
            url = data.get('tracklist')
            resp = requests.get(url)
            track_data = resp.json().get('data')
            data["track_data"] = track_data
        print(data)
        return data