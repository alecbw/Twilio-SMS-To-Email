# Related article

https://github.com/alecbw/Twilio-SMS-To-Email-www.alec.fyi

# Using this

\#2.1 - clone the [Github repo](https://github.com/alecbw/Twilio-SMS-To-Email-www.alec.fyi)

```bash
git clone git@github.com:alecbw/Twilio-SMS-To-Email-www.alec.fyi.git
```
(rename the top level directory to be whatever you want)

\#2.2 - (optional) change variable names in `serverless.yml`

You can keep the defaults or change the service (CloudFormation stack) name, AZ region, and function name and API endpoint path
```yaml
service: public-facing
... truncated...
provider:
    region: us-west-1
... truncated...
functions:
  twilio-webhook:
    handler: twilio_webhook_handler.lambda_handler
    events:
      - http:
          path: /twilio_webhook
          method: post
```

\#2.3 - deploy stack (_change NAMEOFTOPLEVELDIRECTORY_)
```bash
cd NAMEOFTOPLEVELDIRECTORY && sls deploy
```
