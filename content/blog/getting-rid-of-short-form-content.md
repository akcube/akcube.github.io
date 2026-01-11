---
author: Kishore Kumar
date: 2024-06-25 14:25:53+0530
doc: 2024-06-05 05:06:01+0530
title: Getting Rid of Short-Form Content
---
Social media platforms are universally competing to capture all our time and attention by spamming us with brain-rot short form content... and it's working. And unlike other forms of addiction, it's not even true that we get dopamine hits from consuming short form content. More often than not, we don't even realize the amount of time that was passed consuming tidbits of random brain rot. YouTube for example randomly starts on the shorts page and users don't even realize they're scrolling through shorts until much later. Below we'll quickly outline a few software fixes we can implement at the moment to try to purge short form content from our life. Needless to say, if you're an iOS user, please chuck your phone. 
# Instagram Reels
I use Instagram sometimes to view friends' stories and chat once in a while. There are a couple of possible fixes to getting rid of short form content from Instagram mobile. 
## Web + AdBlock
Use only Instagram web. The UI is absolute trash and terrible to use. But you can use an AdBlocker tool to get rid of the reels elements and then it's just a modded Instagram with pretty bad UI. 
## Instander
Use a modded version of Instagram like [Instander](https://thedise.me/instander/). There are a few other mods like AeroInsta, MyInsta, etc. but I personally find Instander to be the most trustworthy among them. They're all closed source but the developer of Instander is pretty well known and trusted in the community. People have also ran network logging experiments to verify that Instander is not performing any extra data espionage or mining activities on the device. Alright, assuming you've uninstalled Instagram and installed Instander, what do we do now? 
1. After logging in, navigate to "Instander Settings", right above the usual Instagram settings button. Go to Developer Mode and enable it. Also on the same screen, click on "Get MobileConfig" and "Update."
2. Restart the app. 
3. Next, return to the home screen of Instander and long press the "Home" (house) icon on the bottom tab. This will enter you into developer options. Navigate to "MetaConfig Settings & Overrides"
4. Search for "panorama v2 variants", you'll find a setting called `panorama v2 variants: reels tab enabled`, turn it off. 
5. Next, search for "panavision nav". At the bottom, you'll see a few settings for specific tabs. You're interested in `tab 1` and `tab 3`.
6. Click on both `tab 1` and `tab 3` and set their value to `news`. Note that I want to turn off both explore and the reels tab. If you want to keep explore for some reason you can leave it as is.
7. Restart the app.
And we're done. There's still "Suggested reels" that sometimes pops into your primary feed when scrolling. It's annoying, but infinitely easier to notice and avoid compared to just clicking on something via explore. I do not know of any solution / fix to remove that from your feed. If anyone does know a solution to that then please let me know.
### Disclaimer
Using modded Instagram can possibly get your account blocked by Instagram. But I know many people & entire Reddit communities who have used these apps for years without issues. Worst case you can probably appeal and get your account back. Worst-worst case you can get rid of Instagram. Win-win situation. 
# YouTube Shorts
## Mobile
The easiest fix is through ReVanced Manager. 
1. Install [ReVanced](https://revanced.app/). 
2. Go to Patcher > Select an App
3. Search for "YouTube"
4. Click on the inner `Suggested: vXX.XX.XX` button
5. Install the `nodpi` version from a source like ApkMirror
6. Launch patched YouTube. Install MicroG and sign in when it prompts you to.
7. And we now have better YouTube. We need to get rid of the original YouTube now. There are two options.
	1. Disable it using system settings
	2. Use `adb` to uninstall it. 
## Desktop 
Just install one of the many YouTube feed / shorts blockers from the chrome web store. I use [ShortsBlocker](https://chromewebstore.google.com/detail/shortsblocker-remove-shor/oahiolknhkbpcolgnpljehalnhblolkm?hl=en). 

# TikTok
Easy fix. Uninstall. There's literally no point of having this app. 
