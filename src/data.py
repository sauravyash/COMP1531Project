global data
data = {
    'users': [
        {
            'id': 1,
            'name' : 'user1',
            'token': 'VALID token',
            'authenticated': True,
            'owner': 'owner'
        },
        {
            'id': 2,
            'name' : 'user2',
            'token': 'VALID token2',
            'authenticated': True,
            'owner': 'owner'
        },
        {
            'id': 5,
            'name' : 'user5',
            'token': 'VALID token5',
            'authenticated': True,
            'owner': 'owner'
        }
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
            'admins': ['exampleID1', 'exampleID2'],
            'members': [1,2],
            'messages': [
                {
                    'msg_id': 1,
                    'msg_author': "mbr1",
                    'msg_content': "hi",
                }
            ]
        }
       
    ]

}
