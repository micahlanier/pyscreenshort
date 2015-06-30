# pyscreenshort
A simple Python script for making pretty “screenshorts,” “tweet shots,” and “text shots” for social media posting.

## Background
[“Screenshorts”](http://www.buzzfeed.com/charliewarzel/viva-screenshorts) are a popular way to embed “preview” text of articles in social media posts. `pyscreenshort` was inspired by apps and features like [OneShot](http://oneshot.link), [Instapaper](http://instapaper.com), and [Medium](https://medium.com/the-story/text-shots-3f82f2536cc) that make it easy to generate these images on certain devices and services. Though not as straightforward to use, `pyscreenshort` is an experiment in using Python to generate consistent (and hopefully attractive!) images like these. It takes as inspiration Instagram’s attractive formatting, as well as the style used by [The New York Times](https://twitter.com/nytimes/status/614907835252670464) in many of their tweets.

## Usage
Run `screenshort.py` to use. The first input will be used as your image’s primary text. If provided, a second input will be used as the “secondary” text in the lower left corner. An example that will produce a two-line image with secondary text:

```
./screenshort.py \
  $'This is a trial of pyscreenshort.\nIt is a Python project for creating attractive “screenshorts” from whatever text you provide.' \
  micahlanier.github.io/pyscreenshort \
  --bg_color=white \
  --padding=40 \
  --main_text_color=black \
  --main_font_name='Hoefler Text' \
  --main_font_size=32 \
  --secondary_text_color=#999 \
  --output screenshort.png
```

The result of the above will be written to a PNG file. `pyscreenshort` will automatically wrap text where appropriate. To manually include newline characters, use syntax like above (if using bash) or wrap your text in double quotation marks.

Finally, run `screenshort.py -h` for a list of additional formatting options, including image size, colors, and fonts.

**Note**: The current version of this software looks for fonts where they are expected to be found on Mac OS X. Source modification may be necessary for other systems.

## Dependencies
`pyscreenshort` uses several typical Python packages, as well as [Pillow 2.7](https://python-pillow.github.io).
