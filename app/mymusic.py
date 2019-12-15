import requests
from app import logging, db
from app.dbclass import Genre, Favorite
from flask_login import current_user

class MyMusic:
    # URL
    BASE_URL = 'http://api.deezer.com/'

    def check_favorite(self, entity_type, entity_id):
        fav = self.get_favorite(entity_type, entity_id)
        if fav:
            return True
        else:
            return False
    def get_favorite(self, entity_type, entity_id):
        return Favorite.query.filter_by(user_id=current_user.id, entity_type=entity_type, entity_id=entity_id).first()
    def add_favorite(self, entity_type, entity_id):
        fav = Favorite(user_id=current_user.id, entity_type=entity_type, entity_id=entity_id)
        db.session.add(fav)
        db.session.commit()
    def delete_favorite(self, fav):
        db.session.delete(fav)
        db.session.commit()
    def toggle_favorite(self, entity_type, entity_id):
        fav = self.get_favorite(entity_type, entity_id)
        if fav:
            self.delete_favorite(fav)
        else:
            self.add_favorite(entity_type, entity_id)

    def search_entity(self, name, value):
        QUERY_URL = 'search/{}?q={}'.format(name, value)
        url = self.BASE_URL + QUERY_URL
        resp = requests.get(url)
        json = resp.json()
        data = json.get('data')
        for d in data:
            d['favorite'] = self.check_favorite(d.get('type'), d.get('id'))
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
        return data_list

    def get_entity_byId(self, search_type, id):
        print(search_type)
        #print(id)
        QUERY_URL = '{}/{}'.format(search_type, id)
        url = self.BASE_URL + QUERY_URL
        resp = requests.get(url)
        data = resp.json()
        data['favorite'] = self.check_favorite(data.get('type'), data.get('id'))
        if search_type == 'artist':
            url = data.get('tracklist')
            resp = requests.get(url)
            track_data = resp.json().get('data')
            data["track_data"] = track_data
        #print(data)
        return data