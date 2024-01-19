# pip install pyyaml requests
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import requests

from nwebclient import util
from nwebclient import base as b


def openapitype_to_sql(typename):
    res = 'VARCHAR(255)'
    # integer string
    if typename == 'integer':
        res = 'NUMBER(9)'
    return res

def openapitype_to_java(typename):
    res = 'String'
    # integer string
    if typename == 'integer':
        res = 'int'
    return res

def openapi_to_sql_col_name(name):
    return name

class OpenApi(b.Base)
   classes = []
   def __init__(self, yaml_text):
        self.data = yaml.load(text, Loader=Loader)
        objs = data['components']['schemas']
        for name in objs.keys():
            self.classes.append(ObjectDef(name, objs[name]))
    def to_mermaid(self, for_gitlab=False):
        res = ''
        if for_gitlab:
            res += '```mermaid\n'
        res +=  '---\n'
        res += 'title: Klassendiagramm\n'
        res += '---\n'
        res += 'classDiagram\n'
        for obj in self.classes:
            res += obj.to_mermaid()
        if for_gitlab:
            res += '```\n'
        return res
    def to_sql(self):
        res = ''
        for obj in self.classes:
            res += obj.to_sql() + '\n'
        return res


class ObjectDef(b.Base):

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def sql_col_modifier(self, name, data, i):
        if name == 'id' or i == 0:
            return ' PRIMARY KEY'
        return ''

    def sql_col_def(self):
        cols = []
        i = 0
        for name in self.data['properties'].keys():
            sql_type = openapitype_to_sql(self.data['properties'][name]['type'])
            sql_modifier = self.sql_col_modifier(name, self.data['properties'][name], i)
            cols.append('   ' + openapi_to_sql_col_name(name) + ' ' + sql_type + sql_modifier)
            i += 1
        return ', \n'.join(cols)

    def sql_col_names(self):
        cols = []
        for name in self.data['properties'].keys():
            cols.append(openapi_to_sql_col_name(name))
        return cols


    def to_sql(self):
        res = 'CREATE TABLE ' + self.name + '(\n'
        res += self.sql_col_def()
        res += ');\n'
        return res

    def to_mermaid(self):
        res = '    class '+self.name+'\n'
        for name in self.data['properties'].keys():
            res +='    '+self.name+' : +'+name+': '+self.data['properties'][name]['type']
        return res
    def to_java(self):
        res = '\n\n'
        res += 'public class ' + self.name + ' {\n\n'
        for name in self.data['properties'].keys():
            res += '    private '+openapitype_to_java(self.data['properties'][name]['type'])+' '+name+';\n'
        # TODO getter und setter
        res = '\n}'
        return res


def help():
    print('Usage: python -m nwebclient.openapi sql-create --url {url}')


def main():
    help()
    args = util.Args()
    text = requests.get(args.getValue('url')).text
    api = OpenApi(text)
    #args.dispatch(
    #    sql_create=lambda: print(api.to_sql())
    #)
    print(api.to_sql())


if __name__ == '__main__':
    main()
