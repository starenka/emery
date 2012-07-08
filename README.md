# WTF?

Emery is a simple wrapper on top of requests, pyquery, beautifulsoup and tablib which simplifies basic web page scraping. Did you ever bumped into a webpage containing precious data you desperatly needed to get as CSV? Get all links? Yes, you can easily make this using libraries mentioned above or with Python's stdlib. But why bother?

## Installing

    pip install git+git://github.com/starenka/emery.git

## Usage

Usage is quite straigtforward. Check it for yourself. First, fetch the page (or just supply html via html kwarg):

    >>> from emery import Page
    >>> p = Page(url='http://icanhascheezburger.com/')

HTML is not so cool to read, is it?

    >>> p.text
    u'<![endif] PHI Consolidated Theme: 2012.06.08.2 generated 233 seconds ago\n\tgenerated in ... [truncated]

Now something more funny - harvest all links

    >>> p.links[:10]
    [('', 'http://cheezburger.com/'), ('I Can Has Cheezburger?', 'http://icanhascheezburger.com'),
    ('FAIL Blog', 'http://failblog.org'), ('Memebase', 'http://memebase.com'),
    ('The Daily What', 'http://thedailywh.at'), ('Know Your Meme', 'http://knowyourmeme.com/?utm_source=blue&utm_medium=web&utm_campaign=blue'),
    ('LOLmart', 'http://lolmart.com'), (u'All Sites \xbb', 'http://cheezburger.com/'),
    ('ICHC', 'http://icanhascheezburger.com'), ('Lolcats', 'http://lolcats.icanhascheezburger.com/')]

or use a selector to filter'em a bit.

    >>> p.get_links('a[href*="cheez"]')[:10]
    [('', 'http://cheezburger.com/'), ('I Can Has Cheezburger?', 'http://icanhascheezburger.com'),
    (u'All Sites \xbb', 'http://cheezburger.com/'), ('ICHC', 'http://icanhascheezburger.com'),
    ('Lolcats', 'http://lolcats.icanhascheezburger.com/'), ('Loldogs', 'http://dogs.icanhascheezburger.com'),
     ('Animals', 'http://justcapshunz.icanhascheezburger.com'), ('Gifs', 'http://gifs.icanhascheezburger.com'),
     ('Squee!', 'http://squee.icanhascheezburger.com'), ('Memes', 'http://memes.icanhascheezburger.com')]

I CAN HAS IMAGES TOO?

    >>> p.images[:10]
    [(None, 'http://s0.wp.com/wp-content/themes/vip/cheezcommon2/images/CheezburgerBadge.png?m=1341286124g'),
    (None, 'http://s0.wp.com/wp-content/themes/vip/cheezcommon2/images/ajax-loader.gif?m=1286129087g'),
    (None, 'http://icanhascheezburger.files.wordpress.com/2012/07/funny-pictures-animal-gifs-the-internet-summarized.gif?w=95&h=95&crop=1'),
    (None, 'http://icanhascheezburger.files.wordpress.com/2012/07/funny-pictures-what-meow-means2.jpg?w=95&h=95&crop=1'),
    (None, 'http://icanhascheezburger.files.wordpress.com/2012/07/funny-pictures-animal-capshunz-sloth-logic.jpg?w=95&h=95&crop=1'),
    (None, 'http://icanhascheezburger.files.wordpress.com/2012/07/funny-pictures-lolcats-literary-road-rage.jpg?w=95&h=95&crop=1'),
    (None, 'http://s.chzbgr.com/s/release_20120319.1/Images/OnoOptin/opt_in_ichc_option3.jpg'),
    ('funny pictures - Last Pack Before I Quit.  I Swear.', 'http://icanhascheezburger.files.wordpress.com/2012/07/funny-pictures-last-pack-before-i-quit-i-swear1.jpg'),
    ('funny pictures - Lead the Way!', 'http://icanhascheezburger.files.wordpress.com/2012/07/funny-pictures-lead-the-way.jpg'),
    ('advice animals memes  - Animal Memes: Lawyer Dog: Fixing to Retire Soon', 'http://icanhascheezburger.files.wordpress.com/2012/07/advice-animals-memes-lawyer-dog-fixing-to-retire-soon.jpg')]

How about tables? Everybody loves tables. Get them all as tablib objects

    >>> p = Page(url='http://www.nuforc.org/webreports/ndxe201206.html')
    >>> p.tables
    [<dataset object>]

which you can represent as a list of tuples

    >>> list(p.tables[0])[:5]
    [('6/30/12 00:00', 'Kansas City', 'MO', 'Cigar', 'over1 and a half hours', 'Five cigar shape images going in circles above our neighbor hood.', '7/4/12'), ('6/30/12 00:00', 'Kansas City', 'MO', 'Cigar', 'over1 and a half hours', 'Five fast.cigar shape images going in circles above our neighbor hood.', '7/4/12'), ('6/30/12 23:50', 'Bremerton', 'WA', 'Oval', '30 seconds', 'Kitsap county ufo sighting', '7/4/12'), ('6/30/12 23:30', 'Blaine', 'WA', 'Light', '2 minutes', 'Orange lights over Drayton Harbor', '7/4/12'), ('6/30/12 23:00', 'Monroe', 'MI', 'Sphere', '1-2 minutes', 'Orange ufo sighted in Monroe near I-75', '7/4/12')]

or JSON (,CSV, XLS etc.)

    >>> p.tables[0].json
    '[{"Date / Time": "6/30/12 00:00", "City": "Kansas City", "State": "MO", "Shape": "Cigar", "Duration": "over1 and a half hours", "Summary": "Five cigar shape images going in circles above our neighbor hood.", "Posted": "7/4/12"}, {"Date / Time": "6/30/12 00:00", "City": "Kansas City", "State": "MO", "Shape": "Cigar", "Duration": "over1 and a half hours", "Summary": "Five fast.cigar shape images going in circles above our neighbor hood.", "Posted": "7/4/12"}, {"Date / Time": "6/30/12 23:50", "City": "Bremerton", "State": "WA", "Shape": "Oval", "Duration": "30 seconds", "Summary": "Kitsap county ufo sighting", "Posted": "7/4/12"}, {"Date / Time": "6/30/12 23:30", "City": "Blaine", "State": "WA", "Shape": "Light", "Duration": "2 minutes", "Summary": "Orange lights over Drayton Harbor", "Posted": "7/4/12"}, {"Date / Time": "6/30/12 23:00", "City": "Monroe", "State": "MI", "Shape": "Sphere", "Duration": "1-2 minutes", "Summary": "Orange ufo sighted in Monroe near I-75", "Posted": "7/4/12"}, {"Date / Time": "6/30/12 23:00", "City": "Niles", "State": "OH", "Shape": "Changing", "Duration": "One minute", "Summary": "Square box in shape color red to orange, shape changed from square to circle color red to yellow.", "Posted": "7/4/12"}, ... [truncated]

Remember, you can use get_* methods to filter links, images or tables.

## TODO
- docs
- .text should ignore JavaScript and friends
- more features
- cleanup
