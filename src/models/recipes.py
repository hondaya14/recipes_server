
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime


Base = declarative_base()


class RecipesModel(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    making_time = Column(String)
    serves = Column(String)
    ingredients = Column(String)
    cost = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def to_dict(self):
        data_dict = dict()
        data_dict['id'] = self.id
        data_dict['title'] = self.title
        data_dict['making_time'] = self.making_time
        data_dict['serves'] = self.serves
        data_dict['ingredients'] = self.ingredients
        data_dict['cost'] = self.cost
        data_dict['created_at'] = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        data_dict['updated_at'] = self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        return data_dict

    def from_json(self, json):
        self.title = json['title']
        self.making_time = json['making_time']
        self.serves = json['serves']
        self.ingredients = json['ingredients']
        self.cost = json['cost']
        return self

    def set_created_timestamp(self):
        created_time = datetime.datetime.now()
        self.created_at = created_time.strftime('%Y-%m-%d %H:%M:%S')

    def set_updated_timestamp(self):
        updated_time = datetime.datetime.now()
        self.updated_at = updated_time.strftime('%Y-%m-%d %H:%M:%S')

    def print_all_item(self):
        print(f'id: {self.id}, '
              f'title: {self.title}, '
              f'making_time: {self.making_time}, '
              f'serves: {self.serves}, '
              f'ingredients: {self.ingredients}, '
              f'cost: {self.cost} ')
