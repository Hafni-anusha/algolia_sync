from algoliasearch.search_client import SearchClient 
import frappe 
import json


client = SearchClient.create('NACKX1OJD8', '9363abde47bfbf7a153516be09475db4')
index = client.init_index('dev_item')

def send_algolia(doc,event):
    items = frappe.get_doc('Item', doc.name)
    records = {"item":items.item_name,"item_code":items.item_code,"item_group":items.item_group}

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
    algolia_id = item_doc.algolia_id
    item_name = item_doc.item_name
    item_code = item_doc.item_code
    item_group = item_doc.item_group

    update_object = index.partial_update_object({"objectID":algolia_id,"item":item_name,"item_code":item_code,"item_group":item_group},{'createIfNotExists':False})
    
def show_website(doc,event):
    item_doc = frappe.get_doc('Item',doc.name)
    algolia_id = item_doc.algolia_id
    records = {"objectID":algolia_id,"item":item_doc.item_name,"item_code":item_doc.item_code,"item_group":item_doc.item_group}

    if item_doc.show_in_website ==1:
        send = index.save_object(records)
    else:
        del_object = index.delete_object(algolia_id)


