#!/usr/local/bin python2.7

"""
Script to run after adding a new blog post to `index.html` to update the rss feed at rss.xml

input: /index.html
output: /rss.xml

new posts have format:
<item>
    <title>This is the most recent entry in my sample feed</title>
    <link>http://webdesign.about.com/rss2.0feed/entry.html</link>
    <description>This is the text that will appear in the feedreaders. It describes the post itself, not the entire feed.</description>
    <guid>http://webdesign.about.com/rss2.0feed/entry.html</guid>
</item>

"""
import os

rss_opening_tags = \
'<?xml version="1.0" encoding="utf-8"?>\n\
<rss version="2.0">\n\
<channel>\n\
    <title>Bitly Science RSS 2.0 Feed</title>\n\
    <link>http://bitlyscience.github.io/</link>\n\
    <description>Exciting things happening at the intersection of science and the world of bitly!</description>\n\n'

rss_closing_tags = \
'</channel>\n\
</rss>'

DIR_NAME, _ = os.path.split(os.path.abspath(__file__))

post_data = []

def parse_html(line):
    link = line.split('"')[1]
    title = line.split('>')[2].split('<')[0]
    description = title # because i'm uncreative...
    
    return title, link, description

def scrape_index_html():
    global post_data
    
    with open(DIR_NAME + '/../index.html') as fh:
        for line in fh:

            if line.startswith('<a href="'):
                post_data.append(parse_html(line))  # time ordered (ie, most recent at top/first)

def build_rss_file():
    fh = open(DIR_NAME + '/../rss.xml','w')
    fh.write(rss_opening_tags)

    for post in post_data:
        title, link, description = post

        fh.write('<item>\n  <title>' + title + '</title>\n')
        fh.write('  <link>' + link + '</link>\n')
        fh.write('  <description>' + description + '</description>\n'  )
        fh.write('</item>\n\n')
    
    fh.write(rss_closing_tags)
    fh.close()
    
if __name__ == "__main__":
    scrape_index_html()
    build_rss_file()
    