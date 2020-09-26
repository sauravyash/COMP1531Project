# Assumption/ Channel
---
## Channel Assumptions
### Channel Invite
- Channel ID must be valid
- User ID must be valid
- User ID not in the channel
- Token needs to be unique and valid (Token can only be used once)
- Only Channel member can invite
- One invite per member

### Channel details:
- Channel ID is valid and unique
- Token ID is valid and unique
- Keep track on the number of members

### Channel messages:
- Channel ID needs to be valid
- Keep track on the latest 50 messages
- Valid User ID

### Channel_leave: 
- Channel member minus   
-  Valid User ID
- Channel ID needs to be valid

### Channel_join:    
- Channel member add 1
- Valid User ID
- Channel ID needs to be valid

### Channel_addowner:
- Valid User ID
- Channel ID needs to be valid
- Must from Owner ID
- Channel can have one owner

### Channel_removeowner:
- Must from Owner ID
- RNG u_ID becomes owner
