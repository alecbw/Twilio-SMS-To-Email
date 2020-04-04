import logging
import json
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3

## NOTE: SES not available in us-west-1. I use us-west-2 for SES

def lambda_handler(event, context):
    param_dict, missing_params = validate_params(
        event,
        # required_params=["ToCountry", "ToState", "SmsMessageSid", "FromZip", "FromState", "FromCity", "From", "Body"],
        required_params=["Tocountry", "Tostate", "Smsmessagesid", "Fromzip", "Fromstate", "Fromcity", "From", "Body"],

    )
    # Add newlines for readability in the eventual email
    # param_dict = {k:(v + "\t\n") for k,v in param_dict.items()}
    param_dict["From"] = param_dict["From"].replace("%2B", "")
    param_dict["Body"] = param_dict["Body"].replace("+", " ")

    invocation_dict = {
        "Subject": f"Received SMS: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}",
        "Body": json.dumps(param_dict),
        "Recipients": ["alec@contextify.io"]
    }



    request_data, request_status = invoke_lambda(
        invocation_dict,
        "contextify-serverless-prod-send-email",
        "RequestResponse"
    )
    logging.info(request_data, request_status)

        # response = boto3.client("ses", region_name="us-west-2").send_email(
    #     Source="hello@contextify.email",
    #     ReplyToAddresses=["hello@contextify.email"],
    #     Destination={"ToAddresses": invocation_dict["Recipients"]},
    #     Message={"Subject": {"Data": invocation_dict["Subject"]}, "Body": {"Text": {"Data": invocation_dict["Body"]}}},
    # )

    # logging.info(response)


######################## Standard Lambda Helpers ################################################


def validate_params(event, required_params, **kwargs):
    event = standardize_event(event)
    commom_required_params = list(set(event).intersection(required_params))
    commom_optional_params = list(set(event).intersection(kwargs.get("optional_params", [])))

    param_only_dict = {k: v for k, v in event.items() if k in required_params + kwargs.get("optional_params", [])}
    logging.info(f"Total param dict: {param_only_dict}")
    logging.info(f"Found optional params: {commom_optional_params}")

    if commom_required_params != required_params:
        missing_params = [x for x in required_params if x not in event]
        return param_only_dict, missing_params

    return param_only_dict, False


def standardize_event(event):
    if "body" in event:  # POST, synchronous API Gateawy
        body_dict = {x[0]:x[1] for x in [x.split("=") for x in event["body"].split("&")]}
        event = {**event, **body_dict}
    elif "queryStringParameters" in event:  # GET, synchronous API Gateway
        event.update(event["queryStringParameters"])
    elif "query" in event:  # GET, async API Gateway
        event.update(event["query"])

    result_dict = {
        k.title().strip().replace(" ", "_"):(False if v == "false" else v)
        for (k, v) in event.items()
    }
    return result_dict


def invoke_lambda(params, function_name, invoke_type):

    lambda_client = boto3.client("lambda")
    lambda_response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType=invoke_type,
        Payload=json.dumps(params),
    )
    # Async Invoke returns only StatusCode
    if invoke_type.title() == "Event":
        return None, lambda_response.get("StatusCode", 666)

    string_response = lambda_response["Payload"].read().decode("utf-8")
    json_response = json.loads(string_response)

    if not json_response:
        return "Unknown error: no json_response. Called lambda may have timed out.", 500
    elif json_response.get("errorMessage"):
        return json_response.get("errorMessage"), 500

    status_code = int(json_response.get("statusCode"))
    json_body = json.loads(json_response.get("body"))

    if json_response.get("body") and json_body.get("error"):
        return json_body.get("error").get("message"), status_code

    return json_body["data"], status_code

