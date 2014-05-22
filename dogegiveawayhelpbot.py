import time
import praw

#identifies the bot to reddit
r = praw.Reddit('Dogecoin giveaway tipper')
#input username and password the bot will use here.
r.login("USERNAME","PASSWORD")
already_done = set()
words = ['Giveaway', 'giveaway']


def find_giveaway():
        print 'Starting...'
        subreddit = r.get_subreddit('dogecoin')
        #Gets the last 25 submissions from /r/dogecoin
        subreddit_submissions = subreddit.get_new(limit=25)
        print 'Looking for giveaway post'
        for submission in subreddit_submissions:
                post_title = submission.title.lower()
                #Creates a text file that logs the submissions its already seen
                obj = open('alreadyseen.txt', 'ab+')
                #Sees if the title of the post has the word "giveaway" in it
                has_word = any(string in post_title for string in words)
                link = submission.permalink
                if link in open("faucet_users.txt").read():
                        #Checks to see if it has enough upvotes
                        if submission.ups>10:
                                if submission.id not in already_done and has_word:
                                        print 'Found post that qualifies! Commenting...'
                                        #This is the comment the bot leaves on the giveaway, change it to suit your needs.
                                        submission.add_comment('+/u/dogetipbot 15 doge \n\n^^Please ^^consider ^^tipping ^^this ^^bot ^^to ^^keep ^^me ^^running! \n\n^^Owned ^^by ^^/u/cbg119. ^^Problems? ^^Shoot ^^me ^^a ^^message!')
                                        already_done.add(submission.id)
                                        obj.write(link + ' ') 
                                        obj.close()
                                        time.sleep(30)
                                        break
#loops the defined function
while True:
        find_giveaway()
        print 'Done. Starting over in 30 seconds.'
        time.sleep(30)

