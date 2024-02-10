# Read this for details and troubleshooting! More has been added

Code to generate deliveroo account.

Clone project onto your machine

Add file api_key.txt file containing just the api key for juicy sms.
https://juicysms.com/myaccount <-- Generate key using this link should be in the account section

type "pip install -r requirements.txt" to install dependencies (no speech marks)

type "python3 deliveroo.py" to run program (no speech marks), once proceess is complete text file will be made with account email and password, along with a chrome window open with the account

If password is not being accepted and you sure it's correct run "safaridriver --enable" (no speech marks) in different terminal

delete lines 146 and 147 once youve run it once and password is accepted

Click close session to when continuing to use safari 