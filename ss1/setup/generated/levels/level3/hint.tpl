This one is a web-based vulnerability, so go ahead and
point your browser to http://localhost:__NEXT_LEVEL_PORT__/

As it turns out, it's a public uppercasing service. You can POST data to it,
and it will uppercase it for you:

  curl localhost:__NEXT_LEVEL_PORT__ -d 'hello friend'
  {
      "processing_time": 5.0067901611328125e-06,
      "queue_time": 0.41274619102478027,
      "result": "HELLO FRIEND"
  }

Could it be that this seemingly innocuous service will be __NEXT_LEVEL__'s downfall?
