# New Features
## 1. Kick Member (kickmember)
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

## 2. Ban Member (ban_member)
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

## 3. NSFW Channel Censor
- Monitors channel messages for 'offensive language'.
- If a message contains 'offensive language':
    - The word will be replaced with a random string of special characters of the same length.
- Arguments:
    - message (not more than 1000 characters)
    - channel_id of the channel the message is contained in.
- Return:
    - The edited message.
- Raise an INPUT ERROR:
    - Message is more than 1000 characters.
    - channel_id does not exist.
    
## 4. Deployment to Heroku
- This project has been deployed to heroku.
- This means it can now be accessed remotely via a unique url.
- Frontend url: https://flockr-frontend.herokuapp.com/register
- Backend url: https://flockr-backend.herokuapp.com/
