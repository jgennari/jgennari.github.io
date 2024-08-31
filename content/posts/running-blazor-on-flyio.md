---
title: "Running Blazor on Fly.io"
date: 2024-08-24T10:36:56-04:00
draft: false
tags: ["csharp","blazor","hosting"]
author: "Me"
categories: ["Tech"]
---

I've been running a Blazor app on Heroku for a bit, but I decided to give [Fly.io](https://fly.io) a try. Aside from the ease of deployment through their CLI, they boast some pretty cool, zero-configuration global deployment benefits:

> Over 3 million apps have launched on Fly.io, boosted by global Anycast load-balancing, zero-configuration private networking, hardware isolation, and instant WireGuard VPN connections. Push-button deployments that scale to thousands of instances.

Since .NET Core 1.0 first release in 2016, Microsoft has made a Docker image available for the .NET runtime, making composing Docker containers and running .NET application a breeze. This has made hosting on services that support Docker (like Heroku and Fly) a breeze. To get started, you need `Dockerfile` in your project folder. Simply change the `AppName.dll` to match your executable name. I'm also running .NET 9.0 preview builds, so adjust accordingly.

```docker
# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/dotnet/nightly/sdk:9.0-preview AS build-env
WORKDIR /app
    
# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore
    
# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o out
    
# Build runtime image
FROM mcr.microsoft.com/dotnet/nightly/aspnet:9.0-preview
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "AppName.dll"]
```

### Deploying to Fly.io

Once you have your `Dockerfile`, you can deploy to Fly.io. Follow their guide to install [flyctl](https://fly.io/docs/flyctl/install/). Configuring a new app, flyctl will auto-generate a `fly.toml` file:

```toml
app = 'appname'
primary_region = 'mia'

[build]

[http_service]
  internal_port = 5000
  force_https = false
  auto_stop_machines = 'stop'
  auto_start_machines = true
  min_machines_running = 1
  processes = ['app']

[[vm]]
  memory = '2gb'
  cpu_kind = 'shared'
  cpus = 4

[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/"

[env]
  HTTP_PORT = "5000"
  METRICS_PORT = "9091"
  ASPNETCORE_ENVIRONMENT = "Production"
  #other config values
```

Once you've configured your app, you can just use `fly deploy` and flyctl will build your Docker container and deploy it to all of your machines. Depending on your regions, Fly will use a rolling deployment strategy to make sure you don't have any downtime.

### Environment Variables

If you're not familiar with Docker-based cloud deployment, configuration variables and secrets are typically deployed as environment variables. In the case of Fly, you can either store them in you `fly.toml` or in your dashboard:

![Image 0](../../images/running-blazor-on-flyio_1724511530452.png)  

In your application, you can access your environment variables using the following code, which will look for an environment variable first, then check your `appsettings.json` or `appsettings.{environment}.json`. 

```csharp
builder.Configuration.GetValue<string>("METRICS_PORT");
```

If you have configuration stored in `appsettings.json`, you can use double underscores (e.g. `__`) to access nested values. For instance, to access your AWS profile setting:

```json
"AWS": {
    "Profile": "r2",
}
```

You would use:

```csharp
builder.Configuration.GetValue<string>("AWS__PROFILE");
```

Which means in your `fly.toml` you can set an environment variable as `AWS__PROFILE`. 

### A Sticky Situation

One problem I haven't quite solved yet, as it relates to Blazor, is that the Blazor server backend requires clients in a load balanced environment to be "sticky", or in other words, always responding to the machine they originally connect to. Fly.io doesn't officially support sticky sessions, but they do have some cookies and headers that will direct a request to a specific server, but it has some [problems](https://community.fly.io/t/503-using-fly-machine-id-cookie/21430). In another post I'll show you how I implemented middleware to set that cookie.

In the meantime, I've limited my deployment to a single machine.

### Metrics

Fly.io supports Prometheus metrics for your application, giving you insights into how you're utilizing your infrastructure. You can also feed custom metrics from your application into Prometheus and display them on the Grafana dashboard. I'm using OpenTelemetry which has some really cool built-in metrics for the ASP.NET hosting process. Here are the NuGet packages I'm referencing:

```xml
<PackageReference Include="OpenTelemetry.Exporter.Console" Version="1.9.0" />
<PackageReference Include="OpenTelemetry.Exporter.Prometheus.AspNetCore" Version="1.9.0-beta.2" />
<PackageReference Include="OpenTelemetry.Extensions.Hosting" Version="1.9.0" />
<PackageReference Include="OpenTelemetry.Instrumentation.AspNetCore" Version="1.9.0" />
<PackageReference Include="OpenTelemetry.Instrumentation.Hangfire" Version="1.6.0-beta.1" />
<PackageReference Include="OpenTelemetry.Instrumentation.Http" Version="1.9.0" />
<PackageReference Include="OpenTelemetry.Instrumentation.Process" Version="0.5.0-beta.6" />
<PackageReference Include="OpenTelemetry.Instrumentation.Runtime" Version="1.9.0" />
```

Then I configure the Prometheus scraping endpoint using a non-public port:

```csharp
app.UseOpenTelemetryPrometheusScrapingEndpoint(context => 
    context.Connection.LocalPort == Int32.Parse(envVarMetricsPort) &&
    context.Request.Path == "/metrics");
```

And finally adding this to my `fly.toml` to make Fly aware of that endpoint:

```toml
[metrics]
  port = 9091
  path = "/metrics"
```

And voila, ASP.NET hosting metrics in your Grafana dashboard:

![Image 1](../../images/running-blazor-on-flyio_1724512742188.png)

In a future post I'll show you how to write your own custom metrics!

### Conclusion

In conclusion, deploying a Blazor app on Fly.io offers several benefits, including ease of deployment, global deployment capabilities, and zero-configuration private networking. By following the steps outlined in this guide, you can successfully deploy your Blazor app on Fly.io using Docker containers. Additionally, you can leverage environment variables for configuration and take advantage of Fly.io's support for Prometheus metrics to gain insights into your application's performance. With these tools and techniques, you can confidently host your Blazor app on Fly.io and take advantage of its powerful features. Happy coding!