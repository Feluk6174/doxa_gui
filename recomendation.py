import api
import math
import json
import threading

import access_my_info

def get_pos(connection:api.Connection, users:list[str]):
    user_info = connection.get_users(users)
    return [(user["user_name"], user["pos"]["pos"]) for user in user_info]

def get_user_names(connection:api.Connection, posts:list[str]):
    post_info = connection.get_posts(id=posts)
    print(post_info)
    try:
        return post_info, [post["user_id"] for post in post_info]
    except KeyError:
        return post_info, []

def get_own_pos(connection:api.Connection, user_name:str):
    user_info = connection.get_user(user_name)
    return user_info["pos"]["pos"]

def calc_positive_vectors(own_pos, positions):
    vectors = []
    for pos in positions:
        print(type(pos), pos, type(own_pos), own_pos)
        vectors.append([pos[i]-own_pos[i] for i in range(len(pos))])
    return vectors

def calc_negative_vectors(own_pos, positions):
    print(own_pos, positions)
    vectors = []
    for pos in positions:
        vectors.append([own_pos[i]-pos[i] for i in range(len(pos))])
    return vectors

def add_vectors(*vector_lists):
    res = [0.0 for _ in range(len(vector_lists[0][0]))]
    for vector_list in vector_lists:
        for vector in vector_list:
            for i in range(len(res)):
                try:
                    res[i] += vector[i]
                except IndexError:
                    res[i] += 0
    return res

def average_module(*vector_lists):
    res = 0.0
    iteration = 0
    for vector_list in vector_lists:
        for vector in vector_list:
            res += math.sqrt(sum([arg**2 for arg in vector]))
            iteration += 1
    return res/iteration

def calculate_final(vector:list[float], avg_module:float):
    module = math.sqrt(sum([arg**2 for arg in vector]))
    normalized_vector = [arg/module for arg in vector]
    print(1, normalized_vector)
    final_vector = [arg*avg_module for arg in normalized_vector]
    return final_vector

def calc_pos(own_pos:list[float], vector:list[float]):
    return [own_pos[i]+vector[i] for i in range(len(vector))]

def update_pos(connection:api.Connection, likes:list[str], dislikes:list[str], following:list[str], own_user_name:str, priv_key):
    own_pos = get_own_pos(connection, own_user_name)
    print(own_pos)
    
    following_pos = get_pos(connection, following)
    
    likes_info, users_likes = get_user_names(connection, likes)
    dislikes_info, users_dislikes = get_user_names(connection, dislikes)

    likes_pos = get_pos(connection, users_likes)
    dislikes_pos = get_pos(connection, users_dislikes)

    following_pos = [user[1] for user in following_pos]

    temp = []
    for info in likes_pos:
        for _ in range(users_likes.count(info[0])):
            temp.append(info[1])

    likes_pos = temp

    temp = []
    for info in dislikes_pos:
        for _ in range(users_dislikes.count(info[0])):
            temp.append(info[1])

    dislikes_pos = temp

    likes_vectors = calc_positive_vectors(own_pos, likes_pos)
    dislikes_vectors = calc_negative_vectors(own_pos, dislikes_pos)
    following_vectors = calc_positive_vectors(own_pos, following_pos)

    avg_module = average_module(likes_vectors, dislikes_vectors, following_vectors)
    vector = add_vectors(following_vectors, likes_vectors, dislikes_vectors)
    print(2, vector, avg_module)
    final_vector = calculate_final(vector, avg_module)
    print(3, final_vector)
    pos = calc_pos(own_pos, final_vector)

    connection.update_pos(own_user_name, pos, priv_key)
    print(pos)

def get_calc_info():
    return access_my_info.get_user_name(), access_my_info.get_following(), access_my_info.get_liked_id(), [], access_my_info.get_priv_key()

def recomendation_thread():
    connection = api.Connection("34.175.220.44", 30003)
    user_name, following, liked, disliked, priv_key = get_calc_info()
    update_pos(connection, liked, disliked, following, user_name, priv_key)
    connection.close()

def start():
    thread = threading.Thread(target=recomendation_thread)
    thread.start()

if __name__ == "__main__":
    import auth
    priv_key, pub_key = auth.get_keys("Encryption3")
    conn = api.Connection(host="34.175.220.44", port=30003)
    likes = [6944621523578514130, 7059199636460889928, 1915575247258266844, 4736148301386577443, 9201594495180409724, 3045622388096265858, 4475756610220643193, 5084639947606855714, 6695412984306455998, 7339758310394585263, 7480698144295845361, 8194539549398005816, 9011660353629230397, 1753910482091284737, 4140938122884328889, 5893776177057732069, 6097899059139852110]
    dislikes = [4884953191363853822, 544415039804386557 , 6429385432085904977, 7513512029627912653, 8401281896670198152, 9020834178117821992, 6496761605344240154, 8139192730068770939, 979037123386232739 , 138193217647863819 , 1687815330118206646, 1963039643112552616, 23614833863001096  , 2500791660549007988, 2764770418760741171, 3548288859908700583, 4684194317318931492, 5554698916488725406]
    following = ["JoanCarxofes17", "jos", "Josue._", "juliafont", "kfraunberg", "Llovera", "Monika", "Paulet05", "PauTri", "rogersigma" , "santi", "Santiago", "sdfghjk", "sdrfghjkl"]

    update_pos(conn, [str(like) for like in likes], [str(dislike) for dislike in dislikes], following, "Encryption3")