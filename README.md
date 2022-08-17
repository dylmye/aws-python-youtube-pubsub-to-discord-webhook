<!--
title: 'AWS YouTube WebSub to Discord Webhook'
description: 'This template takes go-live events from YouTube WebSub (formerly PubSub), and publishes the events through a Discord webhook.'
layout: Doc
framework: v3
platform: AWS
language: python
authorLink: 'https://github.com/dylmye'
authorName: 'Dylan Myers'
authorAvatar: 'https://avatars1.githubusercontent.com/u/7024578?s=200&v=4'
-->

# Serverless Framework Python YouTube WebSub to Discord Webhook on AWS

This template takes go-live events from YouTube WebSub (formerly PubSub), and publishes the events through a Discord webhook.

## Usage

### Required Parameters

Set these up in the .env file or pass them as parameters in the monitoring display. Remember that if you are auto-deploying from GitHub etc. your .env file will not be available for the script to read from.

* `DISCORD_WEBHOOK_URL`: This is the URL provided by the Discord webhook you have set up
* `DISCORD_ROLE_ID`: If you want to @everyone when you go live, set this to "everyone", otherwise set it to the ID of the Discord role that should be @'d. Default: `'everyone'`
* `INCLUDE_SHORTS_UPLOADS`: Set this to `'False'` if you don't want notifications for YouTube shorts. Default: `'True'`

### Deployment

> Make sure to make your .env file following the .env.example file!

```
$ yarn
$ serverless
```

After creating/selecting an app and deploying to it, you should see output similar to:

```bash
Deploying aws-python-youtube-websub-to-discord-webhook to stage dev (us-east-1)

✔ Service deployed to stack aws-python-youtube-websub-to-discord-webhook-dev (140s)

endpoint: GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/webhook
functions:
  handler: aws-python-youtube-websub-to-discord-webhook-dev-webhook (2.3 kB)
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [httpApi event docs](https://www.serverless.com/framework/docs/providers/aws/events/http-api#jwt-authorizers).

### Invocation

**Prerequisites:**

* 5 minutes of your time

Follow YouTube's guide [here](https://developers.google.com/youtube/v3/guides/push_notifications). In this case, the callback server is this lambda. The Callback URL is the same as the one from the deploy output above. PubSub is now called WebSub, and you can find a bunch of WebSub hubs online (these links are not endorsements, just a few examples):

* [WebSubHub.com](https://websubhub.com/) - free, max subscription period is 10 days
* [Superfeedr](https://superfeedr.com) - unmaintained, free for < 8 subscriptions then $1/8 requests, no max subscription period
* [Google PubSubHubbub Hub](https://pubsubhubbub.appspot.com/) - unmaintained, no permanent subscriptions


### Local development

You can invoke your function locally by using the following command:

```bash
serverless invoke local --function webhook
```

Which should result in response similar to the following:

```
{
  "statusCode": 200,
  "body": "{\n  \"executed\": False,\n}"
}
```

Alternatively, it is also possible to emulate API Gateway and Lambda locally by using `serverless-offline` plugin. In order to do that, execute the following command:

```bash
serverless plugin install -n serverless-offline
```

It will add the `serverless-offline` plugin to `devDependencies` in `package.json` file as well as will add it to `plugins` in `serverless.yml`.

After installation, you can start local emulation with:

```
serverless offline
```

To learn more about the capabilities of `serverless-offline`, please refer to its [GitHub repository](https://github.com/dherault/serverless-offline).

## Credits

This Serverless template is an adaptation of [this Lambda](https://github.com/dylmye/superfeedr-discord) I created in 2021 - please also see the credits section there

This README is shamelessly adapted from [aws-node-http-api](https://github.com/serverless/examples/tree/v3/aws-node-http-api)'s README, written by [Matthieu Napoli](https://github.com/mnapoli) for Serverless.
