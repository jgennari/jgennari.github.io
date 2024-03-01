---
title: "Submitting an Unraid Community App"
date: 2024-03-01T12:03:20-05:00
draft: false
tags: ["docker","unraid"]
author: "Me"
category: ["Tech"]
series: ["Build with Me"]
---

In a previous post I created a docker container for Goatcounter, a privacy-friendly analytics service. I wanted to submit it to the Unraid Community Apps repository so that others could easily install it. This post will cover the process of submitting a new app to the Unraid Community Apps repository. The first step I took was to install the docker container from Docker Hub. To do this, you can use the "Click Here To Get More Results From DockerHub" link. 

![Image 0](../../images/submitting-unraid-community-app_1709312715869.png)  

Now the image I created earlier is available:

![Image 1](../../images/submitting-unraid-community-app_1709312781911.png)  

Community Apps will try and discover the ports and volumes that the container uses. In this case, it was able to find the port and volume that I had set up.

![Image 2](../../images/submitting-unraid-community-app_1709312833050.png)  

From here, Unraid drops you to the docker creation screen. I filled out the port and volume settings I needed and hit Apply. This allowed me to test the container and make sure it was working as expected.

From here I followed Squid's instructions on this [thread](https://forums.unraid.net/topic/57181-docker-faq/#comment-566084) to submit the app. You'll need to generate an XML file based on the container you just created. To do that, you need to follow a few steps:

1. Turn Docker off under Settings -> Docker
2. Turn on Docker Creation mode 
3. Turn Docker back on
4. Go to the Docker tab and click Add Container
5. Use the existing container as a template
6. Fill out the defaults and click Save

You'll be presented a text box with some XML in it. You'll need to save that XML and make it available in a new Github [repository](https://github.com/jgennari/UnraidApps). 

> ⚠️ It's important to note that this needs to be a separate repository from the container itself. This repository can store multiple Community Apps as well as your developer profile.

From here it's mostly social work to get the app published. You'll need to reach out to Squid with a link to your XML repository. You'll also need to create a support thread on the Unraid forums, and then update your XML with that URL.