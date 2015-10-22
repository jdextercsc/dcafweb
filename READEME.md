## To use:

```
# git clone <repoURL>

# cd dcafweb

# virtualenv venv

# . venv/bin/activate

# pip install -r requirements.txt

# python run.py
```

## Other Notes:

* No discovery of URL yet
Currently the URL discovery has no functionality, it's only there for visual purposes now

* Test host list
When navigating to the host selection page, the following URL can be used to see a test table:

```
http://0.0.0.0:5000/hosts/debug
```
Otherwise the page will report 'no hosts found'
