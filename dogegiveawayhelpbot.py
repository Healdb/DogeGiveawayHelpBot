import time
import praw
import re
#identifies the bot to reddit
r = praw.Reddit('Dogecoin giveaway tipper')
#input username and password the bot will use here.
r.login("USERNAME","PASSWORD")
already_done = set()
words = ['Giveaway', 'giveaway']
dogeTerms = ['+/u/dogetipbot']
tip_amount_pattern = re.compile("D?(\d+) ?(?:D|doge)?", re.IGNORECASE)


def find_giveaway():
        print 'Starting...'
        subreddit = r.get_subreddit('dogecoin')
        #Gets the last 25 submissions from /r/dogecoin
        subreddit_submissions = subreddit.get_new(limit=100)
        print 'Looking for giveaway post'
        for submission in subreddit_submissions:
                post_title = submission.title.lower()
                #Creates a text file that logs the submissions its already seen
                obj = open('alreadyseen.txt', 'ab+')
                #Sees if the title of the post has the word "giveaway" in it
                has_word = any(string in post_title for string in words)
                link = submission.permalink
                sub_id = submission.id
                if sub_id not in open("alreadyseen.txt").read() and has_word:
                        #Checks to see if it has enough upvotes
                        if submission.ups>=3:
                                if sub_id not in already_done:
                                        print 'Found post that qualifies! Commenting...'
                                        #This is the comment the bot leaves on the giveaway, change it to suit your needs.
                                        submission.add_comment('+/u/dogetipbot 50 doge \n\n'
                                        '^^Please ^^consider ^^tipping ^^this ^^bot ^^to ^^keep ^^me ^^running ^^and ^^to ^^see ^^larger ^^tips!\n\n'
                                        '^^Owned ^^by ^^/u/cbg119. ^^Problems? ^^Shoot ^^me ^^a ^^message!')
                                        already_done.add(sub_id)
                                        obj.write(sub_id + '  ') 
                                        obj.close()
                                        time.sleep(30)
                                        break
#Thanks the people who donate to the bot
#This still needs to be worked on, as it does not catch every tip, but almost every tip.

def check_tip():
    messages = r.get_unread('comments')
    for message in messages:
        obj = open('tipreplies.txt', 'ab+')
        tip_message = message.body
        has_tip = any(string in tip_message for string in dogeTerms)
        if message.id not in open("tipreplies.txt").read() and has_tip:
            if message.id not in already_done:
                amount_found = tip_amount_pattern.findall(tip_message)
                if amount_found:
                    print 'Donation received! Thanking for donation.'
                    message.reply('Thank you for donating! This will keep me running longer!')
                    already_done.add(message.id)
                    obj.write(message.id + '  ')
                    obj.close()
                    time.sleep(30)
                    break

        
#loops the defined functions
while True:
        find_giveaway()
        check_tip()
        print 'Done. Starting over in 30 seconds.'
        time.sleep(30)
