local results = {}
local fantom_shares_ids = {}
local unacked_shares_ids = {}
local unacked_messages_ids = {}

local count = tonumber(ARGV[1]) - 1
local acks_timeout = tonumber(ARGV[2])
local messages_prefix = ARGV[3]
local pending_messages_prefix = ARGV[4]

local ready_shares_key = KEYS[1]
local ranged_shares_key = KEYS[2]
local unacked_shares_key = KEYS[3]
local pending_shares_key = KEYS[4]

local time = redis.call('TIME')
local ready_shares_ids = redis.call('ZRANGE', ready_shares_key, 0, count)

if #ready_shares_ids < count then
    redis.call('ZREMRANGEBYSCORE', unacked_shares_key, '-inf', time[1] - acks_timeout)
    redis.call('ZRANGESTORE', ranged_shares_key, pending_shares_key, '-inf', time[1], 'BYSCORE')
    redis.call('ZDIFFSTORE', ready_shares_key, 2, ranged_shares_key, unacked_shares_key)
    ready_shares_ids = redis.call('ZRANGE', ready_shares_key, 0, count)
end

while #ready_shares_ids > 0 do
    local shares_ids = {}
    local messages_ids = {}
    local messages_keys = {}
    local pending_messages_keys = {}
    local next_ready_shares_ids = {}

    for idx, share_id in ipairs(ready_shares_ids) do
        local pending_messages_key = pending_messages_prefix .. ":" .. share_id
        local pending_messages_ids = redis.call('ZRANGE', pending_messages_key, 0, 0)

        if #pending_messages_ids == 0 then
            table.insert(fantom_shares_ids, share_id)
        else
            local message_id = pending_messages_ids[1]
            local message_key = messages_prefix .. ":" .. message_id

            table.insert(shares_ids, share_id)
            table.insert(messages_ids, message_id)
            table.insert(messages_keys, message_key)
            table.insert(pending_messages_keys, pending_messages_key)
        end
    end

    if #messages_keys > 0 then
        for idx, message in ipairs(redis.call('MGET', unpack(messages_keys))) do
            if message then
                table.insert(results, message)
                table.insert(unacked_shares_ids, shares_ids[idx])
            else
                table.insert(next_ready_shares_ids, shares_ids[idx])
                redis.call('ZREM', pending_messages_keys[idx], messages_ids[idx])
            end
        end
    end

    ready_shares_ids = next_ready_shares_ids
end

if #fantom_shares_ids > 0 then
    redis.call('ZREM', ready_shares_key, unpack(fantom_shares_ids))
    redis.call('ZREM', pending_shares_key, unpack(fantom_shares_ids))
end

if #unacked_shares_ids > 0 then
    local scored_unacked_shares_ids = {}

    for _, share_id in ipairs(unacked_shares_ids) do
        table.insert(scored_unacked_shares_ids, time[1])
        table.insert(scored_unacked_shares_ids, share_id)
    end

    redis.call('ZREM', ready_shares_key, unpack(unacked_shares_ids))
    redis.call('ZADD', unacked_shares_key, unpack(scored_unacked_shares_ids))
end

return results
