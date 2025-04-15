# wordly
so first of all we need to make the game.
before this experience i've never done something like this.
so еo do this, I made a plan that I could build on later.
First is like first screen. First screen would be like this:
Play with AI (there need to be using open source AI)
play with friends (there need to be like this: one man create a word, second need to guess it)
And finally last button would be the difficult button (need on AI version of wordly: first level it’s infinity tries and three hints, second like 10 tries and 1 hint, third like 5 tries and no hints and fourth like three tries and no hints)
So, the game screen. This would be easy. Just number of rows is determined by the difficulty level and the number of attempts. In this rows is just a word of 5 letters. 
If you correct guess the letter but not in right place the letter is yellow if correct letter and correct place the letter is green.
To do this, I used these materials:

https://youtu.be/-a1Wjuinqvc?si=aEAvpEZPRQfpqFRU

this video is about complaining chatGPT and ruGPT-3.5 by SBER(which i'm using right now)

https://youtu.be/O-fGWA_tOH4?si=gVAx6Mi50BJryM9J

this video helps with understanding how to print coloured text

https://arxiv.org/abs/2309.10931

this paper is complaining morphologically analyze russian dictionary

https://www.researchgate.net/publication/374707138_Information_Theory-based_Wordle_Game_Word_Difficulty_Classification_and_Dynamic_Planning_Optimization_Research

this paper should help you configure your difficulty

https://youtu.be/QFhWS4qh2XY?si=7uWXackUrsaq3Y1m

this video is like tutorial of packaging python projects(i've never done it иуащку so i use it pretty much every time)


if you haven't installed some libraries there's all you need to do:

pip install transformers sentencepiece termcolor pymorphy2 langdetect
