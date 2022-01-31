from DB.Tables import User, Goods, session


def check_user_db(id_user):
        query = session.query(User).filter_by(id=id_user)
        query = list(query)

        if query == []:
            return False

        else:
            return True

