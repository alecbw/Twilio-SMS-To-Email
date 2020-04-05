# Related article

https://github.com/alecbw/Twilio-SMS-To-Email-www.alec.fyi

# Using this

clone this Github repo

```bash
git clone git@github.com:alecbw/Twilio-SMS-To-Email-www.alec.fyi.git
```
(rename the top level directory to be whatever you want)

(optional) change variable names in `serverless.yml`

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

deploy the stack (_change NAMEOFTOPLEVELDIRECTORY_)
```bash
cd NAMEOFTOPLEVELDIRECTORY && sls deploy
```
