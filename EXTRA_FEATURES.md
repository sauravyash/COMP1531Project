# New Features
## 1. Remove_member
- Allows the owner of a channel or the owner of Flockr to remove a member from a channel.
- This member may rejoin or be invited to rejoin after if they wish to.
- Arguments: 
    - token (of user requesting removal)
    - channel_id (of channel the member is being removed from)
    - user_id (of user being removed)
- Raise an INPUT ERROR:
    - Channel ID is not a valid channel.
    - When user with user_id does not exist or is not a member of the channel.
- Raise an ACCESS ERROR:
    - When the token is invalid or does not exist.
    - When the authorised user is not an owner of the flockr, or an owner of this channel.

## 2. Ban_member
- Allows the owner of a channel or the owner of Flockr to ban a member from a channel.
- This member may never rejoin or be invited to this channel again.
- Arguments: 
    - token (of user requesting removal)
    - channel_id (of channel the member is being removed from)
    - user_id (of user being removed)
- Return:
    - Empty dictionary, {}.
- Raise an INPUT ERROR:
    - Channel ID is not a valid channel.
    - When user with user_id does not exist or is not a member of the channel.
- Raise an ACCESS ERROR:
    - When the token is invalid or does not exist.
    - When the authorised user is not an owner of the flockr, or an owner of this channel.

## 3. Monitor_Language
- Monitors channel messages for 'offensive language'. 
- If a message contains 'offensive language' the owner of flockr will recieve an email containing:
    - The channel the message is contained in.
    - The handle of the user who sent this message.
- Arguments: 
    - message (not more than 1000 characters)
    - user_id of the message sender.
- Return:
    - True if the message contains offensive language (ie. swearing, racial slurs, etc.)
    - False if the message is clean.
- Raise an INPUT ERROR:
    - Message is more than 1000 characters.
    - u_id does not exist.

## 4. Extra_permissions
- Allows the owner of Flockr to change user roles with more permission options.
- New Roles:
    - (3) Channel master: Can view & join any channel regardless of public/ private settings.
    - (4) Policing member: Can remove and ban any member, even if they are not an owner of a channel.
- Arguments: 
    - token (of user requesting change)
    - permission_id of change (ie. 3 or 4)
    - user_id (of user being changed)
- Raise an INPUT ERROR:
    - Channel ID is not a valid channel.
    - When user with user_id does not exist or is not a member of the channel.
    - When permission ID is not 1-4. (append this to other permission_change function)
- Raise an ACCESS ERROR:
    - When the token is invalid or does not exist.
    - When the authorised user is not an owner of the flockr.