# Assumption

## Channel Assumptions

### Channel Invite
- Channel ID must be valid
- User ID must be valid
- User ID not in the channel
- Token needs to be unique and valid (Token can only be used once)
- Only Channel member can invite
- One invite per member

### Channel details
- Channel ID is valid and unique
- Token ID is valid and unique
- Keep track on the number of members

### Channel messages
- Channel ID needs to be valid
- Keep track on the latest 50 messages
- Valid User ID

### Channel_leave
- Channel member minus   
-  Valid User ID
- Channel ID needs to be valid

### Channel_join  
- Channel member add 1
- Valid User ID
- Channel ID needs to be valid

### Channel_addowner
- Valid User ID
- Channel ID needs to be valid
- Must from Owner ID
- Channel can have one owner

### Channel_removeowner
- Must from Owner ID
- RNG u_ID becomes owner


## Channels Assumptions

### For channels_list
- Valid token (input)
- Valid channels 
- Channels & associated details correctly linked to User ID
- User is authorised to view channels in list
- User token is correctly matched to User ID
- List displays all information (not just some of the channels, etc.)
- Function returns a list (an empty list if no channels are found)
- User is able to view private channels they are a member/ admin of.

### For channels_listall:
- Valid token (input)
- If this is used to view all channels for admin and server purposes:
    - Admin privileges are required to view all public & private channels.
    - Internal server has admin privileges.
- If this is used to view channels that a User may join/ for navigation:
    - User can only view public channels/ private channels they are a member of.
- Function returns a list (an empty list if no channels are found)

### For channels_create:
- Valid token (input)- no empty string, unique
- Valid name (input)- no empty string
- Valid is_public varible (input)
- Input error if name > 20 characters
- New 'empty' channel is created-> only member is admin, no messages, etc.
- Channel is set as either public or private
- That this channel will be/ is linked to the creator of the channel (as an admin):
    - Internal server has admin privileges in order to assign creator as admin.


## Auth Assumptions

### For auth_register:
 - Valid token generated (unique)
 - Valid first name (input)
 - Valid last name (input)
 - Valid email address (input)
 - Valid password (input)
 - Valid User ID
 - Input error if first name is empty or > 50 characters
 - Input error if last name is empty or > 50 characters
 - Input error if invalid email address
 - Input error if password < 6 characters

### For auth_login:
 - Valid token generated (unique)
 - Valid first name
 - Valid last name
 - Valid email address (input)
 - Valid password (input)
 - Valid User ID
 - Input error if invalid email address
 - Input error if invalid password

### For auth_logout
 - Valid token (input)- active
 - Returns true if successful logout, or false if already logged out.
