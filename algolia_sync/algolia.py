
from algoliasearch.search_client import SearchClient 
import frappe 
import json
import itertools

client = SearchClient.create('WVG1ZYK6U9','3b5461f1aa258882624decbda14db7e9')
index = client.init_index('dev_item')

def send_algolia(doc,event):
    items = frappe.get_doc('Item', doc.name)
    attribute_list=[]
    value_list=[]
    for i in items.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)
    image2 = items.website_image_2
    image3 = items.website_image_3
    records = {"item":items.item_name,"item_code":items.item_code,"item_group":items.item_group,"Description":items.description,"imageURL":[items.website_image,image2,image3],"Item_price":items.standard_rate,attribute_list[0]:value_list[0],attribute_list[1]:value_list[1] }
    send = index.save_object(records,  {'autoGenerateObjectIDIfNotExist': True})
    
    for ids in send:

        obj_id = ids["objectIDs"]
        update = frappe.db.set_value('Item',doc.name,'algolia_id', obj_id)
        

def delete_object(doc,event):

    item_doc = frappe.get_doc('Item',doc.name)

    algolia_id = item_doc.algolia_id

    del_object = index.delete_object(algolia_id)

def update_object(doc,event):

    item_doc = frappe.get_doc('Item',doc.name)
    
    attribute_list=[]
    value_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value) 
    # frappe.throw(attribute_list)
    
    algolia_id = item_doc.algolia_id
    item_name = item_doc.item_name
    item_code = item_doc.item_code
    item_group = item_doc.item_group
    item_price = item_doc.standard_rate
    image1 = item_doc.website_image
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    description = item_doc.description
    update_object = index.partial_update_object({"objectID":algolia_id,"item":item_name,"item_code":item_code,"item_group":item_group,"Description":description,"imageURL":[image1,image2,image3],"item_price":item_price,attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2]},{'createIfNotExists':False})
    
    # frappe.throw(attribute_list[2])
    # frappe.throw(value_list[2])
    
def show_website(doc,event):
    item_doc = frappe.get_doc('Item',doc.name)
    algolia_id = item_doc.algolia_id
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    attribute_list=[]
    value_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)

    
    records = {"objectID":algolia_id,"item":item_doc.item_name,"item_code":item_doc.item_code,"item_group":item_doc.item_group,"Description":item_doc.description,"imageURL":[item_doc.website_image,image2,image3],"item_price":item_doc.standard_rate,attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2]}
    if item_doc.show_in_website == 1 or item_doc.show_variant_in_website == 1:
        send = index.save_object(records)
    else:
        del_object = index.delete_object(algolia_id)


