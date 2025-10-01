Mirror of articles in the text edition of the Christian Science Monitor in the [particle](https://browser.particlestudios.eu/#particle-formatting) web format, to be used in the [Constellation browser](https://browser.particlestudios.eu) for the [Playdate console](https://play.date).

- Watch for updates from the CSM [RSS feed[(https://rss.csmonitor.com/feeds/all)
- Every story has a text version accessible by adding `/text_edition` in the url after `www.csmonitor.com`; for example the text version of `https://www.csmonitor.com/World/Middle-East/2025/0930/palestinian-reaction-trump-gaza-ceasefire-plan` is found at `https://www.csmonitor.com/text_edition/World/Middle-East/2025/0930/palestinian-reaction-trump-gaza-ceasefire-plan`
- The text version has a very simple structure that is easy to parse. Parse the HTML and convert it into the particle format for display on the Constellation browser for playdate.
- Package everything up as a GitHub action cron job that runs at 6am PT every day and produces the resulting json files on the project site on GH pages.
