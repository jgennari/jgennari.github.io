---
title: "Create a Custom Prometheus .NET Meter"
date: 2024-08-25T21:36:04-04:00
draft: false
tags: ["csharp","metrics"]
author: "Me"
category: ["Tech"]
---

In a previous post I showed you how to add Prometheus metrics to a Blazor app on Fly.io using the OpenTelemetry NuGet packages. Fly makes capturing and displaying metrics simple with their built in Grafana dashboards. But sometimes there are events and metrics from the application layer that you'd like to track, such as how many views a particular piece of content got. Here I've created `InstrumentationService.cs` which I can easily inject into any Blazor component in order to increment a counter:

```csharp
using System.Diagnostics;
using System.Diagnostics.Metrics;

public class InstrumentationService : IDisposable
{
    internal const string ActivitySourceName = "Movment";
    internal const string MeterName = "Movment";
    private readonly Meter meter;

    public InstrumentationService()
    {
        string? version = typeof(InstrumentationService).Assembly.GetName().Version?.ToString();
        this.ActivitySource = new ActivitySource(ActivitySourceName, version);
        this.meter = new Meter(MeterName, version);
        this.VideoViews = this.meter.CreateCounter<long>("video.views", description: "The views from any video");
        this.VideoViews.Add(1);
    }

    public ActivitySource ActivitySource { get; }

    public Counter<long> VideoViews { get; }

    public void Dispose()
    {
        this.ActivitySource.Dispose();
        this.meter.Dispose();
    }
}
```

The important bit here is the `meter`, which can store any number of counters, histograms or gauges, including the `VideoView` counter I've created:

![Image 0](../../images/custom-prometheus-dotnet-meter_1724636952485.png)  

And then in the `program.cs` file, I make sure we add that service to DI:

```csharp
builder.Services.AddSingleton<InstrumentationService>();
```

Also in the `program.cs` I'm adding all the standard ASP.NET instrumentation, plus my custom meter in `InstrumentationService.cs`:

```csharp
builder.Services.AddOpenTelemetry()
    .WithMetrics(builder => builder
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddRuntimeInstrumentation()
        .AddProcessInstrumentation()
        .AddMeter(InstrumentationService.MeterName)
        .AddPrometheusExporter());
```

Then, when I need to increment a counter in a Razor component, I can inject the service:

```razor
@inject InstrumentationService Instrumentation
```

And simply call the AddMethod on the VideoViews counter:

```csharp
Instrumentation.VideoViews.Add(1);
```

And in your Grafana instance, you can create a new dashboard referencing that metric:

![Image 1](../../images/custom-prometheus-dotnet-meter_1724637521535.png)  

#### Conclusion

In conclusion, adding custom Prometheus metrics to a .NET application is straightforward. By creating an `InstrumentationService` and injecting it into Blazor components, you can easily track events and metrics at the application layer. With Grafana dashboards, you can visualize and analyze the collected data, gaining valuable insights into your application's performance.