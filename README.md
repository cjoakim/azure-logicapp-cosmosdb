# azure-logicapp-cosmosdb

Simple HTTP-triggered Azure Logic App that writes to CosmosDB

---

## HTTP Client 

Implemented in Python, creates and HTTP POSTs a randomized JSON document 
like the following to the Azure Logic App.

```
{
  "id": "48431681-2512-4666-a3b7-c70b54b502a9",
  "pk": "G",
  "epoch": 1593446959,
  "doctype": "logic_app_post",
  "x": "X-3452",
  "y": "Y-28176"
}
```

Note that an **id** uuid value is generated, as well as the **pk** - the CosmosDB
partition key attribute name for the target container.

### HTTP Client Setup and Execution

```
$ git clone https://github.com/cjoakim/azure-logicapp-cosmosdb.git
$ cd azure-logicapp-cosmosdb
$ cd py
$ ./venv.sh create                                # <-- create the python virtual environment with PyPI libs
$ source bin/activate                             # <-- activate the python virtual environment
$ python http_client.py invoke_http_logic_app     # <-- execute the program, post a doc to the Logic App
```

---

## CosmosDB Configuration 

### Initial Error

```
{
    "statusCode": 400,
    "headers": {
        "x-ms-last-state-change-utc": "Fri,26 Jun 2020 19:59:50.185 GMT",
        "lsn": "1",
        "x-ms-schemaversion": "1.9",
        "x-ms-quorum-acked-lsn": "1",
        "x-ms-substatus": "1001",
        "x-ms-current-write-quorum": "3",
        "x-ms-current-replica-set-size": "4",
        "x-ms-xp-role": "1",
        "x-ms-global-Committed-lsn": "1",
        "x-ms-number-of-read-regions": "0",
        "x-ms-transport-request-id": "1",
        "x-ms-cosmos-llsn": "1",
        "x-ms-cosmos-quorum-acked-llsn": "1",
        "x-ms-session-token": "0:1",
        "x-ms-request-charge": "0",
        "x-ms-serviceversion": "version=2.11.0.0",
        "x-ms-activity-id": "496a279d-ba5d-48ff-a7fc-85187cc10602",
        "Strict-Transport-Security": "max-age=31536000",
        "x-ms-gatewayversion": "version=2.11.0",
        "Timing-Allow-Origin": "*",
        "x-ms-apihub-cached-response": "true",
        "Date": "Mon, 29 Jun 2020 15:30:32 GMT",
        "Content-Length": "1170",
        "Content-Type": "application/json"
    },
    "body": {
        "code": "BadRequest",
        "message": "Message: {\"Errors\":[\"The partition key supplied in x-ms-partitionkey header has fewer components than defined in the the collection.\"...
    }
}
```