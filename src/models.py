import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute
    id = Column(Integer, primary_key=True)
    email = Column (String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    lastname = Column (String(50), nullable=False)
  

    post = relationship("Post")

class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Post (Base):
  __tablename__ = 'post'
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
  image_url = Column(String(255), nullable=False)
  caption = Column(String(500))
  location = Column(String(100))

  user = relationship('User', back_populates='posts')
  comments = relationship('Comment', back_populates='post', cascade='all, delete')
  likes = relationship('Like', back_populates='post', cascade='all, delete')
  
  class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(String(500), nullable=False)
    user = relationship ("User")
    post = relationship ("Post", back_populates="comments")
    
    class Like(Base):
        
        __tablename__ = 'like'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    

    user = relationship ("User")
    post = relationship ("Post", back_populates= "likes")

    def to_dict(self):
        return { 
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
        

        }
    

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
