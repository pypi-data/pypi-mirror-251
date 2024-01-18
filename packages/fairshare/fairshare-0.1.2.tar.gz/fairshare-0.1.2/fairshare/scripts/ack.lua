local share_id = ARGV[1]
local message_id = ARGV[2]
local message_key = KEYS[1]
local pending_shares_key = KEYS[2]
local unacked_shares_key = KEYS[3]
local pending_messages_key = KEYS[4]

local pending_messages_ids = redis.call('ZRANGE', pending_messages_key, 0, 1, 'WITHSCORES')

if #pending_messages_ids > 0 then
    redis.call('DEL', message_key)
    redis.call('ZREM', pending_messages_key, message_id)

    if pending_messages_ids[1] == message_id then
        redis.call('ZREM', unacked_shares_key, share_id)

        if #pending_messages_ids ~= 4 then
            redis.call('ZREM', pending_shares_key, share_id)
        else
            redis.call('ZADD', pending_shares_key, pending_messages_ids[4], share_id)
        end
    end
end
