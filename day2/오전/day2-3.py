# class SafeProfile:
#     def __init__(self):
#         pass
#     def get(self,key):
#         return True

# user_profile = SafeProfile()
# print(user_profile.get('is_verified'))


# class SafeProfile:
#     def __init__(self):
#         pass
#     def get(self,key):
#         return True

# user_profile = None
# if user_profile.get('is_verified'):
#     print('성공')
# else:
#     print('실패')


# class SafeProfile:
#     def __init__(self):
#         pass
#     def get(self,key):
#         return True

# user_profile = None
# if user_profile and user_profile.get('is_verified'):
#     print('성공')
# else:
#     print('실패')


class SafeProfile:
    def __init__(self):
        pass
    def get(self,key):
        return True

user_profile = SafeProfile()
if user_profile and user_profile.get('is_verified'):
    print('성공')
else:
    print('실패')