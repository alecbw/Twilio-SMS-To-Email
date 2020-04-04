# Related article
https://www.alec.fyi/setup-email-sending-for-anything.html

# Using this


This repo uses the serverless.com Infrastructure-as-code platform (which itself wraps AWS CloudFormation).

To create a CloudFormation Stack (and also subsequently update it), use:

``` 
sls deploy
```

It will be called `send-email-prod` (you can edit this in the serverless.yml)


You can test the Lambda locally (be aware it does send an actual email) with:

```
sls invoke local -f send-email -d '{"Recipients":["recipient@your-domain.com"], "Subject":"CLI Test", "Body":"testing 1 2 3"}'
```

To take down the CloudFormation Stack and associated Lambda, use:

```
sls remove
```
