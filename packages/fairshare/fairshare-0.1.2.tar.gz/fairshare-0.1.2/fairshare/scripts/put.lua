local share_id = ARGV[1]
local message_id = ARGV[2]
local message_data = ARGV[3]
local message_limit = tonumber(ARGV[4])
local message_defer_by = tonumber(ARGV[5])
local message_expire_in = tonumber(ARGV[6])

local message_key = KEYS[1]
local pending_shares_key = KEYS[2]
local pending_messages_key = KEYS[3]

if message_limit ~= -1 then
    if message_limit <= redis.call('ZCARD', pending_messages_key) then
        return 0
    end
end

local time = redis.call('TIME')
local time_as_float = tonumber(time[1] .. "." .. time[2])

redis.call('SET', message_key, message_data, 'NX', 'EX', message_expire_in)
redis.call('ZADD', pending_shares_key, 'LT', time_as_float + message_defer_by, share_id)
redis.call('ZADD', pending_messages_key, 'NX', time_as_float + message_defer_by, message_id)

return 1
