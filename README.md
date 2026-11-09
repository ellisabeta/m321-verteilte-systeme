# m321-verteilte-systeme

## Service B
Service B is a Python app. When you open its /ping endpoint, it requests the list of people from Service A and returns one line of text with a pipe (|) between people.

### 1. Start Service B in terminal 2

Open a second terminal in the Service B folder that contains service_b.py. Service B uses Python’s standard library, so you can run it directly:

python service_b.py

If your copy is named Service-B.py, run python Service-B.py instead.

### 2. Check the connection

Open Service B’s /ping endpoint. With Service A’s sample data, you should see:

Tommy, Vice City | Niko, Liberty City | Pico, Mini Liberty City

The Service B home page shows the Hello World message. Use /ping to test the call between the two services.
