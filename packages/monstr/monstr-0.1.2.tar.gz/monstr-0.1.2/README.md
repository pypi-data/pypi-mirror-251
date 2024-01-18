# monstr

Monstr: Python Nostr module. Python code for working with nostr.

* A basic relay implementation for testing against locally
* Client for working with a single relay
* ClientPool for working with multiple relays
* Keys for working with and converting between hex/npub/nsec
* Entities for encoding and decoding NIP19 nostr entities

# install
```sh
git clone https://github.com/monty888/monstr.git
cd monstr
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt # or pip install .
# probably required to run examples else nostr module won't be found
export PYTHONPATH="$PYTHONPATH:./"
```
to use postgres as store psycopg2 must be installed
```sh
# install wheel helper, if needed.
pip pip install wheel
# maybe required on linux
# sudo apt install postgresql automake pkg-config libtool
# maybe required on mac
# brew install postgresql automake pkg-config libtool libffi
# now actually install psycopg2
pip install psycopg2
```

# test `monstr` package import
```py
# create a new python shell
python3
>> import monstr
>> from monstr.encrypt import Keys
>> test = Keys()
>> Keys.is_valid_key(test.private_key_hex())
True
>>
```

Note: developed against python 3.10.6

# use 

### basic queries with context manager
```python

    from monstr.client.client import Client

    async with Client(url) as c:
        events = await c.query({
            'limit': 100
        })

        for c_evt in events:
            print(c_evt)
```
### basic queries without context manager

```python

    from monstr.client.client import Client

    c = Client(url)
    asyncio.create_task(c.run())
    await c.wait_connect()
    events = await c.query({
        'limit': 100
    })

    for c_evt in events:
        print(c_evt)
    c.end()
```

### further examples

**/monstr/examples/keys.py** - create new keys or look up other representation of existing keys  

**/monstr/examples/create_test_env** - creates a test environment relay running on local host port 8888 storing data in sqlitedb
prepopulated with some data - currently hardcoded to come from relay wss://nostr-pub.wellorder.net
and based on key 5c4bf3e548683d61fb72be5f48c2dff0cf51901b9dd98ee8db178efe522e325f. The relay 
also has HTTP get methods added:  
* /e
* /req
* /view_profile

**/monstr/examples/basic_usage.py** - examples query and post to test relay

**/monstr/examples/post_text.py** - type in and post text events to test relay

**/monstr/examples/print_text_notes.py** - display text notes for given key, EOSE and EVENT

**/monstr/exampels/query.py** - simple cmd line queries see query.py --help  

**/monstr/examples/simple_bot.py** - a simple bot that return the count for each time it gets a message for a pub_k 

**/monstr/examples/view_profile.py** - simple webserver running at 8080 with method /view_profile?pub_k={a_pub_k} that returns that profiles data by querying the local relay

# Contribute:

-- TODO
