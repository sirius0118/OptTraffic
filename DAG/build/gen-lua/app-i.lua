local http = require "resty.http"
local socket = require("socket")

compute_size = 1
req_size = 1000
res_size = 10000
downstream = {"app-k"}

-- 模拟计算的过程，设置计算量
local function compute(c_size)
    local temp = 0
    for i = 0, c_size, 1 do
        temp = 0
        for j = 0, 100, 1 do
            temp = temp + 1
        end
    end
end
local a = 'aaaaaaaaazaaaaaaaaazaaaaaaaaazaaaaaaaaazaaaaaaaaazaaaaaaaaazaaaaaaaaazaaaaaaaaazaaaaaaaaazaaaaaaaaaz'

local function http_post_client(url, timeout)
    local httpc = http.new()
    timeout = timeout or 30000
    httpc:set_timeout(timeout)

    local body_str = ''
    for i = 0, (req_size - 149) / 100, 1 do
        body_str = body_str .. a
    end

    local res, err_ = httpc:request_uri(url, {
            method = "GET",
            -- 在body内添加字符串可以修改请求的大小
            body=body_str,
            headers = {
                ["Content-Type"] = "application/x-www-form-urlencoded",
            }
    })
    httpc:set_keepalive(5000, 100)
    --httpc:close()
    return res, err_
end


-- 将IP在下面逐个访问

compute(compute_size)

if #downstream > 0 then
    for i = 1, #downstream, 1 do
        ip , resolver =  socket.dns.toip(downstream[i])
        local res, err = http_post_client("http://" .. ip .. ":80", 3000)
    end
end


local response = ''

for i = 0, res_size / 100, 1 do
    response = response .. a
end
ngx.header.content_type = "text/plain"
-- 在ngx.say内添加内容可以实现修改响应的大小

ngx.say("200" .. response)
