# Authentication to SD-WAN Manager

## Pre-20.18

Pre-17.17, the application authenticates with vManage using credentials passed in the body of POST /j_security_check.  The response sets a JSESSIONID cookie.  The application may need to make an additional call to GET /dataservice/client/token, passing in the JSESSIONID cookie in the request header to obtain a XSRF token.  Subsequent API calls need to pass in the JSESSIONID and depending on the call, the X-XSRF-TOKEN as cookies within the request header.

Log in with a user name and password to establish a session:

### 1. Authenticate

`POST /j_security_check` with `content type x-www-form-urlencoded`. The user name and password are submitted as `j_username` and `j_password`. The session token is in the response http cookie, `JSESSIONID={session hash}`.

```example
POST https://{vmanage-ip-address}/j_security_check
Content-Type: application/x-www-form-urlencoded
HTTP Body:
  "j_username={admin}&j_password={credential}"
```

If a user is successfully authenticated, the response body is empty and a valid session cookie is set is response (set-cookie: JSESSIONID=). If a user is un-authenticated, the response body contains a html login page with tag in it. API client should check the response body for to identify whether the authentication is successful or not. This is the behavior of our application server.


### 2. Get a Cross-Site Request Forgery Prevention Token

Get a cross-site request forgery prevention token, which is required for most POST operations:

`GET /dataservice/client/token` with content type application/json. The `JESSIONID={session hash}` cookie is required to authenticate.
The XSRF token is in the response body. Use the XSRF token along with the JESSIONID cookie for ongoing API requests.

```example
GET https://{vmanage-ip-address}/dataservice/client/token
Content-Type: application/json
HTTP Header:
  "Cookie: JESSIONID={session hash id}"
```

### 3. Make an API Call

Make an API request

For non-whitelisted endpoints, the user needs to provide an API token as a cookie: `JESSIONID={session hash}`.

For POST requests, the user also needs to provide the matching XSRF token.

```example
https://{vmanage-ip-address}/dataservice/{api-endpoint-url}
Content-Type: application/json
HTTP Header:
  "Cookie: JESSIONID={session hash id}"
  "X-XSRF-TOKEN: {XSRF token}"
```

### 4. Log out and destroy the session

The user needs to log out after finishing the API requests. This is not only a good security practice, but also releases the allocated session resource.

If the http response code is 302 redirect with location header `https://{vmanage-ip-address}/welcome.html?nocache=`, the session has been invalidated. Otherwise, an error occurred in the session invalidation process.

```example
POST https://{vmanage-ip-address}/logout?nocache={random-number}`
HTTP Header: "Cookie: JESSIONID={session hash id}"
```

### 5. Code snippet

```python
class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, username, password):
        api = "/j_security_check"
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        url = base_url + api
        payload = {'j_username' : username, 'j_password' : password}

        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return(jsessionid[0])
        except:
            print("No valid JSESSION ID returned\n")
            exit()

    @staticmethod
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None

Auth = Authentication()
jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,vmanage_username,vmanage_password)
token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)

if token is not None:
    header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json",'Cookie': jsessionid}

```


## With 20.18

Support for jwt tokens. Form/JSession based authentication will still work in 20.17+ release. In addition, we introduce JWT token based authentication in 20.18.There is no change for X-XSRF-TOKEN.

The application will authenticate using the POST /jwt/login to obtain the jwt token which is used for subsequent API calls.
