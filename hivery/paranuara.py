import json
import db
import falcon
import logging
from collections import OrderedDict


            
class Resource(object):

    def on_get(self, req, resp,company_name):
        session = db.get_session()
        employees = []
        try:
            logging.info("into on_get method")
            result = session.execute(""" SELECT name from trans_people, dim_company where company_id = id and company_name = UPPER(:name)
                                    """,{"name":company_name}).fetchall()
            
            if not result:
                resp.status = falcon.HTTP_404
                resp.body= json.dumps({'error':"Sorry.It looks like there are no employees listed for the particular company"})
            else:
                for row in result:
                        employees.append(row['name'])
                # Create a JSON representation of the resource
                resp.body= json.dumps({'employees':employees},ensure_ascii=False)
            
            
        except Exception as e:
            db.PrintException()
            resp.status = falcon.HTTP_500
        finally:
            session.close()

class FriendResource(object):

    def on_get(self, req, resp,ppl_one,ppl_two):
        session = db.get_session()
        mutual_friends=[]
        try:
            friend_result = session.execute(""" 
                                        SELECT name from trans_people WHERE ppl_id IN(SELECT friend_ppl_id FROM trans_friends a, trans_people b WHERE a.ppl_id = b.ppl_id and EXISTS
                                        (SELECT * FROM (SELECT c.ppl_id,c.friend_ppl_id from trans_friends c, trans_people d where c.ppl_id = d.ppl_id and d.name =:ppl_one ) c WHERE a.friend_ppl_id = c.friend_ppl_id AND b.name = :ppl_two)) AND UPPER(eye_colour) = 'BROWN' AND has_died = 0
                                        """,{"ppl_one":ppl_one,"ppl_two":ppl_two}).fetchall()

            if not friend_result:
                    mutual_friends ='There are no mutual friend who are alive and have brown eyes'
            else:
                for row in friend_result:
                    mutual_friends.append(row['name'])

            ppl_result = session.execute("""SELECT name,age,address,phone FROM trans_people WHERE name = :ppl_one OR name =:ppl_two
                                            """,{"ppl_one":ppl_one,"ppl_two":ppl_two}).fetchall()
            
            if not ppl_result:
                resp.status = falcon.HTTP_404
                resp.body= json.dumps({'error':"Sorry.It looks like there is no one listed under the names given"})
            else:   
                result_two = json.loads(json.dumps([dict(r) for r in ppl_result],ensure_ascii=False))
                resp.body = json.dumps({'details':result_two,'mutual_friends':mutual_friends})
                
        except Exception as e:
            db.PrintException()
            resp.status = falcon.HTTP_500
        finally:
            session.close()      

class PeopleResource(object):

    def on_get(self,req,resp,ppl_one):
        session = db.get_session()
        try:
            detail = OrderedDict()
            vegetables = []
            fruits=[]
            result = session.execute(""" SELECT name,age from trans_people where name = :name
                                    """,{"name":ppl_one}).fetchone()
            if not result:
                resp.status = falcon.HTTP_404
                resp.body= json.dumps({'error':"Sorry.It looks like there is no one listed under the name given"})
            else:
                fav_food = session.execute("""SELECT b.food_name,b.is_fruit FROM trans_fav_food a, dim_fav_food b, trans_people c
                                                WHERE a.ppl_id = c.ppl_id and a.food_name = b.food_name and c.name= :name
                                                """,{"name":ppl_one}).fetchall()
                detail['username']= result['name']
                detail['age'] = result['age']
                for row in fav_food:
                    if row['is_fruit']==1:
                        fruits.append(row['food_name'])
                    else:
                        vegetables.append(row['food_name'])
                detail['fruits'] = fruits
                detail['vegetables']= vegetables 
                # Create a JSON representation of the resource
                resp.body= json.dumps(detail,ensure_ascii=False)
        except Exception as e:
            db.PrintException()
            resp.status = falcon.HTTP_500
        finally: 
            session.close()