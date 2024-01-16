import requests
from pprint import pprint as pp

class NoteAPIException(Exception):
    ...

class Note:
    
    def __init__(self, data_note: dict):
        self.__data_note = data_note
    
    @property
    def id(self): return self.__data_note['id']
    
    @property
    def title(self): return self.__data_note['title']

    @property
    def body(self): return self.__data_note['body']
    
    @property
    def created(self): return self.__data_note['created']
    
    @property
    def updated(self): return self.__data_note['updateds']            


class NoteAPI:
    
    def __init__(self, token: str):
        access = requests.get(f'http://127.0.0.1:8000/api/{token}/')

        if access.status_code == 200:
            self.token = token
            self.url = f'http://127.0.0.1:8000/api/{self.token}/'
            
        else:
            self = None
            raise Exception('Неверный Токен')
    
    def get_notes(self):
        notes = requests.get(self.url + 'getNotes').json()
        return notes
    
    def get_note(self, id = None, title: str = None, obj = None):
        
        if id:
            note = requests.get(self.url + f'note?id={str(id)}').json()
        
        elif title:
            note = requests.get(self.url + f'note?title={title}').json()
        
        else:
            raise NoteAPIException('Укажите переменую id или title')
        
        if obj:
            return Note(note)
            
        return note
    
    def create_note(self, title: str, body: str):
        note = requests.post(self.url + f'note?title={title}&body={body}')
        return note
    
    def delete_note(self, id):
        note = requests.delete(self.url + f'note?id={id}')
    
    def edit_note(self, id, title = None, body = None):
        
        if title and body:
            note = requests.put(self.url + f'note?id={id}&title={title}&body={body}')
        
        elif title:
            note = requests.put(self.url + f'note?id={id}&title={title}')
        
        elif body:
            note = requests.put(self.url + f'note?id={id}?body={body}')
        
        else:
            raise NoteAPIException('Передайте переменную/переменные в метод edit_note')
    
    def docs(self):
        return 'http://127.0.0.1:8000/home/api'
        

notes = NoteAPI('VBLh4PqZWhGcaYAh8XpKWcDbAdHJdtiHJPJd2Beg85CKVz1WJP6vw0OTVeyiDLunsPQOqbLs3QNYLd37lNpe5MxhQnGGZtBM7ZnX')
note = notes.get_note(id = 1, obj = True)
print(note.title)


        