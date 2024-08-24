---
title: "Blazor Magic Link"
date: 2024-08-21T18:33:25-04:00
draft: false
tags: ["c#","blazor","programming"]
author: "Me"
category: ["Tech"]
---

I wanted a quick Magic Link implementation for my Blazor app, so I cobbled together a solution. I took inspiration from a NuGet package (forgot which one), but it's simple enough to do with a few methods.

#### Generating the Magic Link

When a user decides to log in with a magic link, you can call a method like this. I'm loading a lot of the email server config elsewhere in the service.

```csharp
public async Task<string?> GenerateMagicLinkAsync(string userId)
{
    var token = GenerateToken(userId); // the actual encoded JWT token
    var baseUrl = _options.MagicLinkBaseUrl; // the base URL of the app stored in config
    var magicLink = $"{baseUrl}?i={token}"; // the magic link formatted for the controller
    
    var user = await userManager.FindByEmailAsync(userId); // get the email address of the userId
    
    var email = new MimeMessage();
    email.To.Add(new MailboxAddress("", user.Email));
    email.From.Add(new MailboxAddress(_options.EmailFromName, _options.EmailFromAddress));
    email.Subject = "Login";
    email.Body = new TextPart("html") { Text =  $"Click the following link to sign in: <br/><a href=\"{magicLink}\">{magicLink}</a>" };

    using var client = new SmtpClient(); // load the details fo the SMTP server from config
    await client.ConnectAsync(_options.MailServer, _options.MailPort, _options.MailUseSsl);
    await client.AuthenticateAsync(_options.MailUsername, _options.MailPassword);
    await client.SendAsync(email);
    await client.DisconnectAsync(true);

    return magicLink;
}
```

So the magic piece of the magic link is a JWT token which signs the information about the authentication and the user with a secret key specific to your app:

```csharp
public string GenerateToken(string userId)
{
    var secretKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_options.SecretKey)); // secret key to decode the JWT
    var signingCredentials = new SigningCredentials(secretKey, SecurityAlgorithms.HmacSha256);
    var claims = new List<Claim> { new Claim(ClaimTypes.NameIdentifier, userId) };

    var tokenDescriptor = new SecurityTokenDescriptor
    {
        Issuer = _options.Issuer,
        Audience = _options.Audience,
        Expires = DateTime.UtcNow.AddMinutes(_options.TokenExpirationMinutes),
        SigningCredentials = signingCredentials,
        Claims = claims.ToDictionary(c => c.Type, c => (object)c.Value),
        IssuedAt = DateTime.UtcNow,            
    };

    var tokenHandler = new JwtSecurityTokenHandler();
    var securityToken = tokenHandler.CreateToken(tokenDescriptor);
    return tokenHandler.WriteToken(securityToken);
}
```

When the user clicks the magic link, the app responds from this minimal API in `program.cs`:

```csharp
app.Map("/token", async (HttpContext context, MagicLinkService magicLink, string i) =>
{
    if (await magicLink.ValidateMagicLinkAsync(i))
        context.Response.Redirect("/");
    else
        context.Response.Redirect("/login");
}).DisableAntiforgery();
```

And from there, we pass the token into the `ValidateToken` method (below) and if it's valid, I'm using the `FindByEmailAsync` method to sign the user in 

```csharp
public async Task<bool> ValidateMagicLinkAsync(string token)
{
    using (var scope = _serviceProvider.CreateScope())
    {
        var userManager = scope.ServiceProvider.GetRequiredService<UserManager<ApplicationUser>>();
        var signinManager = scope.ServiceProvider.GetRequiredService<SignInManager<ApplicationUser>>();

        var isValid = ValidateToken(token, out string? email);
        if (isValid && email != null)
        {
            var user = await userManager.FindByEmailAsync(email);
            if (user != null)
            {
                await signinManager.SignInAsync(user, true);
                return true;
            }
        }
        return false;
    }
}
```

From there, we call the `ValidateToken` method to cryptographically decrypt the JWT and validate if it's valid.

```csharp
public bool ValidateToken(string token, out string? email)
{
    email = null;
    var tokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ClockSkew = TimeSpan.Zero,
        ValidIssuer = _options.Issuer,
        ValidAudience = _options.Audience,
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_options.SecretKey))
    };

    var tokenHandler = new JwtSecurityTokenHandler();
    try
    {
        var principal = tokenHandler.ValidateToken(token, tokenValidationParameters, out _);
        email = principal.Claims.FirstOrDefault(c => c.Type == ClaimTypes.NameIdentifier)?.Value;
        return !string.IsNullOrEmpty(email);
    }
    catch /*(Exception ex)*/
    {
        return false;
    }
}
```

#### Conclusion

In conclusion, implementing a Magic Link authentication feature in a Blazor app can be achieved by generating a JWT token as the magic link, sending it via email, and validating it when the user clicks the link. The `GenerateMagicLinkAsync` method generates the magic link and sends it to the user's email using SMTP. The `GenerateToken` method creates a JWT token with the necessary claims and signing it with a secret key. The minimal API in `program.cs` handles the redirection based on the validity of the magic link. The `ValidateMagicLinkAsync` method validates the token and signs in the user if it's valid. Finally, the `ValidateToken` method decrypts and validates the JWT token. With these components in place, you can provide a seamless and secure authentication experience for your Blazor app users.