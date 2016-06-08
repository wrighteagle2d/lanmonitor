# lanmonitor
A set of simple scripts to monitor rcssserver auto test status (working in combination with [autotest2d](https://github.com/wrighteagle2d/autotest2d))

# Usages
- Change `host` in `client/client.py` to the address of a central server
- Change the address in `server/server.py` accordingly
- Deploy and run `server/server.sh` in `/usr/local/bin/lanmonitor/server` directory to the server machine
- Deploy and run `client/client.sh` in `/usr/local/bin/lanmonitor/client` directory to several client machines
- Run an auto test using `autotest2d` with `CLIENTS` configured as the above clients
- Visit the generated `index.html` in the server directory with your favorite `HTTPSERVER` and browser

