---
title: "Blazor Authentication Without Razor Pages"
date: 2024-08-23T18:00:02-04:00
draft: false
tags: ["c#","blazor","programming","authentication"]
author: "Me"
category: ["Tech"]
---

For a while now I've been using the standard ASP.NET authentication methods with customized Razor pages to match the style of my site. And while this works, it's annoying to lose all the functionality of Blazor, especially when you pour hours of time into customizing the look-and-feel, only to need to recreate it in the Razor page.

In short, the special sauce is a minimal API method hat accepts a `POST` form-encoded username and password, which I called `internal_login`:

```csharp
app.MapPost("/internal_login", async (HttpContext context, 
    SignInManager<ApplicationUser> signinManager, 
    UserManager<ApplicationUser> userManager) =>
{
    if (context.Request.Host.Host != "localhost") // don't allow external access
        return Results.BadRequest($"Unauthorized login attempt");
        
    var form = await context.Request.ReadFormAsync();
    var username = form["username"];
    var password = form["password"];

    if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password))
        return Results.Unauthorized();

    var user = await userManager.FindByEmailAsync(username);
    if (user != null && await signinManager.PasswordSignInAsync(user, password, true, false) == Microsoft.AspNetCore.Identity.SignInResult.Success)
        return Results.Ok();
    else 
        return Results.Unauthorized();
}).DisableAntiforgery();
```

Some things to note here:

* This code is only accepting calls from inside the application (although this probably isn't correct, I'll need to come back to make it more secure)
* I'm using the PasswordSignInAsync call to determine if the username and password provided is correct. 
* I had to disable antiforgery on this specific request because this wasn't coming from the users browser.

### Authenticating in Blazor

Ok in back in Blazor-land, once our user has entered their username and password, we need to check authenticate the user and set the ASP.NET auth cookie. 

```csharp
var httpClient = new HttpClient();
var content = new FormUrlEncodedContent(new[]
{
    new KeyValuePair<string, string>("username", email),
    new KeyValuePair<string, string>("password", password)
});
var response = await httpClient.PostAsync("http://localhost:5000/internal_login", content);
var cookies = response.Headers.GetValues("Set-Cookie");
var auth = cookies.FirstOrDefault(c => c.StartsWith(".App.Auth=")); //custom name from program.cs

if (auth != null)
{
    var authToken = auth.Split('=')[1].Split(';')[0];
    await JSRuntime.InvokeVoidAsync("setCookie", ".Movment.Auth", authToken, 7);
    NavigationManager.NavigateTo(Redirect ?? "/", true);
}
```

In the `program.cs` file, we can set some saner defaults since we won't be using the standard auth:

```csharp 
//app.UseAuthentication(); //otherwise .NET will load all the authentication junk to the front end

builder.Services.ConfigureApplicationCookie(options =>
{
    options.LoginPath = new PathString("/login"); //otherwise .NET redirects to /Account/Login
    options.ReturnUrlParameter = "redirect";
    options.Cookie.Name = ".App.Auth";
});
```

### Logging Out

Once your user is authenticated and their cookie is set, you can call this other minimal API to log them out and invalidate their cookie:

```csharp
app.Map("/logout", async (HttpContext context, SignInManager<ApplicationUser> signinManager) =>
{
    await signinManager.SignOutAsync();
    context.Response.Redirect("/login");
}).DisableAntiforgery();
```

You can call this from anywhere in your Blazor app using the `NavManager.NavigateTo("/Logout", forceLoad: true);` method. The `forceLoad` will force a complete refresh of the browser.

### Conclusion

And that's it! You've ditched all the legacy Razor pages and you can authenticate right from Blazor code! I came about this solution because I was trying to implement a basic Magic Link solution, [which I wrote about here]({{< ref "/posts/blazor-magic-link" >}} "About Us").