# Features
* MongoDB Queueing data from sensors, able to make sessions via tokens to stream data directly to a consuming microservice.

* Sensor Connected to a site post there data to a message broker, if they have correct API key. 

* Microservice can consume messages from database and able to stream directly from the broker if required, if API key is accepable

* Microservices have API key, originzations, users or other origins can access this microservice if they have a valid Token/API key, unless Microservice is set as public domain.

* Sensor is able to be remotly regulate network posts to ensure concurency within the system.

* Originzation is able to handel its users, API keys, connected Microservices and distrubute it as it deems necessery.

* The system should be distributed and data should be access from its entiernty between clods within authenticated messures. 
