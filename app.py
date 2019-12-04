
# Imports
from flask import Flask
from pathlib import Path
import pandas
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy.orm import mapper, sessionmaker, Session
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import os
from flask_graphql import GraphQLView
import sqlite3
from sqlalchemy.ext.automap import automap_base

# app initialization
app = Flask(__name__)
app.debug = True

# Configs
Conn = 'sqlite:///C:/Users/ariel/flask-graphql-project/demo.db' 
entries = pandas.read_csv(r'C:/Users/ariel/Desktop/dashboard_demo/dashboard_demo/app/backend/model/data/CL_data_190116.csv')
entries.columns = entries.columns.str.replace(' ', '_')
entries.columns = entries.columns.str.replace('[^_A-Za-z0-9]+', '')
entries = entries.drop_duplicates(subset="Timestamp")
app.config['SQLALCHEMY_DATABASE_URI'] = Conn
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db = SQLAlchemy(app)

# Models9
class Entry(db.Model):
    __tablename__ = 'Entries'
    for i in entries.columns:
        if i == 'Timestamp':
            Timestamp = db.Column(db.String, primary_key=True)
        else:
            locals()[i] = db.Column(db.String(100))

class Label(db.Model):
    __tablename__ = 'Labels'
    Index = db.Column(db.Integer)
    Timestamp = db.Column(db.String, db.ForeignKey('Entries.Timestamp'), primary_key=True)
    Chiller_ID = db.Column(db.String(100))
    Label_Type = db.Column(db.Integer)        
    Status = db.Column(db.String(100))

# Schema Objects
class EntryObject(SQLAlchemyObjectType):
    class Meta:
        model = Entry
        interfaces = (graphene.relay.Node, )

class LabelObject(SQLAlchemyObjectType):
    class Meta:
        model = Label
        interfaces = (graphene.relay.Node, )

# CREATE
class CreateEntry(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String(required=True)
    ok = graphene.Boolean()
    entry = graphene.Field(EntryObject)
  
    def mutate(self, info, **args):
        entry = Entry(Timestamp = args.get('timestamp'))
        db.session.add(entry)
        db.session.commit()
        ok = True
        return CreateEntry(entry=entry, ok=ok)

# READ
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_entries = SQLAlchemyConnectionField(EntryObject)
    all_labels = SQLAlchemyConnectionField(LabelObject)

# UPDATE
class ChangeProperty(graphene.Mutation):
    class Arguments:
        index = graphene.String(required=True)
        label = graphene.String()
    ok = graphene.Boolean()
    labelentry = graphene.Field(LabelObject)

    def mutate(self, info, **args):
        query = LabelObject.get_query(info)
        index = args.get('index')
        label = args.get('label')
        labelentry = query.filter(Label.Index == index).first()
        labelentry.Label_Type = label
        db.session.commit()
        ok = True
        return ChangeProperty(labelentry = labelentry, ok = ok)

class Mutation(graphene.ObjectType):
    create_entry = CreateEntry.Field()
    change_property = ChangeProperty.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types = [EntryObject])

# Routes
@app.route('/')
def index():
    return '<p> Hello World</p>'

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run()

# SAMPLE QUERIES

# CREATE QUERY
# mutation {
#   createEntry(timestamp:"2019-01-09 23:55:00 SGT") {
#     entry {
#       Timestamp,
#     }
#   }
# }

# READ QUERY
# {
#   allEntries {
#     edges {
#       node {
#         Timestamp,
#         CH1Efficiency
#       }
#     }
#   }
# 

# UPDATE (property with timestamp)
# mutation {
#   changeProperty(index: "1", label: "2") {
#     labelentry {
#       Index
#       Timestamp
#       LabelType
#     }
#   }
# }
