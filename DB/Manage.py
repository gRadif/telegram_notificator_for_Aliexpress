from DB.Tables import User, Goods, session


def check_user_db(id_user):
        query = session.query(User).filter_by(id=id_user)
        query = list(query)

        if query == []:
            return 'unauthenticated'

        elif query != []:
            return 'is_authenticated'

def get_goods_all_data_all_users():
    goods_all_data_list = []
    goods_all = session.query(Goods)
    for goods in goods_all:
        temp_dict = {}
        temp_dict['id'] = goods.id
        temp_dict['link'] = goods.link
        temp_dict['price'] = goods.price
        temp_dict['user_id'] = goods.user_id

        goods_all_data_list.append(temp_dict)

    return goods_all_data_list


