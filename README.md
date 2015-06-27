# pyscreenshort
A simple Python script for making pretty “screenshorts” for social media posting.

## Background
[“Screenshorts”](http://www.buzzfeed.com/charliewarzel/viva-screenshorts) are a popular way to embed “preview” text of articles in social media posts. `pyscreenshort` was inspired by apps like [OneShot](http://oneshot.link) and [Instapaper](http://instapaper.com) that make it easy to generate these images on mobile devices. `pyscreenshort` provides consistent (and hopefully attractive!) formatting of text that is not dependent on screenshots or saving articles. It takes as inspiration Instagram’s attractive formatting, as well as the style used by [The New York Times](https://twitter.com/nytimes/status/614907835252670464).

## Usage
Run `screenshort.py` to use. The first input will be used as your image’s primary text. If provided, a second input will be used as the “secondary” text in the lower left corner. An example that will produce a two-line image with secondary text:

```
./screenshort.py $'This is line 1.\nThis is line 2.' 'This is my secondary text.'
```

`pyscreenshort` will automatically wrap text where appropriate. To include newline characters, use syntax like above (if using bash) or wrap your text in double quotation marks.

Finally, run `screenshort.py -h` for a list of additional formatting options, including image size, colors, and fonts.

**Note**: The current version of this software looks for fonts where they are expected to be found on Mac OS X. Source modification may be necessary for other systems.

## Dependencies
`pyscreenshort` uses several typical Python packages, as well as [Pillow 2.7](https://python-pillow.github.io).
