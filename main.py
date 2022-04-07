from csv import writer
from fileinput import filename
import lib_ag as la
from ruamel.yaml.comments import CommentedMap as OrderedDict
from ruamel.yaml import YAML
import sys
file_name =''
algorithName='2.ZI2.18'
filetype = '_lsat'
yaml_template=la.getTemplate(filetype)
yaml_reader = YAML()
excel_List=la.getExcel(algorithName,'1')
counter = 0
for rows in excel_List:
        if rows[12]=='number':
            yaml_template['columns'].append(OrderedDict([('name', rows[11]), ('type', OrderedDict([('type_class', 'BIGINT')]))]))
        if rows[12]=='date' and rows[11]!="ods$effective_from_dt":
            yaml_template['columns'].append(OrderedDict([('name', rows[11]), ('type', OrderedDict([('type_class', 'DATE')]))]))
        if str(rows[12]).find('number(')!=-1:
            yaml_template['columns'].append(OrderedDict([('name', rows[11]), ('type', OrderedDict([('type_class', 'DECIMAL'), ('precision', la.getDataFromSkobkiNumber(rows[12])[0]), ('scale', la.getDataFromSkobkiNumber(rows[12])[1])]))]))
        if str(rows[12]).find('varchar2(')!=-1:
            yaml_template['columns'].append(OrderedDict([('name', rows[11]), ('type', OrderedDict([('type_class', 'VARCHAR'), ('length', la.getDataFromSkobkiVarchar(rows[12]))]))]))
        if rows[6]=='BK' and str(rows[5].replace('_id','_num_id'))!=yaml_template['datastore']['business_keys'][counter]['business_key'] and counter ==0:
            yaml_template['datastore']['business_keys'][counter]['business_key']=yaml_template['datastore']['business_keys'][0]['business_key'].replace('key1_num_id',rows[5].replace('_id','_num_id'))
            counter= counter +1
        if rows[6]=='BK' and str(rows[5].replace('_id','_num_id'))!=yaml_template['datastore']['business_keys'][counter]['business_key'] and counter == 1:
          yaml_template['datastore']['business_keys'][counter]['business_key']=yaml_template['datastore']['business_keys'][0]['business_key'].replace('key2_num_id',rows[5].replace('_id','_num_id'))
#        if rows[6]=='BK' and str(rows[5].replace('_id','_num_id'))!=yaml_template['datastore']['business_keys'][0]['business_key']:
#            yaml_template['datastore']['business_keys'][0]['business_key']=yaml_template['datastore']['business_keys'][0]['business_key'].replace('key1_num_id',rows[5].replace('_id','_num_id'))
        if yaml_template['datastore']['business_keys'][counter]['field_map'] is None and rows[6]=='BK' :
            print(counter)
            yaml_template['datastore']['business_keys'][0]['field_map']=OrderedDict([(rows[11], rows[5])])

#        if yaml_template['datastore']['business_keys'][0]['satellites'][0]['satellite']!=str(rows[4]).replace(filetype,'').split('.')[1]:
#            yaml_template['datastore']['business_keys'][0]['satellites'][0]['satellite']=str(rows[4]).replace(filetype,'').split('.')[1]
#        if rows[5] is not None and rows[12] is not None and rows[6]!='BK' and rows[5]!='effective_date':
#            yaml_template['datastore']['business_keys'][0]['satellites'][0]['field_map'].insert(1,rows[5],rows[11])
        #ora_table : Change
        if rows[10] is not None:
            if yaml_template['creation']['ora_table']!=str(rows[10]).split('.')[1]:
                yaml_template['creation']['ora_table']=str(rows[10]).split('.')[1]
                file_name=str(rows[10]).split('.')[1]
#OrderedDict([str(rows[11]),str(rows[5])5
f=open('external_tables/'+file_name.lower()+algorithName.replace('.','').lower()+'.yaml','w')
yaml_reader.dump(yaml_template,f)
f.close()
#('satellites', [ordereddict([('satellite', 'sat_name'), ('field_map', ordereddict([('ods$effective_from_dt', 'effective_date'), ('1ods$effective_from_dt', '1effective_date')]))])])])])