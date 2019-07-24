# GW2-Market-Analysis
Backend, gather market information from GW2 api and perform predictive analysis

At the moment the test_api_call_json.py file creates local databases containing information on all items, listed items, bank items,
materials storage items, and inventory items across all characters.

To access any of this information an API key is needed. When test_api_call_json.py is run it will prompt you for an API key. 
After you enter it, you may choose to update all databases, or just the ones needed to update the owned database.

NOTE: The all items, and listed items databases will take a fairly long time to create and update. A timer has been added
to ensure that they don't update more than once a week. This can be overridden when prompted, and is done automatically when 
the option to update owned databases is chosen.
