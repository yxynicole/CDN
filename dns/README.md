## how to run dns server 

open first terminal and run

```python
python3 dns/server.py -p 8080 -n xyz.com
```


## how to test running server

open second terminal and run

```bash
dig @localhost -p 8080 xyz.com
```
