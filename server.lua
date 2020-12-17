local http = require('http')
local qs = require('querystring')
local JSON = require('json')

local html = [[
<!doctype html>
<html>
  <head>
    <title> TEST </title>
    <p><!-- MESSAGE --></p>
    <style>
      *{
        font-family: sans-serif;
      }
    </style>
  </head>
  <body>
    <h1> Cookie Jar Actions </h1>
    <h3> User Sign Up </h3>
    <form method=POST>
      <input type="hidden" name="command" value="signup"/>
      <input type="text" name="arg2" placeholder="username"/> <br>
      <input type="password" name="arg1" placeholder="password"/> <br>
      <input type="password" name="confirm1" placeholder="confirm password"/> <br>
      <input type="email" name="arg3" placeholder="email (optional)"/> <br><br>
      <input type="submit" value="Sign Up"></input>
    </form>
  </body>
<html>
]]


http.createServer(function (req, res)
  local body = ""

  req:on('data', function(data)
    print("got data")
    body = body .. data
    print("body: ".. body)
  end)

  req:on('end', function()
    print("end req")
    if(req.body ~= nil) then
      print("req.body: " .. req.body)
    end
    if( req.method == "POST" ) then
      local stuff = qs.parse(body)
      print("POST data: " .. body)
      -- print("POST variables" .. post)
      -- print("arg1: ".. post['arg1'])
      for k,v in pairs(stuff) do
        print(k .. ": " .. v)
      end
      -- print(post)
      -- print("POST")
      -- print("data" .. body)
    else
      print("GET")
    end
    res:setHeader("Content-Type", "text/html")
    res:setHeader("Content-Length", #html)
    res:finish(html)

  end)

end):listen(1337, '127.0.0.1')

print('Server running at http://127.0.0.1:1337/')
