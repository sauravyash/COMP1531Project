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
- Raise an INPUT ERROR:
    - Channel ID is not a valid channel.
    - When user with user_id does not exist or is not a member of the channel.
- Raise an ACCESS ERROR:
    - When the token is invalid or does not exist.
    - When the authorised user is not an owner of the flockr, or an owner of this channel.