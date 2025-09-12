# File: views.py
# Author: Dawson Maska (dawsonwm@bu.edu), 9/9/2025
# Description: views file that calls on the html templates when called on 
# by urls.py and does any additional logic required to display the desired page

from django.shortcuts import render
import random

# List of famous quotes from Joe Biden, both serious and comical,
# for use in this application.
quote_list = [
    "Democracy has prevailed.",
    "This is the time to heal in America.",
    "We will lead not only by the example of our power, but by the power of our example.",
    "America is an idea. An idea is stronger than any army, bigger than any ocean, more powerful than any dictator or tyrant.",
    "For God's sake, this man cannot remain in power.",
    "I am the Democratic Party right now.",
    "We didn't crumble after 9/11. We didn't falter after the Boston Marathon. But we're America. Americans will never, ever stand down. We endure. We overcome. We own the finish line.",
    "Will you shut up, man?",
    "This is a big fucking deal.",
    "We hold these truths to be self-evident. All men and women created by — you know, you know, the thing.",
    "Poor kids are just as bright and just as talented as white kids.",
    "Given a fair shot, given a fair chance, Americans have never, ever, ever, ever let their country down. Never. Never. Ordinary people like us. Who do extraordinary things.",
    "We choose truth over facts.",
    "You're a lying dog-faced pony soldier.",
    "God save the Queen, man.",
    "Let me start off with two words: Made in America.",
    "America is a nation that can be defined in a single word - awdsmeafoothimaaafootafootwhscuseme",
    "Don't compare me to the Almighty, compare me to the alternative.",
    "We finally beat Medicare."
]

# List of links to images of Joe Biden, both serious and comical, 
# for use in this application.
image_list = [
    "https://media.gq-magazine.co.uk/photos/5fa56a03ab4311e33c32f5c2/master/w_1600%2Cc_limit/GettyImages-1205678026.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/1c/President_Joe_Biden_delivers_his_State_of_the_Union_address_to_a_joint_session_of_Congress_in_the_House_Chamber_at_the_U.S._Capitol%2C_Thursday%2C_March_7%2C_2024%2C_in_Washington%2C_D.C.jpg",
    "https://s.abcnews.com/images/Politics/ap_joe_biden_ice_cream_02_floated_jc_141009_16x9_992.jpg?w=992",
    "https://upload.wikimedia.org/wikipedia/commons/f/f8/President_Joe_Biden_wears_his_aviator_sunglasses_while_working_at_the_Resolute_Desk_%2853235198805%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/65/P20240121AS-0405.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/4b/Joe_Biden_at_Jeni%27s_Splendid_Ice_Creams.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/49/Joe_Biden_talking_to_a_little_girl_while_holding_an_ice_cream_cone.jpg",
    "https://m.media-amazon.com/images/I/51XxDU4SESL.jpg",
    "https://www.reuters.com/resizer/v2/https%3A%2F%2Fcloudfront-us-east-2.images.arcpublishing.com%2Freuters%2FV3A7BCVI5FOZFCYGRLMRH4TEAU.jpg?auth=ead416904ead4c772580f93f8b48f043ec6a8f6c8b388036acc7e1d14d90222b&width=4238&quality=80",
    "https://www.bostonherald.com/wp-content/uploads/2019/10/bidensc007.jpg?w=1024",
    "https://media.rnztools.nz/rnz/image/upload/s--CxmELoLQ--/ar_16:10,c_fill,f_auto,g_auto,q_auto,w_1050/v1719603082/4KNVLIQ_AP24180637310520_jpg?_a=BACCd2AD",
    "https://rollcall.com/app/uploads/2022/07/biden_lightning030_042522.jpg",
    "https://e3.365dm.com/24/03/1600x900/skynews-joe-biden-us-president_6475306.jpg?20240301220256",
    "https://media.cnn.com/api/v1/images/stellar/prod/230620165219-01-joe-biden-062023.jpg?c=original",
    "https://cdn.abcotvs.com/dip/images/15354428_092524-cc-biden-on-th-view-new-img.jpg",
    "https://npr.brightspotcdn.com/dims3/default/strip/false/crop/4832x3221+0+0/resize/1100/quality/50/format/jpeg/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F3e%2Ff2%2F09f3d940483eb58ca81433530af1%2Fap24207002747143.jpg",
    "https://www.american.edu/alumni/news/images/Joe-Biden-1988-2_5589884_1200x630.jpg",
    "https://static.politico.com/22/cc/3506731d447d9a8598a6440dce04/webp.net-resizeimage%20(29).jpg",
    "https://media.gq.com/photos/66a25ffbff70c28a13d53043/master/w_2560%2Cc_limit/biden.jpg"
    ]

def home(request):
    """Respond to the URL '' to display the home page, delegate work to a template and
    returns the rendered web page as HTTP response
    """
    # Path to the html template
    template_name = 'quotes/quote.html'
    # choose a random quote and image to display for the static variables to be used in the template
    context = {
        "quote": random.choice(quote_list),
        "image": random.choice(image_list),
    }
    return render(request, template_name, context)

def quote(request):
    """Respond to the URL '/quote' to display a random quote and image, calls home to avoid repitition, and   
    returns the rendered web page as HTTP response
    """
    # quote page does the exact same thing as home page, so we can call home to avoid repitition
    return home(request)

def show_all(request):
    """Respond to the URL '/show_all' to display all quotes and images, delegate work to a template, and
    returns the rendered web page as HTTP response
    """
    # Path to the html template
    template_name = 'quotes/show_all.html'
    #Match up random quotes to random images for the static variable
    shuffled_quotes = quote_list[:]
    shuffled_images = image_list[:]
    random.shuffle(shuffled_quotes)
    random.shuffle(shuffled_images)
    quote_image_pairs = zip(shuffled_quotes, shuffled_images)
    # send the matched up list of pairs to the template to be for looped over
    context = {
        "quote_image_pairs": quote_image_pairs,
    }
    return render(request, template_name, context)

def about(request):
    """Respond to the URL '/about' to display the about page, delegate work to a template, and
    returns the rendered web page as HTTP response
    """
    # Path to the html template
    template_name = 'quotes/about.html'
    # no additional context needed for about page
    return render(request, template_name)