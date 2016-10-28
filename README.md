# CodeNinja        [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

CodeNinja is a slack-bot created during HackTREC 2016, as a step towards increasing an individual's productivity.

# Screenshots

<img src="https://raw.githubusercontent.com/GurpreetSK95/CodeNinja/master/Screenshots/Screen%20Shot%202016-10-21%20at%2010.54.02%20AM.png" width="800">

# Usage

##### Generate the slack api token for your bot
You can generate an api token on slack web api page.

Then you need to configure the SLACK_TOKEN in a python module config.py

##### config.py:

``` 
SLACK_TOKEN = '<your-api-token>' 
````

Run print_bot_id.py to generate your bot id

##### config.py:

```
BOT_ID = '<your-id-here>'
```
### NOTE: Change your bot name in ``` print_bot_id.py ``` and ``` codeNinja.py ```

# License

``` 
Copyright (C) 2016 Gurpreet Singh

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. 
```
