# This file contains the appliation state data that is shared by the entire program

data = {
    'users': [],
    'channels': [],
    'tokens': []
}

'''
EXAMPLE
data = {
    'users': [
        {
            'id': 1,
            'name' : 'user1',
        },
        {
            'id': 2,
            'name' : 'user2',
        },
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
            'admins': [ 'exampleID1', 'exampleID2'],
            'members': [ 'mbr1', 'mbr2'] ,
            'messages' [
                  {
                      'msg_id': 1,
                      'msg_author': "mbr1",
                      'msg_content': "hi"
                  }
             ]
            'is_public': True
        },
        {
            'id': 2,
            'name' : 'channel2',
            ...
        },
    ],
    'tokens': [
        {
            'user_id': "mbr1",
            'token': "1234"
        },
        {
            ...
        }
    ]
}
'''
