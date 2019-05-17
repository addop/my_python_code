import jqdata


def login(user, pw):
    try:
        auth(user, pw)
        return True
    except Exception as e:
        print(e)
        return False


state = login('17192185537', 'Zh19930924')
# query_count = jt.get_query_count()
# print('剩余次数: ', query_count, state)
print(state)