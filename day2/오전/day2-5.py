# 포함관계(in, not in)
# if role == 'admin' or role =='manager'
allowed_role = ['admin','manager','staffe']
role = 'admin'
if role in allowed_role:
    print('접근 허용')
else:
    print('접근 불가')